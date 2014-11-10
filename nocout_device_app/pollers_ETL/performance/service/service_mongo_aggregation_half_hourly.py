from nocout_site_name import *
import imp
from datetime import datetime, timedelta
from itertools import groupby
from operator import itemgetter
from pprint import pprint, pformat
import collections

mongo_module = imp.load_source('mongo_functions', '/omd/sites/%s/nocout/utils/mongo_functions.py' % nocout_site_name)
config_mod = imp.load_source('configparser', '/omd/sites/%s/nocout/configparser.py' % nocout_site_name)

configs = config_mod.parse_config_obj()
desired_site = filter(lambda x: x == nocout_site_name, configs.keys())[0]
desired_config = configs.get(desired_site)

mongo_configs = {
		'host': desired_config.get('host'),
		'port': int(desired_config.get('port')),
		'db_name': desired_config.get('nosql_db')
		}

def mongo_main():
	global mongo_configs
	docs = []
	#end_time = datetime.now()
	end_time = datetime.now()
	start_time = end_time - timedelta(hours=1)
	# Read data from mongodb, performance live data
    	docs = sorted(read_data(start_time, end_time, configs=mongo_configs), key=itemgetter('host'))
	print '## Doc len ##'
	print len(docs)
        # Grouping based on hosts names
        group_hosts = groupby(docs, key=itemgetter('host'))
	for host, services in group_hosts:
		#print "$$$$$$$$$$$$$$$$$$$$$$$$$"
		#print host
		# Sort based on services
		host_services = sorted(list(services), key=itemgetter('host'))
		# Grouping based on service types, for a particular host
		group_services = groupby(host_services, key=itemgetter('service'))
                for serv_name, serv_data in group_services:
			#print serv_name
			# Docs for a particular service, to be aggregated
			service_doc_list = list(serv_data)
			# Grouping based on service data source
			service_doc_list = sorted(service_doc_list, key=itemgetter('ds'))
			service_data_source_grouping = groupby(service_doc_list, key=itemgetter('ds'))
			for data_source, values in service_data_source_grouping:
				#print data_source
				#print 'DS Values'
				#print pprint(list(values))
				make_half_hourly_data(list(values))
			#print '###############'


def read_data(start_time, end_time, **configs):
	db = None
	docs = []
       	db = mongo_module.mongo_conn(
		host=configs.get('configs').get('host'),
			port=configs.get('configs').get('port'),
			db_name=configs.get('configs').get('db_name')
			)
	print start_time, end_time
	if db:
	    cur = db.service_perf.find({"data":{ "$elemMatch": { "time" : { "$gt": start_time, "$lt": end_time}}}})
        
	for doc in cur:
		docs.append(doc)
	
	return docs


