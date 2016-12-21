# -*- encoding: utf-8; py-indent-offset: 4 -*-
from celery import task, group
# Django Dateformat utility
from django.utils.dateformat import format
# datetime utility
import datetime
from dateutil.relativedelta import *
from operator import itemgetter
from inventory.tasks import bulk_update_create
from device.models import Device, DeviceTechnology, DeviceType
from inventory.models import Sector
# Import nocout utils gateway class
from nocout.utils.util import NocoutUtilsGateway
from nocout.settings import PLANNED_EVENTS_ENABLED, PE_REDIS_HOST, PE_REDIS_PORT, PE_REDIS_DB
from alert_center.models import PlannedEvent
from inventory.models import Circuit
import redis
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

try:
	redis_conn = redis.StrictRedis(host=PE_REDIS_HOST, port=PE_REDIS_PORT, db=PE_REDIS_DB)
except Exception as e:
	redis_conn = None

def get_child_ips(device):
	'''
	This function fetch ip addresses connected after the given device
	'''
	ips = list()

	if device:
		ips.append(device.ip_address)
		
		if device.pe_ip.exists(): # PE
			pe_data = device.pe_ip.all()
			for bh in pe_data:
				try:
					ips.append(bh.aggregator.ip_address)
				except Exception, e:
					pass
				try:
					ips.append(bh.pop.ip_address)
				except Exception, e:
					pass
				try:
					ips.append(bh.bh_switch.ip_address)
				except Exception, e:
					pass
				bs_data = bh.basestation_set.all()
				for bs in bs_data:
					try:
						ips.append(bs.bs_switch.ip_address)
					except Exception, e:
						pass
					ips += list(bs.sector.values_list(
						'sector_configured_on__ip_address', flat=True
					))
		elif device.backhaul_aggregator.exists(): # Aggregator
			aggr_data = device.backhaul_aggregator.all()
			for bh in aggr_data:
				try:
					ips.append(bh.pop.ip_address)
				except Exception, e:
					pass
				try:
					ips.append(bh.bh_switch.ip_address)
				except Exception, e:
					pass
				bs_data = bh.basestation_set.all()
				for bs in bs_data:
					try:
						ips.append(bs.bs_switch.ip_address)
					except Exception, e:
						pass
					ips += list(bs.sector.values_list(
						'sector_configured_on__ip_address', flat=True
					))
		elif device.backhaul_pop.exists(): # POP
			pop_data = device.backhaul_pop.all()
			for bh in pop_data:
				try:
					ips.append(bh.bh_switch.ip_address)
				except Exception, e:
					pass
				bs_data = bh.basestation_set.all()
				for bs in bs_data:
					try:
						ips.append(bs.bs_switch.ip_address)
					except Exception, e:
						pass
					ips += list(bs.sector.values_list(
						'sector_configured_on__ip_address', flat=True
					))
		elif device.backhaul_switch.exists(): # BS Converter
			bh_data = device.backhaul_switch.all()
			for bh in bh_data:
				bs_data = bh.basestation_set.all()
				for bs in bs_data:
					try:
						ips.append(bs.bs_switch.ip_address)
					except Exception, e:
						pass
					ips += list(bs.sector.values_list(
						'sector_configured_on__ip_address', flat=True
					))
		elif device.bs_switch.exists(): # BS Switch
			bs_data = device.bs_switch.all()
			for bs in bs_data:
				ips += list(bs.sector.values_list(
					'sector_configured_on__ip_address', flat=True
				))

	return ','.join(list(set(ips)))

def set_planned_events_in_redis(dataset=[]):
	"""
	This function stores Planned Events data in redis on DA end
	"""
	if not dataset:
		return False

	if redis_conn:
		try:
			# format data
			planned_event_dict ={}
			if dataset:
				dataset = sorted(dataset,key=itemgetter(0))
			for entry in dataset:
				if len(entry) == 3:
					planned_event_dict[(entry[0],entry[1])] = (entry[2],)
				elif len(entry) == 5:
					planned_event_dict[(entry[0],entry[1])] = (entry[2],entry[3],entry[4])
			# Set Data to redis 
			redis_conn.set('planned_events', planned_event_dict)
		except Exception as e:
			logger.error('Set redis data exception -- PE')
			logger.error(e)

	return True

@task()
def get_planned_events():
	"""
	This function fetch planned events from monolith's database
	"""

	if PLANNED_EVENTS_ENABLED:
		# PE_COLUMNS = [
		# 	'ScheduledStartDate', 'ScheduledEndDate', 'EventType', 'PEOwnerDetails', 
		# 	'ChangeCoordinator', 'PETTno', 'SRNumber', 'Timing', 'Changesummary', 
		# 	'ChangeStatus', 'ImpactedDomain', 'Component', 'SectorID', 
		# 	'ResourceName', 'ServiceIDs'
		# ]
		PE_COLUMNS = [
			'SRNumber', 'ServiceIDs', 'ChangeStatus', 'ResourceName', 'ResourceType', 
			'ScheduledStartDate', 'ScheduledEndDate', 'TimeModified', 'EventType', 
			'Impacted_Domain', 'Executor', 'PE_TT_NO', 'Timing', 'Summary', 'Component', 
			'PEOwner', 'SectorID'
		]
		TABLE_NAME = 'Wireless1ServiceDump'

		query = 'SELECT \
					{0} \
				FROM \
					{1} \
				WHERE \
					NOT ISNULL(ResourceName) \
					AND \
					ResourceName != "" \
					AND \
					NOT ISNULL(PE_TT_NO) \
					AND \
					PE_TT_NO != ""\
				'.format(', '.join(PE_COLUMNS), TABLE_NAME)

		# Create instance of 'NocoutUtilsGateway' class
		nocout_utils = NocoutUtilsGateway()
		
		# Execute Query to get planned events from monolith DB
		planned_events_dataset = list()

		try:
			planned_events_dataset = nocout_utils.fetch_raw_result(query, machine='monolith')
		except Exception as e:
			logger.error('Query execution exception')
			logger.error(e)
			pass

		if planned_events_dataset:
			set_planned_events.delay(planned_events_dataset)

	return True

