"""
rrd_migration.py
================

This script collects and stores data for all services running on all configured devices for this poller.

"""

from nocout_site_name import *
import os
import demjson,json
from pprint import pformat
import re
from datetime import datetime, timedelta
import subprocess
import pymongo
import imp
import time
import socket
import json
import sys
from itertools import groupby

try:
        import nocout_settings
        from nocout_settings import _LIVESTATUS, _DATABASES
except Exception, exp:
        print exp

utility_module = imp.load_source('utility_functions', '/omd/sites/%s/nocout/utils/utility_functions.py' % nocout_site_name)
mongo_module = imp.load_source('mongo_functions', '/omd/sites/%s/nocout/utils/mongo_functions.py' % nocout_site_name)
config_module = imp.load_source('configparser', '/omd/sites/%s/nocout/configparser.py' % nocout_site_name)

network_data_values = []
service_data_values = []
network_update_list = []
service_update_list = []
device_first_down_list = []

def load_file(file_path):
    #Reset the global vars
    host_vars = {
        "all_hosts": [],
        "ipaddresses": {},
        "host_attributes": {},
        "host_contactgroups": [],
    }
    try:
        execfile(file_path, host_vars, host_vars)
        del host_vars['__builtins__']
    except IOError, e:
        pass
    return host_vars

def build_export(site, network_result, service_result,mrc_hosts,device_down_output, db):
	"""
	Function name: build_export  (function export data from the rrdtool (which stores the period data) for all services for particular host
	and stores them in mongodb in particular structure)

	Args: site : site_name (poller name on which  deviecs are monitored)
	Kwargs: host(Device from which data to collected) , ip (ip for the device) ,mongo_host (mongodb host name ),
                mongo_db (mongo db connection),mongo_port(port for mongodb)
	Return : None
        Raises:
	    Exception: None
	"""
        current = int(time.time())
	global network_data_values
	global service_data_values
	global network_update_list
	global service_update_list
	global device_first_down_list
        age = None
	rt_min, rt_max = None, None
	rta_dict = {}
	data_dict = {
		"host": None,
		"service": None,
		"ds": None,
		"data": [],
		"meta": None,
		"ip_address": None,
		"severity":None,
		"age": None
	}
	matching_criteria ={}
	refer = ''
	threshold_values = {}
	severity = 'unknown'
	host_severity = 'unknown'
	device_first_down_entry =[]
	host_state = "unknown"
	device_first_down ={}
