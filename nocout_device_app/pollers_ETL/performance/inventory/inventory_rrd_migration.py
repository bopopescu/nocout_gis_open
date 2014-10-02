"""
inventory_rrd_migration.py
=======================

This file contains the code for extracting and collecting the data for inventory services and storing this data into embeded mongodb database.

Inventory services are services for which data is coming in 1 day interval.

"""

from nocout_site_name import *
import socket,json
import time
import imp



utility_module = imp.load_source('utility_functions', '/omd/sites/%s/nocout/utils/utility_functions.py' % nocout_site_name)
mongo_module = imp.load_source('mongo_functions', '/omd/sites/%s/nocout/utils/mongo_functions.py' % nocout_site_name)
config_module = imp.load_source('configparser', '/omd/sites/%s/nocout/configparser.py' % nocout_site_name)



class MKGeneralException(Exception):
    """
    Class defination for the Exception Class.
    Args: Exception object
    Kwargs: None
    Return: message
    Exception :None

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
                host_row = filter(lambda t: re.match(interface, t.split('|')[1]) \
                                and re.match(host, t.split('|')[2]), l_host_vars['all_hosts'])
                ss_device = host_row[0].split('|')[0]
        except Exception, e:
                raise Exception, e

        return ss_device



def inventory_perf_data(site,hostlist,mongo_host,mongo_port,mongo_db_name):
	"""
	inventory_perf_data : Function for collecting the data for inventory serviecs.Service state is also retunred for those services
	Args: site (site on poller on which devices are monitored)
	Kwargs: hostlist (all host on that site)

	Return : None
	Raises: No Exception
	"""

	invent_check_list = []
	invent_service_dict = {}
	matching_criteria = {}
	interface_oriented_service = ["cambium_ss_connected_bs_ip_invent"]
	db = mongo_module.mongo_conn(host = mongo_host,port = mongo_port,db_name =mongo_db_name)
	for host in hostlist:
		query = "GET hosts\nColumns: host_services\nFilter: host_name = %s\n" %(host[0])
		query_output = utility_module.get_from_socket(site,query).strip()
		service_list = [service_name for service_name in query_output.split(',')]
		for service in service_list:
			if service.endswith('_invent') or ('_invent' in service and ":" in service):
				invent_check_list.append(service)
		for service in invent_check_list:
			replaced_host = host[0]
			query_string = "GET services\nColumns: service_state plugin_output host_address\nFilter: " + \
			"service_description = %s\nFilter: host_name = %s\nOutputFormat: json\n" 	 	% (service,host[0])
			query_output = json.loads(utility_module.get_from_socket(site,query_string).strip())
			try:
				if query_output[0][1]:
					plugin_output = str(query_output[0][1].split('- ')[1])
					service_state = (query_output[0][0])
					if service_state == 0:
						service_state = "OK"
					elif service_state == 1:
						service_state = "WARNING"
					elif service_state == 2:
						service_state = "CRITICAL"
					elif service_state == 3:
						service_state = "UNKNOWN"
					host_ip = str(query_output[0][2])
				else:
					continue
				if interface_oriented_service[0] in service:
					ds= "bs_ip"
				else: 
					ds=service.split('_')[1:-1]
					ds = ('_').join(ds)
					if 'frequency' in ds:
						ds= 'frequency'
			except:
				continue
			current_time = int(time.time())
			if interface_oriented_service[0] in service:
				interface = service.split(' ')[1]
				service = service.split(' ')[0]
				replaced_host = get_ss(host=host[0], interface=interface)
				host_ip = replaced_host 	

			if service == "cambium_qos_invent":
				qos_plugin_output = plugin_output.split(' ')
				qos_ds = map(lambda x: x.split("=")[0],qos_plugin_output)
				qos_value_list = map(lambda x: x.split("=")[1],qos_plugin_output)

				for index in range(len(qos_ds)):
					if qos_value_list[index]:
						invent_service_dict = dict (sys_timestamp=current_time,check_timestamp=current_time,
						device_name=replaced_host,
						service_name=service,current_value=qos_value_list[index],min_value=0,max_value=0,avg_value=0,
						data_source=qos_ds[index],severity=service_state,site_name=site,warning_threshold=0,
						critical_threshold=0,ip_address=host_ip)
						
						matching_criteria.update({'device_name':str(host[0]),'service_name':service,
						'site_name':site,'data_source':qos_ds[index]})
						
						mongo_module.mongo_db_update(db,matching_criteria,invent_service_dict,"inventory_services")
						mongo_module.mongo_db_insert(db,invent_service_dict,"inventory_services")
						matching_criteria ={}
						invent_service_dict = {}
			else:
				invent_service_dict = dict (sys_timestamp=current_time,check_timestamp=current_time,device_name=replaced_host,
						service_name=service,current_value=plugin_output,min_value=0,max_value=0,avg_value=0,
						data_source=ds,severity=service_state,site_name=site,warning_threshold=0,
						critical_threshold=0,ip_address=host_ip)
			matching_criteria.update({'device_name':replaced_host,'service_name':service,'site_name':site})
			mongo_module.mongo_db_update(db,matching_criteria,invent_service_dict,"inventory_services")
			mongo_module.mongo_db_insert(db,invent_service_dict,"inventory_services")
			matching_criteria ={}
			invent_service_dict = {}
		invent_check_list = []


def inventory_perf_data_main():
	"""
	inventory_perf_data_main : Main Function for data extraction for inventory services.Function get all configuration from config.ini
	Args: None
	Kwargs: None

	Return : None
	Raises: No Exception
	"""
	try:
		configs = config_module.parse_config_obj()
		desired_site = filter(lambda x: x == nocout_site_name, configs.keys())[0]
		desired_config = configs.get(desired_site)
		site = desired_config.get('site')
		mongo_host = desired_config.get('host')
                mongo_port = desired_config.get('port')
                mongo_db_name = desired_config.get('nosql_db')
		query = "GET hosts\nColumns: host_name\nOutputFormat: json\n"
		output = json.loads(utility_module.get_from_socket(site,query))
		inventory_perf_data(site,output,mongo_host,int(mongo_port),mongo_db_name)
	except SyntaxError, e:
		raise MKGeneralException(("Can not get performance data: %s") % (e))
	except socket.error, msg:
		raise MKGeneralException(("Failed to create socket. Error code %s Error Message %s:") % (str(msg[0]), msg[1]))
if __name__ == '__main__':
	inventory_perf_data_main()	
		
				