@task()
def set_planned_events(dataset):
	"""
	This function save given planned events to our database.
	"""

	if dataset:
		bulk_update_pe = list()
		bulk_create_pe = list()
		redis_dataset = list()
		g_jobs = list()

		for event in dataset:
			ticket_no = event.get('PE_TT_NO')
			resource_name = event.get('ResourceName')

			if ticket_no and resource_name:
				startdate = event.get('ScheduledStartDate', '')
				enddate = event.get('ScheduledEndDate', '')
				event_type = event.get('EventType', '')
				owner_details = event.get('PEOwner', '')
				change_coordinator = event.get('Executor', '')
				sr_number = event.get('SRNumber', '')
				timing = event.get('Timing', '')
				summary = event.get('Summary', '')
				status = event.get('ChangeStatus', '')
				impacted_domain = event.get('Impacted_Domain', '')
				component = event.get('Component', '')
				sectorid = event.get('SectorID', '')
				service_ids = event.get('ServiceIDs', '')
				nia = ''
				technnology = ''
				device_type = ''
				try:
					device_instance = Device.objects.get(
						ip_address=resource_name
					)
					technnology = device_instance.device_technology
					device_type = device_instance.device_type
					nia = get_child_ips(device_instance)
				except Exception as e:
					logger.error('{0} named Device not found'.format(str(resource_name)))
					continue


				if nia:
					redis_nia = nia
					# Calculate SS IPs from fetch circuit ids & merge then with NIA IPs
					try:
						if service_ids:
							ss_ips = list(Circuit.objects.filter(
								circuit_id__in=service_ids.split(',')
							).values_list(
								'sub_station__device__ip_address', flat=True
							))

							if ss_ips:
								redis_nia += ',' + ','.join(ss_ips)
							else:
								logger.error('No SS IPs found')
					except Exception as e:
						logger.error('SIA calculation exception')
						logger.error(e)
						pass

					try:
						pmp_port = None
						if component and str(component).lower() == 'sector':
							try:
								sector_instance = Sector.objects.get(sector_id__iexact=sectorid)
								pmp_port = sector_instance.sector_configured_on_port.name
							except Exception as e:
								logger.error('Sector Fetch Exception for === {0}'.format(str(sectorid)))
								logger.error(e)
								pass

						if pmp_port:
							redis_data = (startdate, enddate, redis_nia.split(','), pmp_port, resource_name)
						else:
							redis_data = (startdate, enddate, redis_nia.split(','))
						redis_dataset.append(redis_data)
					except Exception as e:
						logger.error('Planned Events -- Redis dataset exception')
						logger.error(e)
				
				impacted_customer = 0
				try:
					if service_ids:
						impacted_customer = len(filter(None, service_ids.split(',')))
				except Exception as e:
					logger.error('Impacted customer fetch error')
					logger.error(service_ids)
					logger.error(e)

				try:
					event_instance = PlannedEvent.objects.get(
						resource_name__iexact=resource_name,
						pettno__iexact=ticket_no
					)
				except Exception as e:
					event_instance = None
					pass

				if event_instance:
					# Update event info
					event_instance.startdate = startdate
					event_instance.enddate = enddate
					event_instance.event_type = event_type
					event_instance.technology_id = technnology
					event_instance.device_type_id = device_type
					event_instance.owner_details = owner_details
					event_instance.change_coordinator = change_coordinator
					event_instance.pettno = ticket_no
					event_instance.sr_number = sr_number
					event_instance.impacted_customer = impacted_customer
					event_instance.timing = timing
					event_instance.summary = summary
					event_instance.status = status
					event_instance.impacted_domain = impacted_domain
					event_instance.component = component
					event_instance.sectorid = sectorid
					event_instance.resource_name = resource_name
					event_instance.service_ids = service_ids
					event_instance.nia = nia

					# Add event instance to bulk_update_pe list
					bulk_update_pe.append(event_instance)
				else:
					# Add event instance to bulk_create_pe list
					bulk_create_pe.append(PlannedEvent(
						resource_name=resource_name,
						pettno=ticket_no,
						startdate=startdate,
						enddate=enddate,
						event_type=event_type,
						technology_id=technnology,
						device_type_id=device_type,
						owner_details=owner_details,
						change_coordinator=change_coordinator,
						sr_number=sr_number,
						impacted_customer=impacted_customer,
						timing=timing,
						summary=summary,
						status=status,
						impacted_domain=impacted_domain,
						component=component,
						sectorid=sectorid,
						service_ids=service_ids,
						nia=nia
					))

		if bulk_create_pe:
			g_jobs.append(bulk_update_create.s(
				bulk_create_pe,
				action='create',
				model=PlannedEvent
			))

		if bulk_update_pe:
			g_jobs.append(bulk_update_create.s(
				bulk_update_pe,
				action='update',
				model=PlannedEvent
			))

		if redis_dataset:
			set_planned_events_in_redis(
				dataset=redis_dataset
			)

		if not len(g_jobs):
			return False

		job = group(g_jobs)
		ret = False
		result = job.apply_async()  # start the jobs

	return True