#	db = mongo_module.mongo_conn(
#	    host=mongo_host,
#	    port=int(mongo_port),
#	    db_name=mongo_db
#	)
	# Process network perf data
        nw_qry_output = network_result
	file_path = "/omd/sites/%s/etc/check_mk/conf.d/wato/hosts.mk" % site
	host_var = load_file(file_path)
	host_list = [str(index[0]) for index in nw_qry_output]
	if db:
		cur = db.device_first_down.find()
		for dict_entry in cur:
			device_first_down_list.append(dict_entry)		
	for entry in nw_qry_output:
                try:
		    threshold_values = get_threshold(entry[-1])
		    rt_min = threshold_values.get('rtmin').get('cur')
		    rt_max = threshold_values.get('rtmax').get('cur')
		    # rtmin, rtmax values are not used in perf calc
		    threshold_values.pop('rtmin', '')
		    threshold_values.pop('rtmax', '')
		    if entry[2] == 0:
		        host_state = 'up'
		    elif entry[2] == 1:
			host_state = 'down'
		# Age of last service state change
		    last_state_change = entry[-2]
		    age =last_state_change
                except:
                    continue
		for ds, ds_values in threshold_values.items():
			check_time = datetime.fromtimestamp(entry[3]) 
			# Pivot the time stamp to next 5 mins time frame
			local_timestamp = pivot_timestamp_fwd(check_time)
			host_severity =host_state
			if ds == 'pl':
				ds_values['cur'] = ds_values['cur'].strip('%')
				try:
					pl_war = ds_values['war']
					pl_crit = ds_values['cric']
					pl_cur = ds_values['cur']
				except:
					pl_war=None
					pl_crit=None
					pl_cur=None
					pass
				if pl_cur and pl_war and pl_crit:
					pl_cur = float(pl_cur)
					pl_war = float(pl_war)
					pl_crit = float(pl_crit)
					if pl_cur < pl_war:
						host_severity = "up"
					elif pl_cur >= pl_war and pl_cur <= pl_crit:
						host_severity = "warning"
					else:
						host_severity = "down"

				try:
					try:	
						device_first_down_entry = filter(lambda x: str(entry[0]) == x['host'],device_first_down_list)
					except Exception,e:
						pass	
					if device_first_down_entry:
						device_first_down=device_first_down_entry[0]
					if device_first_down == {} and ds_values['cur'] == '100':
						device_first_down['host'] = str(entry[0])
						device_first_down['severity']="down"
						device_first_down['time']=local_timestamp
						device_first_down_list.append(device_first_down)
					elif device_first_down and str(entry[0]) ==  device_first_down['host'] and \
						ds_values['cur'] != '100':
						device_first_down['severity']="up"
					elif device_first_down and str(entry[0]) == device_first_down['host'] and \
						device_first_down['severity'] == "up" \
						and ds_values['cur'] == '100':
						device_first_down['severity']="down"
						device_first_down['time']=local_timestamp
					if device_first_down['time']:
						refer = device_first_down['time']
				except Exception,e:
					refer = ''
			data_values = [{'time': check_time, 'value': ds_values.get('cur')}]
			if ds == 'rta':
				try:
					rta_war =  ds_values['war']
					rta_crit = ds_values['cric']
					rta_cur =  ds_values['cur']
				except:
					rta_war = None
					rta_cur =  None
					rta_crit= None
				if  rta_cur and rta_war and rta_crit:
					rta_cur = float(rta_cur)
					rta_war = float(rta_war)
					rta_crit = float(rta_crit)
					if rta_cur < rta_war:
						host_severity = "up"
					elif (rta_cur >= rta_war) and (rta_cur <= rta_crit):
						host_severity = "warning"
					else:
						host_severity = "down"
					
				rta_dict = {'min_value': rt_min, 'max_value': rt_max}
				data_values[0].update(rta_dict)
			data_dict.update({
				'site': site,
				'host': str(entry[0]),
				'service': 'ping',
				'ip_address': str(entry[1]),
				'severity': host_severity,
				'age': age,
				'ds': ds,
				'data': data_values,
				'meta': ds_values,
				'check_time': check_time,
				'local_timestamp': local_timestamp ,
				'refer':refer
				})
			matching_criteria.update({
				'host': str(entry[0]),
				'service': 'ping',
				'ds': str(ds)
				})
			# Update the value in status collection, Mongodb
			network_update_list.append(matching_criteria)
			#mongo_module.mongo_db_update(db, matching_criteria, data_dict, 'network_perf_data')
			network_data_values.append(data_dict)
			data_dict = {}
			host_severity = host_state
			matching_criteria = {}
		
		refer = ''
		device_first_down = {}
	after = int(time.time())
	#print len(device_first_down_list)
	#print len(first_down_crit_list)
	elapsed = after -current
	data_dict = {}
	current1 = int(time.time())
	matching_criteria ={}
	mrc_update = []
	mrc_insert = []
        indexed_insert_entry = {}
        indexed_update_entry = {}
	indexed_mrc_insert ={}
	indexed_mrc_update ={}
	value = 0
	mrc_host = None
	host_matched_row = None
	dr_host_entry = []
	original_dr_host_list = []
	dr_flag = 0
        serv_qry_output = service_result
	for host_row in host_var['all_hosts']:
		if 'dr:'in host_row:
			dr_host_entry.append(host_row)
			original_host = host_row.split('|')[0]
			original_dr_host_list.append(original_host)
	s_device_down_list = set(device_down_output)
	dr_services= ['wimax_pmp1_utilization','wimax_pmp2_utilization','wimax_pmp1_ul_util_bgp','wimax_pmp1_dl_util_bgp',
			'wimax_pmp2_ul_util_bgp','wimax_pmp2_dl_util_bgp']
	pmp1_mrc_services = ['wimax_pmp1_utilization','wimax_pmp1_ul_util_bgp','wimax_pmp1_dl_util_bgp']
	pmp2_mrc_services = ['wimax_pmp2_utilization','wimax_pmp2_ul_util_bgp','wimax_pmp2_dl_util_bgp']
	exceptional_serv = ['wimax_dl_cinr','wimax_ul_cinr','wimax_dl_intrf','wimax_ul_intrf','wimax_modulation_dl_fec','wimax_modulation_ul_fec',
                                'wimax_dl_rssi','wimax_ul_rssi']
	for entry in serv_qry_output:
                if len(entry) < 8:
                        continue
		if str(entry[2]) in dr_services:
			if str(entry[0]) in original_dr_host_list:
				dr_flag = 1
		
		if str(entry[0]) in s_device_down_list and not dr_flag :
			continue
		if not len(entry[-1]) and not dr_flag:
			continue
			   	
		threshold_values = get_threshold(entry[-1])
		severity = calculate_severity(entry[3])
		# Age of last service state change
		last_state_change = entry[-3]
		age = last_state_change
		data_dict.update({
			'service': str(entry[2]),
			'ip_address': entry[1],
			'severity': severity,
			'age': age
			})
		for ds, ds_values in threshold_values.items():
			check_time = datetime.fromtimestamp(entry[4])
			# Pivot the time stamp to next 5 mins time frame
			local_timestamp = pivot_timestamp_fwd(check_time)
			data_values = [{'time': check_time, 'value': ds_values.get('cur')}]
			data_dict.update({
				'site': site,
				'host': str(entry[0]),
				'service': str(entry[2]),
				'ip_address': entry[1],
				'severity': severity,
				'age': age,
				'ds': ds,
				'data': data_values,
				'meta': ds_values,
				'check_time': check_time,
				'local_timestamp': local_timestamp 
				})
			matching_criteria.update({
				'host': str(entry[0]),
				'service': str(entry[2]),
				'ds': str(ds)
				})
			if str(entry[2]) in pmp1_mrc_services and str(entry[0]) in mrc_hosts:
				indexed_mrc_insert[(str(entry[0]),str(entry[2]))]=data_dict
				indexed_mrc_update[(str(entry[0]),str(entry[2]))]=matching_criteria
				#mrc_insert.append(data_dict)
			        #mrc_update.append(matching_criteria)	
				#mrc_host =  str(entry[0])
				matching_criteria = {}
				data_dict = {}
				continue
			if str(entry[2]) in pmp2_mrc_services and str(entry[0]) in mrc_hosts:
				changed_mrc_service = str(entry[2]).replace('pmp2','pmp1')
				if (str(entry[0]),changed_mrc_service) in indexed_mrc_insert:
					if ds_values.get('cur') and indexed_mrc_insert[(str(entry[0]),changed_mrc_service)].get('data')[0]['value']:
						updated_value = eval(ds_values.get('cur')) +  \
								eval(indexed_mrc_insert[(str(entry[0]),changed_mrc_service)].get('data')[0]['value'])
						indexed_mrc_insert[(str(entry[0]),changed_mrc_service)].get('data')[0]['value']= updated_value
					elif ds_values.get('cur'):
						indexed_mrc_insert[(str(entry[0]),changed_mrc_service)].get('data')[0]['value']= ds_values.get('cur')
					
					if indexed_mrc_insert[(str(entry[0]),changed_mrc_service)]:
						service_update_list.append(indexed_mrc_update[(str(entry[0]),changed_mrc_service)])
						service_data_values.append(indexed_mrc_insert[(str(entry[0]),changed_mrc_service)])
						del indexed_mrc_insert[(str(entry[0]),changed_mrc_service)]
						del indexed_mrc_update[(str(entry[0]),changed_mrc_service)]
						
				
				else:
					changed_ds = ds.replace('pmp2','pmp1')
					data_dict['service']=changed_mrc_service
					data_dict['ds']=changed_ds	
						
					
			 					 
			if dr_flag:
				dr_flag= 0
				host_matched_row=filter(lambda x: re.match(str(entry[0]),x) ,dr_host_entry)
				dr_host = host_matched_row[0].split('|')[3].split(':')[1].strip(' ')
				#print 'dr_host'
				#print dr_host
				#print (dr_host,str(entry[2]))
				if (dr_host,str(entry[2])) in indexed_insert_entry:
					if str(entry[2]) in dr_services :
						if ds_values.get('cur') and indexed_insert_entry[(dr_host,str(entry[2]))].get('data')[0]['value']:
							total_val = eval(ds_values.get('cur')) + eval(indexed_insert_entry[(dr_host,str(entry[2]))].get('data')[0]['value'])
							indexed_insert_entry[(dr_host,str(entry[2]))].get('data')[0]['value']= total_val
							data_dict.get('data')[0]['value']=total_val
						elif ds_values.get('cur'):
							indexed_insert_entry[(dr_host,str(entry[2]))].get('data')[0]['value'] = ds_values.get('cur')
						#print ',,,,,,,,,,,,'
						#print data_dict
						#print indexed_insert_entry
		
						if indexed_insert_entry[(dr_host,str(entry[2]))]:
							service_update_list.append(indexed_update_entry[(dr_host,str(entry[2]))])
							service_data_values.append(indexed_insert_entry[(dr_host,str(entry[2]))])
							del indexed_insert_entry[(dr_host,str(entry[2]))]
							del indexed_update_entry[(dr_host,str(entry[2]))]
				elif str(entry[2]) in dr_services:
					indexed_insert_entry[(str(entry[0]),str(entry[2]))]=data_dict
					indexed_update_entry[(str(entry[0]),str(entry[2]))]=matching_criteria
					#print 'indexed_entry'
					#print indexed_insert_entry
					#print 'updated_entry'
					#print indexed_update_entry
					data_dict = {}
					matching_criteria = {}
					continue


				# insert utilization entry in dict with host as key		
			# Update the value in status collection, Mongodb
			service_update_list.append(matching_criteria)
			#mongo_module.mongo_db_update(db, matching_criteria, data_dict, 'serv_perf_data')
			service_data_values.append(data_dict)
			data_dict = {}
			matching_criteria = {}
	for key,values in indexed_insert_entry.items():
		try:
			service_update_list.append(indexed_update_entry[key])
			service_data_values.append(values)
		except:
			continue
	for key,values in indexed_mrc_insert.items():
		try:
			service_update_list.append(indexed_mrc_update[key])
			service_data_values.append(values)
		except:
			continue
	elap = int(time.time()) - current1
	#print 'service_data_values'
	#print service_data_values
	# Bulk insert the values into Mongodb
	#try:
	#	mongo_module.mongo_db_insert(db, service_data_values, 'serv_perf_data')
	#except Exception, e:
	#	print e.message


