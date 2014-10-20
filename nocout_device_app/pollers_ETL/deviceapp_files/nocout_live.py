"""
nocout_live.py
==============

Script to handle on-demand live polling for a particular service data source
"""

from wato import *
from nocout_logger import nocout_log
from pprint import pformat
import subprocess
#import time
import re
from ast import literal_eval
from nocout import get_parent


interface_services = [
		'cambium_ul_rssi',
		'cambium_ul_jitter',
		'cambium_reg_count',
		'cambium_ul_jitter',
		'cambium_rereg_count',
		'cambium_ss_connected_bs_ip_invent'
		]

#def nocout_log():
#    """
#    Handles logging functinality for device app
#
#    Args:
#        
#    Kwargs:
#
#    Returns:
#        logger object, which logs the activities to a log file
#    
#    Comments:
#        Logging path - /tmp/nocout_da/<site_name>/nocout_live.log
#    """
#    logger=logging.getLogger('nocout_da')
#    os.system('mkdir -p /tmp/nocout_da')
#    os.system('chmod 777 /tmp/nocout_da')
#    os.system('mkdir -p /tmp/nocout_da/%s' % defaults.omd_site)
#    #os.system('mkdir -p /tmp/nocout_da/pardeep_slave_1')
#    fd = os.open('/tmp/nocout_da/%s/nocout_live.log' % defaults.omd_site, os.O_RDWR | os.O_CREAT)
#    #fd = os.open('/tmp/nocout_da/pardeep_slave_1/nocout_live.log', os.O_RDWR | os.O_CREAT)
#    if not len(logger.handlers):
#        logger.setLevel(logging.DEBUG)
#        handler=logging.FileHandler('/tmp/nocout_da/%s/nocout_live.log' % defaults.omd_site)
#        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#        handler.setFormatter(formatter)
#        logger.addHandler(handler)
#    os.close(fd)
#
#    return logger


logger = nocout_log()


def main():
    """
    Entry point for all the functions

    Returns:
        {
	 "success": 1,
	 "message": "Data fetched successfully",
	 "error_message": None,
	 "value": [] # The current values for the desired service data sources
	}
    """
    response = {
        "success": 1,
        "message": "Data fetched successfully",
        "error_message": None,
        "value": []
    }
    action = ''
    action = html.var('mode')
    if action == 'live':
        response['value'] = poll_device()
    else:
        response.update({
            "message": "No data",
            "error_message": "No action defined for this case"
        })

    html.write(pformat(response))


def poll_device():
    current_values = []
    logger.info('[Polling Iteration Start]')
    device = html.var('device')
    service = html.var('service')
    logger.info('device : %s and service : %s' % (device, service))
    # If in case no `ds` supplied in req obj, [''] would be supplied as default
    try:
        data_source_list = literal_eval(html.var('ds'))
    except Exception:
        data_source_list = ['']
        logger.error('No ds provided in request object', exc_info=True)
    if not data_source_list:
        data_source_list = ['']
    logger.debug('data_source_list : %s' % data_source_list)
    
    current_values = get_current_value(device, service, data_source_list)

    return current_values


def get_current_value_old(current_values, device=None, service=None, data_source_list=None):
    response = []
    # Teramatrix poller on which this device is being monitored
    site_name = get_site_name()
    cmd = '/opt/omd/sites/%s/bin/cmk -nvp --checks=%s %s' % (site_name, service, device)
    # Fork a subprocess
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    check_output, error = p.communicate()
    if check_output:
        reg_exp1 = re.compile(r'(?<=\()[^)]*(?=\)$)', re.MULTILINE)
        reg_exp2 = re.compile(r'^ *\S+', re.MULTILINE)
        # Parse perfdata for all services running on that device
        ds_current_states = re.findall(reg_exp1, check_output)
        logger.info('ds_current_states : %s' % ds_current_states)
        # Get all the service names, currently running
	current_services = map(lambda x: x.strip(), re.findall(reg_exp2, check_output)[:-1])
        logger.info('current_services : %s' % current_services)

        service_ds_pairs = zip(current_services, ds_current_states)
        desired_service_ds_pair = filter(lambda x: service in x[0], service_ds_pairs)
        logger.debug('desired_service_ds_pair : %s' % desired_service_ds_pair)
        if desired_service_ds_pair:
            ds_values = desired_service_ds_pair[0][1].split(' ')
            logger.info('ds_values : %s' % ds_values)
            for ds in data_source_list:
		# Parse the output to get current value for that data source
                desired_ds = filter(lambda x: ds in x.split('=')[0], ds_values)
                #logger.debug('desired_ds : %s' % desired_ds)
                current_values.extend(map(lambda x: x.split('=')[1].split(';')[0], desired_ds))
            #logger.info('current_values : %s' % current_values)
            #logger.info('[Polling Iteration End]')

    return current_values