def make_half_hourly_data(docs):
	"""
	Quantifies the perf data in 30 mins time frame
	"""
	
	# Aggregated data doc to be inserted into historical mongodb 
	aggr_data = {}
	# Store the hour-wise perf data into a dict
	hour_wise_perf = {}
	host, ip_address = docs[0].get('host'), docs[0].get('ip_address')
	ds, service = docs[0].get('ds'), docs[0].get('service')
	site = docs[0].get('site')
	for doc in docs:
		data_values = sorted(doc.get('data'), key=itemgetter('time'))
		# Club the data entries based on hour value
		group_values_on_hour = groupby(data_values, key=lambda entry: entry.get('time').hour)
		for hours, hour_values in group_values_on_hour:
			if hours in hour_wise_perf.keys():
			        hour_wise_perf[hours] += list(hour_values)
			else:
				hour_wise_perf[hours] = list(hour_values)

        #print '==== hour_wise_perf ===='
	#pprint(hour_wise_perf)
	for hour, perf in hour_wise_perf.items():
		#print 'perf--------'
		#print perf
		perf = map(lambda t: convert(t), perf)
		#print '---- perf after eval----------'
		#print perf
		# The aggregated data for the first-half would be pivoted to this time
		f_h_pivot_time = perf[0].get('time').replace(minute=30, second=0, microsecond=0)
		# The aggregated data for the second-half would be pivoted to this time
		s_h_pivot_time = f_h_pivot_time + timedelta(minutes=30)
		# 0 - 30 mins data for the particular hour
		first_half_data = filter(lambda entry: entry.get('time').minute <= 30, perf) 
		#print "-- First half data"
		#print first_half_data
		if first_half_data:
		        first_half_data_values = map(lambda e: e.get('value'), first_half_data)
			if not first_half_data_values[0]:
				f_h_min_val, f_h_max_val, f_h_avg_val = None, None, None
			else:
			        f_h_min_val = min(first_half_data_values)
			        f_h_max_val = max(first_half_data_values)
			        f_h_avg_val = sum(first_half_data_values)/len(first_half_data_values)

			aggr_data = {
					'host': str(host),
					'ip_address': str(ip_address),
					'time': f_h_pivot_time,
					'ds': str(ds),
					'service': str(service),
					'site': str(site),
					'min': f_h_min_val,
					'max': f_h_max_val,
					'avg': f_h_avg_val
					}
			#print "-- data to be inserted --"
			#print aggr_data
			# Find the existing doc to update
			find_query = {
					'host': aggr_data.get('host'),
					'service': aggr_data.get('service'),
					'ds': aggr_data.get('ds'),
					'time': aggr_data.get('time')
					}
			existing_doc = find_existing_entry(find_query)
			#print 'existing_doc'
			#print existing_doc
			if existing_doc:
				existing_doc = existing_doc[0]
				min_val = min([existing_doc.get('min'), aggr_data.get('min')]) 
				max_val = max([existing_doc.get('max'), aggr_data.get('max')]) 
				if aggr_data.get('avg'):
				        avg_val = (existing_doc.get('avg') + aggr_data.get('avg')) / 2
				else:
				        avg_val = existing_doc.get('avg')
				aggr_data.update({
					'min': min_val,
					'max': max_val,
					'avg': avg_val
					})
			upsert_aggregated_data(find_query, aggr_data)

		# 30 - 60 mins data for the particular hour
	        second_half_data = filter(lambda entry: entry.get('time').minute > 30, perf) 
		#print "-- second half data --"
		#print second_half_data
		if second_half_data:
		        second_half_data_values = map(lambda e: e.get('value'), second_half_data)
			#print 'second_half_data_values--'
			#print second_half_data_values
			if not second_half_data_values[0]:
				s_h_min_val, s_h_max_val, s_h_avg_val = None, None, None
			else:
			        s_h_min_val = min(second_half_data_values)
			        s_h_max_val = max(second_half_data_values)
			        s_h_avg_val = sum(second_half_data_values)/len(second_half_data_values)

			aggr_data = {
					'host': host,
					'ip_address': ip_address,
					'time': s_h_pivot_time,
					'ds': ds,
					'service': service,
					'site': site,
					'min': s_h_min_val,
					'max': s_h_max_val,
					'avg': s_h_avg_val
					}
			#print "-- data to be inserted --"
			#print aggr_data
			# Find the existing doc to update
			find_query = {
					'host': aggr_data.get('host'),
					'service': aggr_data.get('service'),
					'ds': aggr_data.get('ds'),
					'time': aggr_data.get('time')
					}
			existing_doc = find_existing_entry(find_query)
			#print 'existing_doc'
			#print existing_doc
			if existing_doc:
				existing_doc = existing_doc[0]
				min_val = min([existing_doc.get('min'), aggr_data.get('min')]) 
				max_val = max([existing_doc.get('max'), aggr_data.get('max')]) 
				if aggr_data.get('avg'):
				        avg_val = (existing_doc.get('avg') + aggr_data.get('avg')) / 2
				else:
					avg_val = existing_doc.get('avg')
				aggr_data.update({
					'min': min_val,
					'max': max_val,
					'avg': avg_val
					})
			upsert_aggregated_data(find_query, aggr_data)


def convert(data):
	if isinstance(data, basestring):
		try:
			data = eval(data)
		except Exception:
		        data =  str(data)
		return data
	elif isinstance(data, collections.Mapping):
		return dict(map(convert, data.iteritems()))
	elif isinstance(data, collections.Iterable):
		return type(data)(map(convert, data))
	else:
	        return data


def upsert_aggregated_data(find_query, doc):
	"""
	Insert the data into historical mongodb
	"""

        global mongo_configs
	mongo_configs['db_name'] = 'nocout_historical'
        # Mongodb connection object
       	db = mongo_module.mongo_conn(
		host=mongo_configs.get('host'),
			port=mongo_configs.get('port'),
			db_name=mongo_configs.get('db_name')
			)
	if db:
		db.service_perf_half_hourly.update(find_query, doc,upsert=True)

def find_existing_entry(find_query):
	"""
	Find the doc for update query
	"""

        global mongo_configs
	mongo_configs['db_name'] = 'nocout_historical'
	docs = []
        # Mongodb connection object
       	db = mongo_module.mongo_conn(
		host=mongo_configs.get('host'),
			port=mongo_configs.get('port'),
			db_name=mongo_configs.get('db_name')
			)
	if db:
		cur = db.service_perf_half_hourly.find(find_query)
	for doc in cur:
		docs.append(doc)

	return docs


if __name__ == '__main__':
	mongo_main()