def insert_bulk_perf(net_values, serv_values,net_update,service_update ,device_first_down_list,db):
	#db = mongo_module.mongo_conn(
	#    host=mongo_host,
	#    port=int(mongo_port),
	#    db_name=mongo_db
	#)
	match_dict = {}
	try:
		for index3 in range(len(net_values)):
			mongo_module.mongo_db_update(db,net_update[index3], net_values[index3], 'network_perf_data')
		
		for index4 in range(len(serv_values)):
			mongo_module.mongo_db_update(db,service_update[index4], serv_values[index4], 'serv_perf_data')
	except Exception ,e:
		print e.message
	index1 = 0
	index2 = min(1000,len(net_values))
	#print len(net_values)
	#print len(serv_values)
	#print device_first_down_list
	try:
		while(index2 <= len(net_values)):
			mongo_module.mongo_db_insert(db, net_values[index1:index2], 'network_perf_data')
			#mongo_module.mongo_db_update(db,net_update[index1:index2], net_values[index1:index2], 'network_perf_data')
			index1 = index2
			if index2 >= len(net_values):
				break
			if (len(net_values) - index2)  < 1000:
				index2 += (len(net_values) - index2)
			else:
				index2 += 1000
	except Exception, e:
		print 'Insert error in NW perf values'
		print e.message

	try:
		index1 = 0
		index2 = min(1000,len(serv_values))
		while(index2 <= len(serv_values)):
			mongo_module.mongo_db_insert(db, serv_values[index1:index2], 'serv_perf_data')
			#mongo_module.mongo_db_update(db,service_update[index1:index2], serv_values[index1:index2], 'serv_perf_data')
			index1 = index2
			if index2 >= len(serv_values):
				break
			if (len(serv_values) - index2)  < 1000:
				index2 += (len(serv_values) - index2)
			else:
				index2 += 1000
	except Exception, e:
		print 'Insert error in Serv values'
		print e.message

	try:
		index3 =0
		for index3 in range(len(device_first_down_list)):
			match_dict = {'host':device_first_down_list[index3]['host']}
			mongo_module.mongo_db_update(db,match_dict, device_first_down_list[index3], 
			'device_first_down')
			
	except Exception,e:
		print e
		
