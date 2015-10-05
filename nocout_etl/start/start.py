from __future__ import absolute_import

import os
from sys import path

from celery.beat import PersistentScheduler
from celery.schedules import crontab
from kombu import Queue

from celery import Celery
from celery.utils.celery_sentinel import register_celery_alias

register_celery_alias('redis-sentinel')

app = Celery()
#app.control.purge()


class MyBeatScheduler(PersistentScheduler):
    def __init__(self, *args, **kwargs):
        # remove old schedule db file
        try:
            os.remove(kwargs.get('schedule_filename'))
        except OSError:
            pass
        super(MyBeatScheduler, self).__init__(*args, **kwargs)


class Config:
    PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # redis db to store device inventory info
    INVENTORY_DB = 3

    SENTINELS = [
		    ('10.133.19.165', 26379), 
		    ('10.133.19.165', 26380), 
		    ('10.133.12.163', 26379)
		    ]

    # quorum
    MIN_OTHER_SENTINELS = 2
    SERVICE_NAME = 'mymaster'
    # options needed for celery broker connection
    #BROKER_TRANSPORT_OPTIONS = {
	#	    'service_name': 'mymaster',
	#	    'sentinels': SENTINELS,
	#	    'min_other_sentinels': 2,
	#	    'db': 15
	#	    }
    BROKER_URL = 'redis://'

    CELERY_RESULT_BACKEND = 'amqp://'

    CELERY_IMPORTS = (
            'handlers.db_ops',
            'handlers.distribute',
            'network.network_etl',
            'service.service_etl',
            'service.kpi_etl',
	)
    d_route = {'queue': 'service', 'routing_key': 'service'}
    #CELERY_QUEUES = (
    #        Queue('celery', routing_key='celery'),
    #        Queue('service', routing_key='service'),
    #        )
#    CELERY_ROUTES = {
#		    'handlers.db_ops': d_route,
#		    'network.network_etl': d_route,
#		    'service.service_etl': d_route,
#		    'service.kpi_etl': d_route,
#		    }
    #CELERY_TRACK_STARTED = True
    CELERYD_LOG_COLOR = False
    CELERY_CHORD_PROPAGATES = False
    #CELERY_ALWAYS_EAGER = True
    #CELERY_IGNORE_RESULT = True
    CNX_FROM_CONF = os.path.join(PROJ_DIR, 'db_conf.ini')
    CELERYBEAT_SCHEDULE = {
    		'distribute-task': {
    			'task': 'distribute',
    			'schedule': crontab(),
    			'kwargs': {
    				'site_name': 'pub_slave_1',
    				'Q': 'q:perf:service',
    				'module': 'service.service_etl'
    				}
    			},
            #'network-main': {
            #    'task': 'network-main',
            #    'schedule': crontab(),
            #    'kwargs' : {'site_name':'pub_slave_1'},
            #    },
            #'service-main': {
            #    'task': 'service-main',
            #    'schedule': crontab(),
            #    'kwargs' : {'site_name':'pub_slave_1'},
            #    },
            'get-ul-issue-service-checks': {
            	'task' : 'get-ul-issue-service-checks',
            	'schedule': crontab(minute='*/2'),
            	'kwargs' : {'site_name':'pub_slave_1'},
            	},
            'build-export-dr-mrc':{
	        	'task' : 'build-export-dr-mrc',
	        	'schedule': crontab(minute='*/5'),
	        	'kwargs' : {'site_name':'pub_slave_1'},
	        	},
	     #'call_kpi_services':{
	     #   'task' : 'call_kpi_services',
	     #   'schedule': crontab(minute='*/5'),
	     # }
            }

app.config_from_object(Config)