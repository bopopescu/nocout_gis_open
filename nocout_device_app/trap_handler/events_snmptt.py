'''
Created on 19-Jan-2016

@author: TERAMATRIX\siddhika.nag

Script to read network event data and store to snmptt
'''
#from nocout_site_name import *
from datetime import datetime, timedelta
import imp
import time
from sys import path
path.append('nocout/performance/service')


# change module for production
db_ops_module = imp.load_source('db_ops', '/omd/sites/ospf2_slave_1/lib/python/handlers/db_ops.py')
#from handlers.db_ops import *

start_app_module = imp.load_source('start_pub', '/omd/sites/ospf1_slave_1/lib/python/start_pub.py')
app = start_app_module.app
#from start.start import app

mapper_module =  imp.load_source('mapper', '/omd/sites/ospf1_slave_1/nocout/performance/service/mapper.py')
#from trap_handler import mapper

from mapper import Eventmapper
# from trap_handler.mapper import Eventmapper

@app.task(name='insert_network_event')
def insert_network_event():
    data_list = make_network_snmptt_data()
    if data_list :
        #print "Data list network event",data_list
        worker = Eventmapper()
        worker.filter_events(data_list)
        
@app.task(name='insert_wimax_bs_ul_issue_event')
def insert_wimax_bs_ul_issue_event():
    data_list = make_bs_ul_issue_snmptt_data()
    if data_list :
        #print "Data list Wimax BS UL issue",data_list
        worker = Eventmapper()
        worker.filter_events(data_list)

@app.task(name='insert_cambium_bs_ul_issue_event')
def insert_cambium_bs_ul_issue_event():
    data_list = make_bs_ul_issue_snmptt_data()
    if data_list :
        #print "Data list cambium BS UL issue",data_list
        worker = Eventmapper()
        worker.filter_events(data_list)

@app.task(name='make_network_snmptt_data')
def make_network_snmptt_data():
    ds_event_mapping = {}
    {'rta':'Latency_Threshold_Breach'}
    try:
        queue = db_ops_module.RedisInterface(event_q = 'q:network:snmptt')
        cur = queue.get(0, -1)
        docs = []
        for doc in cur:
            severity = doc.get('severity').lower()
            ds  = doc.get('data_source')
            if severity == 'down':
                severity = 'critical'
            if severity == 'up':
                severity = 'clear'
            if ds == 'pl' and severity == 'major':
               event_name = 'PD_threshold_breach'
            elif ds == 'pl' and severity == 'critical':
                event_name = 'Device_not_reachable'
            elif ds == 'pl' and severity == 'clear':
                event_name = 'PD_threshold_breach'
                # Add alarm for clearing both major and critical alarm ,As we dnt know which was raised earlier.
                t = (
                 '',
                 event_name,
                 '',
                 doc.get('ip_address'),
                 '',
                 '',
                 severity,
                 '',
                 time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(doc.get('check_timestamp')))),
                 ''
                 )
                docs.append(t)
                event_name = 'Device_not_reachable'
            elif ds == 'rta' and severity  == 'critical':
                event_name = 'Latency_Threshold_Breach'
                severity = 'major'
            elif  ds == 'rta':
                event_name = 'Latency_Threshold_Breach'
            t = (
                 '',
                 event_name,
                 '',
                 doc.get('ip_address'),
                 '',
                 '',
                 severity,
                 '',
                 time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(doc.get('check_timestamp')))),
                 ''
                 )
            docs.append(t)
            t =()
        return docs
    except Exception,e :
        pass
        print "Error in Redis Tuple : %s \n",str(e)


@app.task(name='make_bs_ul_issue_snmptt_data')
def make_bs_ul_issue_snmptt_data():
    try:
        queue = db_ops_module.RedisInterface(event_q = 'q:bs_ul_issue_event')
        cur = queue.get(0, -1)
        #print '..........docs...'
	#print cur
        docs = []
        for doc in cur:
            severity = doc.get('state').lower()
            service  = doc.get('service_description')
            event_name = 'Uplink_Issue_threshold_Breach'
            if severity == 'critical' or severity == 'warning' :
                severity = 'major'
            if severity == 'ok':
                severity = 'clear'
            t = (
                 '',
                 event_name,
                 '',
                 doc.get('address'),
                 '',
                 '',
                 severity,
                 '',
                 time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(doc.get('last_chk')))),
                 ''
                 )
            docs.append(t)
            t =()
        return docs
    except Exception,e :
        #pass
        print "Error in BS UL Issue Redis Tuple : %s \n",str(e)
        
"""
@app.task(name='make_cambium_bs_ul_issue_snmptt_data')
def make_cambium_bs_ul_issue_snmptt_data():
    try:
        queue = db_ops_module.RedisInterface(event_q = 'q:cambium_bs_ul_issue_event')
        cur = queue.get(0, -1)
        docs = []
        for doc in cur:
            severity = doc.get('state').lower()
            service  = doc.get('service_description')
            event_name = 'Uplink_Issue_threshold_Breach'
            if severity == 'critical' or severity == 'warning' :
                severity = 'major'
            if severity == 'ok':
                severity = 'clear'
            t = (
                 '',
                 event_name,
                 '',
                 doc.get('address'),
                 '',
                 '',
                 severity,
                 '',
                 time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(doc.get('last_chk')))),
                 ''
                 )
            docs.append(t)
            t =()
        return docs
    except Exception,e :
        #pass
        print "Error in Cambium BS UL Issue Redis Tuple : %s \n",str(e)

if __name__ == '__main__':
    data_list = make_network_snmptt_data()
    if data_list :
        print "Data list",data_list
        worker = Eventmapper()
        print "Worker Obj : ",worker
        #worker.filter_traps(data_list)

"""