def calculate_severity(severity_bit):
	"""
	Function to compute host service states
	"""
	severity = 'unknown'
	if severity_bit == 0:
		severity = 'ok'
	elif severity_bit == 1:
		severity = 'warning'
	elif severity_bit == 2:
		severity = 'critical'

	return severity


def get_host_services_name(site_name=None, db=None):
        """
        Function_name : get_host_services_name (extracts the services monitotred on that poller)

        Args: site_name (poller on which monitoring data is to be collected)

        Kwargs: mongo_host(host on which we have to monitor services and collect the data),mongo_db(mongo_db connection),
                mongo_port( port for the mongodb database)
        Return : None

        raise
             Exception: SyntaxError,socket error
        """
	
        try:
	    mrc_hosts = []
            st = datetime.now()
            current = int(time.time())
	    mrc_query = "GET services\nColumns: host_name service_state host_state host_address plugin_output\n"+ \
                        "Filter: service_description ~ wimax_pmp1_sector_id_invent\n"+\
                        "Filter: service_description ~ wimax_pmp2_sector_id_invent\nOr: 2\nOutputFormat: python\n"

            network_perf_query = "GET hosts\nColumns: host_name host_address host_state last_check host_last_state_change host_perf_data\nOutputFormat: python\n"
	    service_perf_query = "GET services\nColumns: host_name host_address service_description service_state "+\
                            "last_check service_last_state_change host_state service_perf_data\nFilter: service_description ~ _invent\n"+\
                            "Filter: service_description ~ _status\n"+\
                            "Filter: service_description ~ Check_MK\n"+\
                            "Filter: service_description ~ PING\n"+\
                            "Filter: service_description ~ wimax_pmp1_dl_util_kpi\n"+\
                            "Filter: service_description ~ wimax_pmp1_ul_util_kpi\n"+\
                            "Filter: service_description ~ wimax_pmp2_dl_util_kpi\n"+\
                            "Filter: service_description ~ wimax_pmp2_ul_util_kpi\n"+\
                            "Filter: service_description ~ cambium_ul_util_kpi\n"+\
                            "Filter: service_description ~ cambium_dl_util_kpi\n"+\
                            "Filter: service_description ~ radwin_dl_util_kpi\n"+\
                            "Filter: service_description ~ radwin_ul_util_kpi\n"+\
                            "Filter: service_description ~ mrotek_port_values\n"+\
			    "Filter: service_description ~ mrotek_ul_util_kpi\n"+\
	                    "Filter: service_description ~ mrotek_dl_util_kpi\n"+\
                            "Filter: service_description ~ rici_ul_util_kpi\n"+\
                            "Filter: service_description ~ rici_dl_util_kpi\n"+\
		            "Filter: service_description ~ radwin_ss_provis_kpi\n"+\
                            "Filter: service_description ~ cambium_ss_provis_kpi\n"+\
                            "Filter: service_description ~ wimax_ss_provis_kpi\n"+\
                            "Filter: service_description ~ wimax_ss_ul_issue_kpi\n"+\
                            "Filter: service_description ~ cambium_ss_ul_issue_kpi\n"+\
                            "Filter: service_description ~ cambium_bs_ul_issue_kpi\n"+\
                            "Filter: service_description ~ wimax_bs_ul_issue_kpi\n"+\
                            "Or: 24\nNegate:\nOutputFormat: python\n"
	    device_down_query = "GET services\nColumns: host_name\nFilter: service_description ~ Check_MK\nFilter: service_state = 3\n"+\
				"And: 2\nOutputFormat: python\n"

            #service_perf_query = "GET services\nColumns: host_name host_address service_description service_state "+\
            #                "last_check service_last_state_change host_state service_perf_data\nFilter: service_description ~ _invent\n"+\
            #                "Filter: service_description ~ _status\nFilter: service_description ~ Check_MK\nOr: 3\nNegate:\nOutputFormat: python\n"
            nw_qry_output = eval(get_from_socket(site_name, network_perf_query))
            serv_qry_output = eval(get_from_socket(site_name, service_perf_query))
            mrc_qry_output = eval(get_from_socket(site_name, mrc_query))
            device_down_output = eval(get_from_socket(site_name, device_down_query))
	    device_down_list =[str(item) for sublist in device_down_output for item in sublist]
	    for index in range(0,len(mrc_qry_output),2):
            	try:
                        if mrc_qry_output[index][0] == mrc_qry_output[index+1][0] and mrc_qry_output[index][2] != 1:
                                if mrc_qry_output[index][4] == mrc_qry_output[index+1][4]:
                                        mrc_hosts.append(mrc_qry_output[index][0])
                except:
                        continue
            build_export(
                       site_name,
                       nw_qry_output,
                       serv_qry_output,mrc_hosts,device_down_list,
                       db
            )
	    elapsed = int(time.time()) - current

        except SyntaxError, e:
            raise MKGeneralException(("Can not get performance data: %s") % (e))
        except socket.error, msg:
            raise MKGeneralException(("Failed to create socket. Error code %s Error Message %s:") % (str(msg[0]), msg[1]))
        except ValueError, val_err:
                print 'Error in serv/nw qry output'
                print val_err.message