def get_current_value(q,device=None, service_list=None, data_source_list=None):
     #response = []
     # Teramatrix poller on which this device is being monitored
     site_name = get_site_name()
     ss_device, ss_mac, bs_device = None, None, None
     old_device = device
     #logger.debug('service_list: ' + pformat(service_list))

     # Pass our custom alarm handler function to signal
     #signal.signal(signal.SIGALRM, alarm_handler)
     # Set timeout to 1sec (excepts floats only)
     #signal.alarm(0.5)
     for service in service_list:
	     device = old_device
	     if service in interface_services:
		     # Replace the device with bs_device for these services
		     ss_mac, bs_device = get_parent(host=device, db=False) 
		     #ss_mac, bs_device = ss_mac.lower(), bs_device.lower()
		     logger.debug('ss_mac and bs_device:' + pformat(ss_mac) + ' and ' + pformat(bs_device))
		     if ss_mac and bs_device:
			     old_device = device
			     device = bs_device
		     else:
			 logger.info('BS name or SS mac did not found for SS and service ' + \
					 pformat(device)  + ' ' + pformat(service))
			 data_dict = {device: []}
			 q.put(data_dict)
			 return 
	     # Getting result from compiled checks output
             cmd = '/omd/sites/%s/bin/cmk -nvp --checks=%s %s' % (site_name, service, device)
	     #start = datetime.datetime.now()
             # Fork a subprocess
             p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	#     while p.poll() is None:
	#	     time.sleep(0.1)
	#	     now = datetime.datetime.now()
	#	     #logger.debug('In while')
	#	     if (now-start).seconds > timeout:
	#		     #logger.debug('now-start ' + pformat((now-start).seconds))
	#		     os.kill(p.pid, signal.SIGKILL)
	#		     os.waitpid(-1, os.WNOHANG)
	#		     data_dict = {device: []}
	#		     q.put(data_dict)
	#		     return
	     check_output, error = p.communicate()
	     #check_output = """Check_mk version 1.2.2p3
	     #cambium_ul_rssi 0a:00:3e:df:b3:2e OK - Device received signal strength indication is -69   (ul_rssi=-69;-72;-82;;)
	     #cambium_ul_rssi 0a:00:3e:df:b3:f8 OK - Device received signal strength indication is -60   (ul_rssi=-60;-72;-82;;)
	     #cambium_ul_rssi 0a:00:3e:df:b3:41 OK - Device received signal strength indication is -71   (ul_rssi=-71;-72;-82;;)
	     #"""
	     logger.debug(' Check_output: ' + pformat(check_output))
             if check_output:
		 if service in interface_services:
			 check_output = filter(lambda t: ss_mac in t, check_output.split('\n'))
		         logger.debug('check_output after filtering:' + pformat(check_output))
			 try:
			 	check_output = check_output[0]
			 except Exception, e:
			 	logger.error('Empty check_output: ' + pformat(e))
				data_dict = {old_device: []}
			 	q.put(data_dict)
			 	return
                 reg_exp1 = re.compile(r'(?<=\()[^)]*(?=\)$)', re.MULTILINE)
                 # Parse perfdata for all services running on that device
                 ds_current_states = re.findall(reg_exp1, check_output)
                 logger.info('ds_current_states : %s' % ds_current_states)
 
                 # Placing all the ds values into one single list
                 if ds_current_states:
                         ds_values = ds_current_states[0].split(' ')
                         logger.info('ds_values : %s' % ds_values)
                         for ds in data_source_list:
                                 # Parse the output to get current value for that data source
                                 desired_ds = filter(lambda x: ds in x.split('=')[0], ds_values)
                                 logger.debug('desired_ds : %s' % desired_ds)
                                 data_values = (map(lambda x: x.split('=')[1].split(';')[0], desired_ds))
				 #logger.debug('data_values:' + pformat(data_values))
				 data_dict = {old_device: data_values}
				 q.put(data_dict)
				 #q.task_done()
				# Foramt for multiple serivces
				# if data_values:
				#	 if device in host_data_dict.keys():
				#		 host_data_dict[device].update(
				#				 {
				#					 service: data_values
				#					 }
				#				 )
				#	 else:
				#		 host_data_dict.update(
				#				 {
				#					 device: {
				#						 service: data_values
				#						 }
				#					 }
				#				 )
				#	 #response.append(data_dict)
				#	 logger.debug('current_values: ' + pformat(q.qsize()))
		 else:
			 data_dict = {old_device: []}
			 q.put(data_dict)
             #if error:
		     # Log the process error code
		     #logging.debug('Process exits with error code: ' + pformat(error))
     #q.put(host_data_dict)
     #return data_dict


def alarm_handler(signum, frame):
        #logger.debug('For loop -----------')
	raise Alarm


def get_site_name(site=None):
    site = defaults.omd_site

    return site