def get_from_socket(site_name, query):
    """
        Function_name : get_from_socket (collect the query data from the socket)

        Args: site_name (poller on which monitoring data is to be collected)

        Kwargs: query (query for which data to be collectes from nagios.)

        Return : None

        raise
             Exception: SyntaxError,socket error
    """
    socket_path = "/omd/sites/%s/tmp/run/live" % site_name
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    machine = site_name[:-8]
    #socket_ip = _LIVESTATUS[machine]['host']
    #socket_port = _LIVESTATUS[machine][site_name]['port']
    #s.connect((socket_ip, socket_port))
    s.connect(socket_path)
    s.settimeout(60.0)
    s.send(query)
    s.shutdown(socket.SHUT_WR)
    output = ''
    while True:
     try:
     	out = s.recv(100000000)
     except socket.timeout,e:
	err=e.args[0]
	print 'socket timeout ..Exiting'
	if err == 'timed out':
		sys.exit(1) 
     out.strip()
     if not len(out):
        break
     output += out

    return output


class MKGeneralException(Exception):
    """
        This is the Exception class handing exception in this file.
        Args: Exception instance

        Kwargs: None

        return: class object

    """
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        return self.reason



def get_ss(host=None, interface=None):
	ss_device = None
	global nocout_site_name
        l_host_vars = {
		    "FOLDER_PATH": "",
		    "ALL_HOSTS": '', # [ '@all' ]
		    "all_hosts": [],
		    "clusters": {},
		    "ipaddresses": {},
		    "extra_host_conf": { "alias" : [] },
		    "extra_service_conf": { "_WATO" : [] },
		    "host_attributes": {},
		    "host_contactgroups": [],
		    "_lock": False,
	}
	# path to hosts file
	hosts_file = '/omd/sites/%s/etc/check_mk/conf.d/wato/hosts.mk' % nocout_site_name
	try:
		execfile(hosts_file, l_host_vars, l_host_vars)
		del l_host_vars['__builtins__']
		
		host_row = filter(lambda t: re.match(interface, t.split('|')[2]) \
				and re.match(host, t.split('|')[3]), l_host_vars['all_hosts'])
		ss_device = host_row[0].split('|')[0]
	except Exception, e:
		return ss_device

	return ss_device


def split_service_interface(serv_disc):

	return serv_disc[:-18], serv_disc[-17:]


def do_export(site, host, file_name,data_source, start_time, serv):
    """
    Function_name : do_export (Main function for extracting the data for the services from rrdtool)

    Args: site (poller on which devices are monitored)

    Kwargs: host(Device from which data to collected) , file_name (rrd file for data source) ,data_source (service data source),
                start_time (time from which data is extracted),serv (service)
    return:
           None
    Exception:
           JSONDecodeError
    """
    data_series = {}
    cmd_output ={}
    CF = 'AVERAGE'
    resolution = '-300sec';

    # Get India times (GMT+5.30)
    utc_time = datetime(1970, 1,1, 5, 30)
    end_time = datetime.now()

    year, month, day = end_time.year, end_time.month, end_time.day
    hour = end_time.hour
    #Pivoting minutes to multiple of 5, to synchronize with rrd dump
    minute = end_time.minute - (end_time.minute % 5)
    end_time = datetime(year, month, day, hour, minute)

    if start_time is None:
        start_time = end_time - timedelta(minutes=6)
    else:
	start_time = start_time + timedelta(minutes=1)

    #end_time = datetime.now() - timedelta(minutes=10)
    #start_time = end_time - timedelta(minutes=5)
    
    start_epoch = int(time.mktime(start_time.timetuple()))
    end_epoch = int(time.mktime(end_time.timetuple()))
   
    #Subtracting 5:30 Hrs to epoch times, to get IST
    #start_epoch -= 19800
    #end_epoch -= 19800

    # Command for rrdtool data extraction
    if start_time > end_time:
	return
    cmd = '/omd/sites/%s/bin/rrdtool xport --json --daemon unix:/omd/sites/%s/tmp/run/rrdcached.sock -s %s -e %s --step 300 '\
        %(site,site, str(start_epoch), str(end_epoch))
    RRAs = ['MIN','MAX','AVERAGE']

    for RRA in RRAs:
    	cmd += 'DEF:%s_%s=%s:%d:%s XPORT:%s_%s:%s_%s '\
            %(data_source, RRA, file_name, 1, RRA, data_source,
                RRA, data_source, RRA)
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
    cmd_output, err = p.communicate()
    try:
        cmd_output = demjson.decode(cmd_output)
    except demjson.JSONDecodeError, e:
        return data_series

    legend = cmd_output.get('meta').get('legend')
    start_check = cmd_output['meta']['start']
    end_check = start_check+300
    start_check = datetime.fromtimestamp(start_check)
    end_check = datetime.fromtimestamp(end_check)
    local_timestamp = pivot_timestamp(start_check)

    data_series.update({
        "site": site,
        "legend": legend,
        "data" :cmd_output['data'],
        "start_time": start_check,
        "end_time": end_check,
        "check_time": start_check,
        "local_timestamp": local_timestamp
    })
    return data_series


def get_threshold(perf_data):
    """
    Function_name : get_threshold (function for parsing the performance data and storing in the datastructure)

    Args: perf_data performance_data extracted from rrdtool

    Kwargs: None
    return:
           threshold_values (data strucutre containing the performance_data for all data sources)
    Exception:
           None
    """

    threshold_values = {}

    if not len(perf_data):
    	return threshold_values
    for param in perf_data.split(" "):
	param = param.strip("['\n', ' ']")
	if param.partition('=')[2]:
        	if ';' in param.split("=")[1]:
            		threshold_values[param.split("=")[0]] = {
                	"war": re.sub('ms', '', param.split("=")[1].split(";")[1]),
                	"cric": re.sub('ms', '', param.split("=")[1].split(";")[2]),
                	"cur": re.sub('ms', '', param.split("=")[1].split(";")[0])
            		}
        	else:
            		threshold_values[param.split("=")[0]] = {
                	"war": None,
                	"cric": None,
                	"cur": re.sub('ms', '', param.split("=")[1].strip("\n"))
            		}
	else:
		threshold_values[param.split("=")[0]] = {
			"war": None,
			"cric": None,
			"cur": None
                        }

    return threshold_values


def pivot_timestamp(timestamp):
    """
    Function_name : pivot_timestamp (function for pivoting the time to 5 minutes interval)

    Args: timestamp

    Kwargs: None
    return:
           t_stmp (pivoted time stamp)
    Exception:
           None
    """
    t_stmp = timestamp + timedelta(minutes=-(timestamp.minute % 5))

  
    return t_stmp

def pivot_timestamp_fwd(timestamp):
    """
    Function_name : pivot_timestamp (function for pivoting the time to 5 minutes interval)

    Args: timestamp

    Kwargs: None
    return:
           t_stmp (pivoted time stamp)
    Exception:
           None
    """
    t_stmp = timestamp + timedelta(minutes=-(timestamp.minute % 5))
    #if (timestamp.minute %5) != 0:
    t_stmp = t_stmp + timedelta(minutes=5)

  
    return t_stmp



def db_port(site_name=None):
    """
    Function_name : db_port (function for extracting the port value for mongodb for particular poller,As different poller will 
		    have different)

    Args: site_name (poller on which monitoring is performed)

    Kwargs: None
    return:
           port (mongodb port)
    Exception:
           IOError
    """
    port = None
    if site_name:
        site = site_name
    else:
        file_path = os.path.dirname(os.path.abspath(__file__))
        path = [path for path in file_path.split('/')]

        if len(path) <= 4 or 'sites' not in path:
            raise Exception, "Place the file in appropriate omd site"
        else:
            site = path[path.index('sites') + 1]
    
    port_conf_file = '/omd/sites/%s/etc/mongodb/mongod.d/port.conf' % site
    try:
        with open(port_conf_file, 'r') as portfile:
            port = portfile.readline().split('=')[1].strip()
    except IOError, e:
        raise IOError, e

    return port


def mongo_conn(**kwargs):
    """
    Function_name : mongo_conn (function for making mongo db connection)

    Args: site_name (poller on which monitoring is performed)

    Kwargs: Multiple arguments
    return:
           db (mongdb object)
    Exception:
           PyMongoError
    """
    DB = None
    try:
        CONN = pymongo.Connection(
            host=kwargs.get('host'),
            port=kwargs.get('port')
        )
        DB = CONN[kwargs.get('db_name')]
    except pymongo.errors.PyMongoError, e:
        raise pymongo.errors.PyMongoError, e
    return DB


def insert_data(data_dict):
    """
    Function_name : insert_data (inserting data in mongo db)

    Args: data_dict (data_dict which is inserted)

    Kwargs: None
    return:
           None
    Exception:
           None
    """
    port = None
    db  = None
    #Get the port for mongodb process, specific to this multisite instance
    port = db_port()

    #Get the mongodb connection object
    db = mongo_module.mongo_conn(
        host='localhost',
        port=int(port),
        db_name='nocout'
    )

    if db:
        db.device_perf.insert(data_dict)
        return "Data Inserted into Mongodb"
    else:
        return "Data couldn't be inserted into Mongodb"


def rrd_migration_main(site,host,services,ip, mongo_host, mongo_db, mongo_port):
	"""
	Main function for the rrd_migration which extracts and store data in mongodb databses for all services configured on all devices
	Args: site : site (poller name on which  deviecs are monitored)
        Kwargs: host(Device from which data to collected) ,services(host services) ,ip (ip for the device) ,mongo_host (mongodb host name ),
	                mongo_db (mongo db connection),mongo_port(port for mongodb)
	return:
	      None
	Raise
	    Exception : None
	"""
	build_export(site, host, ip, mongo_host, mongo_db, mongo_port)

"""if __name__ == '__main__':
    build_export('BT','AM-400','PING')
"""



def collect_data_for_wimax(host,site,db):
		matching_criteria = {}
		wimax_service_list = ['wimax_modulation_dl_fec','wimax_modulation_ul_fec','wimax_dl_intrf','wimax_ul_intrf','wimax_ss_ip','wimax_ss_mac']
                for service in wimax_service_list:
                        query_string = "GET services\nColumns: service_state service_perf_data host_address last_check\nFilter: " + \
                        "service_description = %s\nFilter: host_name = %s\nOutputFormat: json\n"                % (service,host)
                        query_output = json.loads(utility_module.get_from_socket(site,query_string).strip())
                        try:
                                if query_output[0][1]:
                                        perf_data_output = str(query_output[0][1])
                                        service_state = (query_output[0][0])
                                        host_ip = str(query_output[0][2])
					last_check = (query_output[0][3])
                                        if service_state == 0:
                                                service_state = "OK"
                                        elif service_state == 1:
                                                service_state = "WARNING"
                                        elif service_state == 2:
                                                service_state = "CRITICAL"
                                        elif service_state == 3:
                                                service_state = "UNKNOWN"
                                        perf_data = utility_module.get_threshold(perf_data_output)
                                else:
                                        continue
                        except:
                                continue
                        for datasource in perf_data.iterkeys():
				data = []
                                cur =perf_data.get(datasource).get('cur')
                                war =perf_data.get(datasource).get('war')
                                crit =perf_data.get(datasource).get('cric')
				temp_dict = dict(value = cur,time = pivot_timestamp_fwd(datetime.fromtimestamp(last_check)))
                                wimax_service_dict = dict (check_time=datetime.fromtimestamp(last_check),
						local_timestamp=pivot_timestamp_fwd(datetime.fromtimestamp(last_check)),host=str(host),
                                                service=service,data=[temp_dict],meta ={'cur':cur,'war':war,'cric':crit},
                                                ds=datasource,severity=service_state,site=site,ip_address=host_ip)
                                matching_criteria.update({'host':str(host),'service':service,'ds':datasource})
                                mongo_module.mongo_db_update(db,matching_criteria,wimax_service_dict,"serv_perf_data")
                                mongo_module.mongo_db_insert(db,wimax_service_dict,"serv_perf_data")
				matching_criteria = {}
                wimax_service_dict = {}


def collect_data_from_rrd(db,site,path,host,replaced_host,service,ds_index,start_time,data_dict,status_dict):

	service_data_type = {
		"radwin_rssi" : int,
		"radwin_uas"  : int,
		"radwin_uptime": int,
		"radwin_service_throughput" : float,
		"radwin_dl_utilization": int,
		"radwin_ul_utilization" : int
	}

	m = -5
	data_series = do_export(site, host, path, ds_index, start_time, service)
	if data_series is None:
		return 1
	data_dict.update({
		"check_time": data_series.get('check_time'),
		"local_timestamp": data_series.get('local_timestamp'),
		"site": data_series.get('site')
        })
	status_dict.update({
		"check_time": data_series.get('check_time'),
		"local_timestamp": data_series.get('local_timestamp'),
		"site": data_series.get('site')
        })
 
	data_dict['ds'] = ds_index

	status_dict['ds'] = ds_index
			
	ds_values = data_series['data'][:-1]

	start_time = mongo_module.get_latest_entry(db_type='mongodb', db=db, table_name=None,
                                                                host=replaced_host, serv=data_dict['service'], ds=ds_index)
	temp_dict = {}
	for d in ds_values:
		if d[-1] is not None:
			m += 5
			if service in service_data_type:
				d_type = service_data_type[service]
			else:
				d_type = float
					
			temp_dict = dict(
					time=data_series.get('check_time') + timedelta(minutes=m),
						value=d_type(d[-1]))
			# forcing to not add deuplicate entry in mongo db. currenltly suppose at time 45.00 50.00 data comes in
			# in one iteration then in second iteration 50.00 55.00 data comes .So Not adding second iteration
			# 50.00 data again.
			if ds_index == 'rta':
				temp_dict.update({"min_value":d[-3],"max_value":d[-2]}) 
			if start_time == temp_dict.get('time'):
				data_dict.update({"local_timestamp":temp_dict.get('time')+timedelta(minutes=5),
				"check_time":temp_dict.get('time')+ timedelta(minutes=5)})
				continue
			data_dict.get('data').append(temp_dict)
	if len(temp_dict):
		status_dict.get('data').append(temp_dict)
		status_dict.update({"local_timestamp":temp_dict.get('time'),"check_time":temp_dict.get('time')})


if __name__ == '__main__':
    """
    main function for this file which is called in 5 minute interval.Every 5 min interval calculates the host configured on this poller
    and extracts data

    """
    configs = config_module.parse_config_obj()
    desired_site = filter(lambda x: x == nocout_site_name, configs.keys())[0]
    desired_config = configs.get(desired_site)
    site = desired_config.get('site')
    db = mongo_module.mongo_conn(
	    host=desired_config.get('host'),
	    port = int(desired_config.get('port')),
	    db_name= desired_config.get('nosql_db')
    )
    get_host_services_name(
    site_name=site,db=db
    )
    insert_bulk_perf(network_data_values, service_data_values,network_update_list,service_update_list ,device_first_down_list,db)
