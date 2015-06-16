# coding=utf-8
import datetime
from random import randint
from HTMLParser import HTMLParser
import htmlentitydefs

from dateutil import tz
from django.db import connections
from operator import itemgetter
from nocout.settings import DATE_TIME_FORMAT, USE_TZ, CACHE_TIME

date_handler = lambda obj: obj.strftime(DATE_TIME_FORMAT) if isinstance(obj, datetime.datetime) else None

# for managing the slave-master connections
from django.conf import settings
import socket
# http://stackoverflow.com/questions/26608906/django-multiple-databases-fallback-to-master-if-slave-is-down

# https://github.com/benjamin-croker/loggy/blob/master/loggy.py
import inspect
from functools import wraps

# logging the performance of function
import logging

log = logging.getLogger(__name__)
# logging the performance of function

# # commented because of goes package is not supported for python 2.7 on centos 6.5
compare_geo = False
# Cause of MEMORY EXCEPTION
# TODO: Replace package
"""
try:
    import pyproj
    from shapely.geometry import Polygon, Point
    from shapely.ops import transform
    # commented because of goes package is not supported for python 2.7 on centos 6.5
    from functools import partial

    compare_geo = True
except Exception as e:
    log.exception(e)
    compare_geo = False
"""

import random
from django.core.cache import cache
# import Organization model
from organization.models import Organization

project_group_role_dict_mapper = {
    'admin': 'group_admin',
    'operator': 'group_operator',
    'viewer': 'group_viewer',
}

if getattr(settings, 'PROFILE'):
    from line_profiler import LineProfiler as LLP
    from memory_profiler import LineProfiler as MLP
    from memory_profiler import show_results


class NocoutUtilsGateway:
    """
    This class works as gateway between nocout utils & other apps
    """
    def fetch_raw_result(self, query, machine='default'):
        """

        :param query:
        :param machine:
        :return:
        """
        param1 = fetch_raw_result(query, machine=machine)

        return param1

    def format_value(self, format_this, type_of=None):
        """

        :param format_this:
        :param type_of:
        :return:
        """
        param1 = format_value(format_this, type_of=type_of)
        
        return param1

    def cache_for(self, time):
        """

        :param time:
        :return:
        """
        param1 = cache_for(time)
        
        return param1

    def non_cached_all_gis_inventory(
        self, 
        monitored_only=False, 
        technology=None, 
        type_rf=None, 
        bs_id=None
    ):
        """

        :param monitored_only:
        :param technology:
        :param type_rf:
        :param bs_id:
        :return:
        """
        param1 = non_cached_all_gis_inventory(
            monitored_only=monitored_only, 
            technology=technology, 
            type_rf=type_rf, 
            bs_id=bs_id
        )
        
        return param1

    def cached_all_gis_inventory(
        self, 
        monitored_only=False, 
        technology=None, 
        type_rf=None, 
        bs_id=None, 
        device_list=None
    ):
        """

        :param monitored_only:
        :param technology:
        :param type_rf:
        :param bs_id:
        :param device_list:
        :return:
        """
        param1 = cached_all_gis_inventory(
            monitored_only=monitored_only, 
            technology=technology, 
            type_rf=type_rf, 
            bs_id=bs_id, 
            device_list=device_list
        )
        
        return param1

    def query_all_gis_inventory(
        self, 
        monitored_only=False, 
        technology=None, 
        type_rf=None, 
        bs_id=None, 
        device_list=None
    ):
        """

        :param monitored_only:
        :param technology:
        :param type_rf:
        :param bs_id:
        :param device_list:
        :return:
        """
        param1 = query_all_gis_inventory(
            monitored_only=monitored_only, 
            technology=technology, 
            type_rf=type_rf, 
            bs_id=bs_id, 
            device_list=device_list
        )
        
        return param1

    def convert_utc_to_local_timezone(self, datetime_obj=None):
        """

        :param datetime_obj:
        :return:
        """
        param1 = convert_utc_to_local_timezone(datetime_obj=datetime_obj)
        
        return param1

    def indexed_query_set(self, query_set, indexes, values, is_raw=False):
        """

        :param query_set:
        :param indexes:
        :param values:
        :param is_raw:
        :return:
        """
        param1 = indexed_query_set(query_set, indexes, values, is_raw=is_raw)
        
        return param1

    def check_item_is_list(self, items):
        """

        :param items:
        :return:
        """
        param1 = check_item_is_list(items)
        
        return param1

    def is_lat_long_in_state(self, latitude, longitude, state):
        """

        :param latitude:
        :param longitude:
        :param state:
        :return:
        """
        param1 = is_lat_long_in_state(latitude, longitude, state)
        
        return param1

    def disable_for_loaddata(self, signal_handler):
        """

        :param signal_handler:
        :return:
        """
        param1 = disable_for_loaddata(signal_handler)
        
        return param1

    def nocout_datatable_ordering(self, self_instance, qs, order_columns):
        """

        :param self_instance:
        :param qs:
        :param order_columns:
        :return:
        """
        param1 = nocout_datatable_ordering(self_instance, qs, order_columns)
        
        return param1

    def logged_in_user_organizations(self, self_object):
        """

        :param self_object:
        :return:
        """
        param1 = logged_in_user_organizations(self_object)
        
        return param1

    def html_to_text(self, html):
        """

        :param html:
        :return:
        """
        param1 = html_to_text(html)
        
        return param1

    def init_dict_differ_added(self, current_dict, past_dict):
        """

        :param current_dict:
        :param past_dict:
        :return:
        """
        param1 = DictDiffer(current_dict, past_dict).added()
        
        return param1

    def init_dict_differ_removed(self, current_dict, past_dict):
        """

        :param current_dict:
        :param past_dict:
        :return:
        """
        param1 = DictDiffer(current_dict, past_dict).removed()
        
        return param1

    def init_dict_differ_changed(self, current_dict, past_dict):
        """

        :param current_dict:
        :param past_dict:
        :return:
        """
        param1 = DictDiffer(current_dict, past_dict).changed()
        
        return param1

    def init_dict_differ_unchanged(self, current_dict, past_dict):
        """

        :param current_dict:
        :param past_dict:
        :return:
        """
        param1 = DictDiffer(current_dict, past_dict).unchanged()
        
        return param1

    def time_it(self):

        param1 = time_it()

        return param1 

    def fetch_ss_inventory(
        self,
        monitored_only=True,
        technology=None,
        device_name_list=None
    ):
        """
        """
        param1 = fetch_ss_inventory(
            monitored_only=monitored_only,
            technology=monitored_only,
            device_name_list=device_name_list
        )

        return param1

    def fetch_ptpbh_ss_inventory(
        self,
        monitored_only=True,
        technology='P2P',
        device_name_list=None
    ):
        """
        """
        param1 = fetch_ptpbh_ss_inventory(
            monitored_only=monitored_only,
            technology=technology,
            device_name_list=device_name_list
        )

        return param1

    def get_inventory_ss_query(
        self,
        monitored_only=True,
        technology=None,
        device_name_list=None,
        is_ptpbh=False
    ):
        """
        """
        param1 = get_inventory_ss_query(
            monitored_only=monitored_only,
            technology=monitored_only,
            device_name_list=device_name_list,
            is_ptpbh=is_ptpbh
        )

        return param1

    def fetch_sector_inventory(
        self,
        monitored_only=True,
        technology=None,
        device_name_list=None,
        grouped_query=True
    ):
        """
        """
        param1 = fetch_sector_inventory(
            monitored_only=monitored_only,
            technology=technology,
            device_name_list=device_name_list,
            grouped_query=grouped_query
        )

        return param1

    def fetch_dr_sector_inventory(
        self,
        monitored_only=True,
        technology='WiMAX',
        device_name_list=None,
        grouped_query=True
    ):
        """
        """
        param1 = fetch_dr_sector_inventory(
            monitored_only=monitored_only,
            technology=technology,
            device_name_list=device_name_list,
            grouped_query=grouped_query
        )

        return param1

    def fetch_mrc_sector_inventory(
        self,
        monitored_only=True,
        technology='WiMAX',
        device_name_list=None,
        grouped_query=True
    ):
        """
        """
        param1 = fetch_mrc_sector_inventory(
            monitored_only=monitored_only,
            technology=technology,
            device_name_list=device_name_list,
            grouped_query=grouped_query
        )

        return param1

    def get_inventory_sector_query(
        self,
        monitored_only=True,
        technology=None,
        device_name_list=None,
        is_dr=False,
        is_mrc=False,
        grouped_query=True
    ):
        """
        """
        param1 = get_inventory_sector_query(
            monitored_only=monitored_only,
            technology=technology,
            device_name_list=device_name_list,
            is_dr=is_dr,
            is_mrc=is_mrc,
            grouped_query=grouped_query
        )

        return param1

    def fetch_ptp_sector_inventory(self, monitored_only=True, device_name_list=None):
        """
        """
        param1 = fetch_ptp_sector_inventory(
            monitored_only=monitored_only,
            device_name_list=device_name_list
        )

        return param1

    def fetch_ptpbh_sector_inventory(self, monitored_only=True, device_name_list=None):
        """
        """
        param1 = fetch_ptpbh_sector_inventory(
            monitored_only=monitored_only,
            device_name_list=device_name_list
        )

        return param1

    def get_ptp_sector_query(
        self,
        monitored_only=True,
        device_name_list=None,
        is_ptpbh=False
    ):
        """
        """
        param1 = get_ptp_sector_query(
            monitored_only=monitored_only,
            device_name_list=device_name_list,
            is_ptpbh=is_ptpbh
        )

        return param1

    def fetch_backhaul_inventory(
        self,
        monitored_only=True,
        device_name_list=None,
        type_rf='backhaul',
        grouped_query=True
    ):
        """
        """
        param1 = fetch_backhaul_inventory(
            monitored_only=monitored_only,
            device_name_list=device_name_list,
            type_rf=type_rf,
            grouped_query=grouped_query
        )

        return param1

    def get_bh_other_query(
        self,
        monitored_only=True,
        device_name_list=None,
        type_rf='backhaul',
        grouped_query=True
    ):
        """
        """
        param1 = get_bh_other_query(
            monitored_only=monitored_only,
            device_name_list=device_name_list,
            type_rf=type_rf,
            grouped_query=grouped_query
        )

        return param1

    def create_specific_key_dict(self, data_list, key_str):
        """
        """
        param1 = create_specific_key_dict(data_list, key_str)

        return param1



class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """

    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        """


        :return:
        """
        return self.set_current - self.intersect

    def removed(self):
        """


        :return:
        """
        return self.set_past - self.intersect

    def changed(self):
        """


        :return:
        """
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        """


        :return:
        """
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


def time_it(debug=getattr(settings, 'PROFILE')):
    """
    Profiler
    :param debug:
    """
    def decorator(fn):
        """

        :param fn:
        :return:
        """

        def wrapper(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """
            st = datetime.datetime.now()
            if debug:
                log.debug("+++" * 40)
                log.debug("START     \t\t\t: { " + fn.__name__ + " } : ")
                try:
                    # check the module calling the function
                    log.debug("          \t\t\t: function '{}' called by '{}' : '{}'".format(
                        fn.__name__,
                        inspect.stack()[1][3],
                        inspect.stack()[1][1],
                    )
                    )
                except:
                    pass
                # check the module calling the function
                profile_type = getattr(settings, 'PROFILE_TYPE')
                if profile_type == 'line':
                    profiler = LLP()
                elif profile_type == 'memory':
                    profiler = MLP()
                else:
                    profiler = None
                try:
                    if profiler:
                        profiled_func = profiler(fn)
                        result = profiled_func(*args, **kwargs)
                    else:
                        result = fn(*args, **kwargs)
                finally:
                    if profiler:
                        if profile_type == 'line':
                            profiler.print_stats()
                        elif profile_type == 'memory':
                            show_results(profiler)
                        else:
                            pass
                    else:
                        pass
            else:
                result = fn(*args, **kwargs)
            end = datetime.datetime.now()
            if debug:
                elapsed = end - st
                log.debug("TIME TAKEN\t\t\t: [{}".format(divmod(elapsed.total_seconds(), 60)))
                log.debug("END       \t\t\t: { " + fn.__name__ + " } : ")
                log.debug("+++" * 40)

            return result

        return wrapper

    return decorator


@time_it()
def fetch_raw_result(query, machine='default'):
    """
    django raw query does not get result in a single call, it iterates and calls the same query a lot of time
    which can be optmised if we pre fetch the results

    :param query: query to execute
    :param machine: machine name
    :return:the data fetched in form of a dictionary
    """
    db = machine
    db_slave = db + "_slave"
    if test_connection_to_db(database_name=db_slave):
        db = db_slave

    cursor = connections[db].cursor()
    cursor.execute(query)

    return dict_fetchall(cursor)


def test_connection_to_db(database_name):
    """
    REF: http://stackoverflow.com/questions/26608906/django-multiple-databases-fallback-to-master-if-slave-is-down
    :param database_name:
    :return:
    """
    try:
        db_definition = getattr(settings, 'DATABASES')[database_name]
        # if it gets a socket connection in 2 seconds
        s = socket.create_connection((db_definition['HOST'], db_definition['PORT']), 5)
        # if it gets a socket connection in 2 seconds
        s.close()
        return True
    except Exception as e:
        # general exception handelling
        # because connection might not exists in settings file
        return False


def dict_fetchall(cursor):
    """
    https://docs.djangoproject.com/en/1.6/topics/db/sql/
    return the cursor in dictionary format

    :param cursor: data base cursor
    :return: dictioanry of the rows
    """

    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def format_value(format_this, type_of=None):
    """

    :param type_of:
    :param format_this:
    :return:
    """
    if format_this:
        try:
            if not type_of:
                return format_this if format_this else 'NA'
            elif type_of == 'frequency_color':
                return format_this if format_this else 'rgba(74,72,94,0.58)'
            elif type_of == 'frequency_radius':
                return format_this if format_this else 0.5
            elif type_of == 'integer':
                return format_this if format_this else 0
            elif type_of == 'antenna':
                return format_this if format_this else 'vertical'
            elif type_of == 'random':
                return format_this if format_this else randint(40, 70)
            elif type_of == 'icon':
                if len(str(format_this)) > 5:
                    img_url = str("media/" + str(format_this)) \
                        if "uploaded" in str(format_this) \
                        else "static/img/" + str(format_this)
                    return img_url
                else:
                    return "static/img/icons/mobilephonetower10.png"
            elif type_of == 'mac':
                return format_this.upper() if format_this else 'NA'
            elif type_of == 'date':
                return str(format_this)
            elif type_of == 'epoch':
                return date_handler(format_this)
        except:
            return 'NA'
    else:
        return 'NA'

    return 'NA'


def cache_get_key(*args, **kwargs):
    """
    Get the cache key for storage
    :param kwargs:
    :param args:
    """
    import hashlib

    serialise = []
    for arg in args:
        serialise.append(str(arg))
    for key, arg in kwargs.items():
        serialise.append(str(key))
        serialise.append(str(arg))
    key = hashlib.md5("".join(serialise)).hexdigest()
    return key


def cache_for(time):
    """
    decorator for caching functions
    :param time:
    """
    def decorator(fn):
        """

        :param fn:
        :return:
        """

        def wrapper(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """
            debug = getattr(settings, 'PROFILE')
            st = datetime.datetime.now()
            if debug:
                log.debug("---" * 40)
                log.debug("FROM CACHE       \t: START : { " + fn.__name__ + " } : ")
            key = cache_get_key(fn.__name__, *args, **kwargs)
            result = cache.get(key)
            if not result:
                if debug:
                    log.debug("FUNCTION CALL\t: START : { " + fn.__name__ + " } : ")
                    # check the module calling the function
                    try:
                        # check the module calling the function
                        log.debug("          \t\t\t: function '{}' called by '{}' : '{}'".format(
                            fn.__name__,
                            inspect.stack()[1][3],
                            inspect.stack()[1][1],
                        )
                        )
                    except:
                        pass
                    # check the module calling the function
                    profile_type = getattr(settings, 'PROFILE_TYPE')
                    if profile_type == 'line':
                        profiler = LLP()
                    elif profile_type == 'memory':
                        profiler = MLP()
                    else:
                        profiler = None
                    try:
                        if profiler:
                            profiled_func = profiler(fn)
                            result = profiled_func(*args, **kwargs)
                        else:
                            result = fn(*args, **kwargs)
                    finally:
                        if profiler:
                            if profile_type == 'line':
                                profiler.print_stats()
                            elif profile_type == 'memory':
                                show_results(profiler)
                            else:
                                pass
                        else:
                            pass
                    cache.set(key, result, time)
                else:
                    result = fn(*args, **kwargs)
                    cache.set(key, result, time)

                if debug:
                    end = datetime.datetime.now()
                    elapsed = end - st
                    log.debug("TIME TAKEN   \t:       : [{}".format(divmod(elapsed.total_seconds(), 60)))
                    log.debug("FUNCTION CALL\t: END   : { " + fn.__name__ + " } : ")
            if debug:
                end = datetime.datetime.now()
                elapsed = end - st
                log.debug("TIME TAKEN       \t:       : [{}".format(divmod(elapsed.total_seconds(), 60)))
                log.debug("FROM CACHE       \t: END   : { " + fn.__name__ + " } : ")
                log.debug("---" * 40)
            return result

        return wrapper

    return decorator


def non_cached_all_gis_inventory(monitored_only=False, technology=None, type_rf=None, bs_id=None):
    """

    :param monitored_only: true false
    :param technology: technology name
    :param type_rf: sector, ss, bh
    :param bs_id: id of the base station
    :return: live cached result for the bs or for complete inventory
    """
    query = query_all_gis_inventory(monitored_only, technology, type_rf, bs_id=bs_id)
    return fetch_raw_result(query)


@cache_for(CACHE_TIME.get('INVENTORY', 300))  # caching GIS inventory
def cached_all_gis_inventory(monitored_only=False, technology=None, type_rf=None, bs_id=None, device_list=None):
    """

    :param monitored_only: true false
    :param technology: technology name
    :param type_rf: sector, ss, bh
    :param bs_id: id of the base station
    :param device_list: list of device names
    :return: cached result for the bs or for complete inventory
    """
    query = query_all_gis_inventory(monitored_only, technology, type_rf, bs_id=bs_id, device_list=device_list)
    return fetch_raw_result(query)


@time_it()
def query_all_gis_inventory(monitored_only=False, technology=None, type_rf=None, bs_id=None, device_list=None):
    """
    Function to get complete GIS inventory raw query(sql)
    :param monitored_only: True or False
    :param technology: Technology Name
    :param type_rf: sector or ss or backhaul
    :param bs_id: base station ID
    :param device_list: list of device names
    :return: query for gis
    """
    added_device = " "

    tech = " "

    if monitored_only:
        added_device = "where device.is_added_to_nms = 1 "

    if technology:
        tech = " and technology.name = '{0}'".format(technology)

    added_device += tech

    # based on devices
    get_these_devices = list()
    where_these_devices = ''

    # if device_list:
    #     for device in device_list:
    #         if device.get('id'):
    #             where_these_devices = ' device.id in '
    #             get_these_devices.append(device.get('id'))
    #         elif device.get('device_name'):
    #             where_these_devices = ' device.device_name in '
    #             get_these_devices.append(device.get('device_name'))
    #         elif device.get('name'):
    #             where_these_devices = ' device.device_name in '
    #             get_these_devices.append(device.get('name'))
    #         else:
    #             continue

    # search_these_devices = ''
    # if len(get_these_devices):
    #     search_these_devices = where_these_devices + " ( " + ",".join(get_these_devices) + " ) "


    # based on RF tech
    if type_rf == 'sector':
        rf_tech = " where SECTOR_TECH = '{0}' ".format(technology)
    elif type_rf == 'ss':
        rf_tech = " where SECTOR_TECH = '{0}' and SS_TECH = '{0}' ".format(technology)
    elif type_rf == 'bh':
        rf_tech = " where BHTECH = '{0}' ".format(technology)
    else:
        rf_tech = " "

    where_bs = ''
    if bs_id:
        where_bs = ' where basestation.id  = {0} '.format(bs_id)

    gis = '''
        SELECT * FROM (
                SELECT  basestation.id AS BSID,
                        basestation.name AS BSNAME,
                        basestation.alias AS BSALIAS,
                        basestation.bs_site_id AS BSSITEID,
                        basestation.bs_site_type AS BSSITETYPE,

                        device.ip_address AS BSSWITCH,

                        basestation.bs_type AS BSTYPE,
                        basestation.bh_bso AS BSBHBSO,
                        basestation.hssu_used AS BSHSSUUSED,
                        basestation.hssu_port AS BSHSSUPORT,
                        basestation.latitude AS BSLAT,
                        basestation.longitude AS BSLONG,

                        basestation.infra_provider AS BSINFRAPROVIDER,
                        basestation.gps_type AS BSGPSTYPE,
                        basestation.building_height AS BSBUILDINGHGT,
                        basestation.tower_height AS BSTOWERHEIGHT,
                        basestation.tag1 AS BSTAG1,
                        basestation.tag2 AS BSTAG2,
                        basestation.maintenance_status AS BSMAINTENANCESTATUS,

                        city.city_name AS BSCITY,
                        city.id AS BSCITYID,
                        state.state_name AS BSSTATE,
                        state.id AS BSSTATEID,
                        country.country_name AS BSCOUNTRY,

                        basestation.address AS BSADDRESS,

                        backhaul.id AS BHID,
                        sector.id AS SID,

                        basestation.bh_port_name AS BS_BH_PORT,
                        basestation.bh_capacity AS BS_BH_CAPACITY

                FROM inventory_basestation AS basestation
                LEFT JOIN inventory_sector AS sector
                ON sector.base_station_id = basestation.id
                LEFT JOIN inventory_backhaul AS backhaul
                ON backhaul.id = basestation.backhaul_id
                LEFT JOIN device_country AS country
                ON country.id = basestation.country_id
                LEFT JOIN device_city AS city
                ON city.id = basestation.city_id
                LEFT JOIN device_state AS state
                ON state.id = basestation.state_id
                LEFT JOIN device_device AS device
                ON device.id = basestation.bs_switch_id
    {2}
                )AS bs_info
    LEFT JOIN (
        SELECT * FROM (SELECT

        sector.id AS SECTOR_ID,
        sector.name AS SECTOR_NAME,
        sector.alias AS SECTOR_ALIAS,
        sector.sector_id AS SECTOR_SECTOR_ID,
        sector.base_station_id AS SECTOR_BS_ID,
        sector.mrc AS SECTOR_MRC,
        sector.dr_site AS SECTOR_DR,
        sector.tx_power AS SECTOR_TX,
        sector.rx_power AS SECTOR_RX,
        sector.rf_bandwidth AS SECTOR_RFBW,
        sector.frame_length AS SECTOR_FRAME_LENGTH,
        sector.cell_radius AS SECTOR_CELL_RADIUS,
        sector.modulation AS SECTOR_MODULATION,
        sector.planned_frequency AS SECTOR_PLANNED_FREQUENCY,

        technology.name AS SECTOR_TECH,
        technology.id AS SECTOR_TECH_ID,
        vendor.name AS SECTOR_VENDOR,
        devicetype.name AS SECTOR_TYPE,
        devicetype.id AS SECTOR_TYPE_ID,
        devicetype.device_icon AS SECTOR_ICON,
        devicetype.device_gmap_icon AS SECTOR_GMAP_ICON,

        device.id AS SECTOR_CONF_ON_ID,
        device.device_name AS SECTOR_CONF_ON,
        device.device_name AS SECTOR_CONF_ON_NAME,
        device.device_alias AS SECTOR_CONF_ON_ALIAS,
        device.ip_address AS SECTOR_CONF_ON_IP,
        device.mac_address AS SECTOR_CONF_ON_MAC,

        antenna.antenna_type AS SECTOR_ANTENNA_TYPE,
        antenna.height AS SECTOR_ANTENNA_HEIGHT,
        antenna.polarization AS SECTOR_ANTENNA_POLARIZATION,
        antenna.tilt AS SECTOR_ANTENNA_TILT,
        antenna.gain AS SECTOR_ANTENNA_GAIN,
        antenna.mount_type AS SECTORANTENNAMOUNTTYPE,
        antenna.beam_width AS SECTOR_BEAM_WIDTH,
        antenna.azimuth_angle AS SECTOR_ANTENNA_AZMINUTH_ANGLE,
        antenna.reflector AS SECTOR_ANTENNA_REFLECTOR,
        antenna.splitter_installed AS SECTOR_ANTENNA_SPLITTER,
        antenna.sync_splitter_used AS SECTOR_ANTENNA_SYNC_SPLITTER,
        antenna.make_of_antenna AS SECTOR_ANTENNA_MAKE,

        frequency.color_hex_value AS SECTOR_FREQUENCY_COLOR,
        frequency.frequency_radius AS SECTOR_FREQUENCY_RADIUS,
        frequency.value AS SECTOR_FREQUENCY,
        frequency.id AS SECTOR_FREQUENCY_ID,

        dport.name AS SECTOR_PORT,

        drd.id AS DR_CONF_ON_ID,
        drd.device_name AS DR_CONF_ON,
        drd.ip_address AS DR_CONF_ON_IP

        FROM inventory_sector AS sector
        JOIN (
            device_device AS device,
            inventory_antenna AS antenna,
            device_devicetechnology AS technology,
            device_devicevendor AS vendor,
            device_devicetype AS devicetype
        )
        ON (
            device.id = sector.sector_configured_on_id
        AND
            antenna.id = sector.antenna_id
        AND
            technology.id = device.device_technology
        AND
            devicetype.id = device.device_type
        AND
            vendor.id = device.device_vendor
        ) LEFT JOIN (device_devicefrequency AS frequency)
        ON (
            frequency.id = sector.frequency_id
        ) LEFT JOIN ( device_deviceport AS dport )
        ON (
            dport.id = sector.sector_configured_on_port_id
        ) LEFT JOIN (
            inventory_sector AS dr,
            device_device AS drd
        )
        ON (
            dr.id = sector.id
            AND
            drd.id = dr.dr_configured_on_id
        )
    {0}
    ) AS sector_info
    LEFT JOIN (
        SELECT circuit.id AS CID,
            circuit.alias AS CALIAS,
            circuit.circuit_id AS CCID,
            circuit.sector_id AS SID,

            circuit.circuit_type AS CIRCUIT_TYPE,
            circuit.qos_bandwidth AS QOS,
            circuit.dl_rssi_during_acceptance AS RSSI,
            circuit.dl_cinr_during_acceptance AS CINR,
            circuit.jitter_value_during_acceptance AS JITTER,
            circuit.throughput_during_acceptance AS THROUHPUT,
            circuit.date_of_acceptance AS DATE_OF_ACCEPT,

            customer.id AS CUSTID,
            customer.alias AS CUST,
            customer.address AS SS_CUST_ADDR,

            substation.id AS SSID,
            substation.name AS SS_NAME,
            substation.alias AS SS_ALIAS,
            substation.version AS SS_VERSION,
            substation.serial_no AS SS_SERIAL_NO,
            substation.building_height AS SS_BUILDING_HGT,
            substation.tower_height AS SS_TOWER_HGT,
            substation.ethernet_extender AS SS_ETH_EXT,
            substation.cable_length AS SS_CABLE_LENGTH,
            substation.latitude AS SS_LATITUDE,
            substation.longitude AS SS_LONGITUDE,
            substation.mac_address AS SS_MAC,

            antenna.height AS SSHGT,
            antenna.antenna_type AS SS_ANTENNA_TYPE,
            antenna.height AS SS_ANTENNA_HEIGHT,
            antenna.polarization AS SS_ANTENNA_POLARIZATION,
            antenna.tilt AS SS_ANTENNA_TILT,
            antenna.gain AS SS_ANTENNA_GAIN,
            antenna.mount_type AS SSANTENNAMOUNTTYPE,
            antenna.beam_width AS SS_BEAM_WIDTH,
            antenna.azimuth_angle AS SS_ANTENNA_AZMINUTH_ANGLE,
            antenna.reflector AS SS_ANTENNA_REFLECTOR,
            antenna.splitter_installed AS SS_ANTENNA_SPLITTER,
            antenna.sync_splitter_used AS SS_ANTENNA_SYNC_SPLITTER,
            antenna.make_of_antenna AS SS_ANTENNA_MAKE,

            device.ip_address AS SSIP,
            device.id AS SS_DEVICE_ID,
            device.device_alias AS SSDEVICEALIAS,
            device.device_name AS SSDEVICENAME,

            technology.name AS SS_TECH,
            technology.id AS SS_TECH_ID,
            vendor.name AS SS_VENDOR,
            devicetype.name AS SS_TYPE,
            devicetype.id AS SS_TYPE_ID,
            devicetype.name AS SSDEVICETYPE,
            devicetype.device_icon AS SS_ICON,
            devicetype.device_gmap_icon AS SS_GMAP_ICON

        FROM inventory_circuit AS circuit
        JOIN (
            inventory_substation AS substation,
            inventory_customer AS customer,
            inventory_antenna AS antenna,
            device_device AS device,
            device_devicetechnology AS technology,
            device_devicevendor AS vendor,
            device_devicetype AS devicetype
        )
        ON (
            customer.id = circuit.customer_id
        AND
            substation.id = circuit.sub_station_id
        AND
            antenna.id = substation.antenna_id
        AND
            device.id = substation.device_id
        AND
            technology.id = device.device_technology
        AND
            vendor.id = device.device_vendor
        AND
            devicetype.id = device.device_type
        )
    {0}
    ) AS ckt_info
    ON (
        ckt_info.SID = sector_info.SECTOR_ID
    )
    ) AS sect_ckt
    ON (sect_ckt.SECTOR_BS_ID = bs_info.BSID)
    LEFT JOIN
        (
            SELECT bh_info.BHID AS BHID,
                bh_info.BH_PORT AS BH_PORT,
                bh_info.BH_TYPE AS BH_TYPE,
                bh_info.BH_PE_HOSTNAME AS BH_PE_HOSTNAME,
                bh_info.BH_PE_IP AS BH_PE_IP,
                bh_info.BH_CONNECTIVITY AS BH_CONNECTIVITY,
                bh_info.BH_CIRCUIT_ID AS BH_CIRCUIT_ID,
                bh_info.BH_CAPACITY AS BH_CAPACITY,
                bh_info.BH_TTSL_CIRCUIT_ID AS BH_TTSL_CIRCUIT_ID,

                bh_info.BH_DEVICE_ID AS BH_DEVICE_ID,
                bh_info.BHCONF AS BHCONF,
                bh_info.BHCONF_IP AS BHCONF_IP,
                bh_info.BHTECH AS BHTECH,
                bh_info.BHTECHID AS BHTECHID,
                bh_info.BHTYPE AS BHTYPE,
                bh_info.BHTYPEID AS BHTYPEID,
                bh_info.BH_AGGR_PORT AS BH_AGGR_PORT,
                bh_info.BH_DEVICE_PORT AS BH_DEVICE_PORT,

                POP,
                POP_DEVICE_ID,
                POP_IP,
                POP_TECH,
                POP_TYPE,
                AGGR,
                AGGR_DEVICE_ID,
                AGGR_IP,
                AGGR_TECH,
                AGGR_TYPE,
                BSCONV,
                BSCONV_DEVICE_ID,
                BSCONV_IP,
                BSCONV_TECH,
                BSCONV_TYPE

        FROM (
        SELECT backhaul.id AS BHID,
                backhaul.bh_port_name AS BH_PORT,
                backhaul.bh_type AS BH_TYPE,
                backhaul.pe_hostname AS BH_PE_HOSTNAME,
                backhaul.pe_ip AS BH_PE_IP,
                backhaul.bh_connectivity AS BH_CONNECTIVITY,
                backhaul.bh_circuit_id AS BH_CIRCUIT_ID,
                backhaul.bh_capacity AS BH_CAPACITY,
                backhaul.ttsl_circuit_id AS BH_TTSL_CIRCUIT_ID,
                backhaul.aggregator_port AS BH_AGGR_PORT,
                backhaul.switch_port AS BH_DEVICE_PORT,

                device.id AS BH_DEVICE_ID,
                device.device_name AS BHCONF,
                device.ip_address AS BHCONF_IP,
                tech.name AS BHTECH,
                tech.id AS BHTECHID,
                devicetype.name AS BHTYPE,
                devicetype.id AS BHTYPEID

        FROM inventory_backhaul AS backhaul
        JOIN (
            device_device AS device,
            device_devicetype AS devicetype,
            device_devicetechnology AS tech
        )
        ON (
            device.id = backhaul.bh_configured_on_id
            AND
            tech.id = device.device_technology
            AND
            devicetype.id = device.device_type
        )

        ) AS bh_info LEFT JOIN (
                SELECT backhaul.id AS BHID,
                        device.id AS POP_DEVICE_ID,
                        device.device_name AS POP,
                        device.ip_address AS POP_IP,
                        devicetype.name AS POP_TYPE,
                        tech.name AS POP_TECH
                FROM inventory_backhaul
                AS backhaul
                LEFT JOIN (
                    device_device AS device,
                    device_devicetype AS devicetype,
                    device_devicetechnology AS tech
                )
                ON (
                    device.id = backhaul.pop_id
                    AND
                    tech.id = device.device_technology
                    AND
                    devicetype.id = device.device_type
                )
        ) AS pop_info
        ON (bh_info.BHID = pop_info.BHID)
        LEFT JOIN ((
                SELECT backhaul.id AS BHID,
                        device.id AS BSCONV_DEVICE_ID,
                        device.device_name AS BSCONV,
                        device.ip_address AS BSCONV_IP,
                        devicetype.name AS BSCONV_TYPE,
                        tech.name AS BSCONV_TECH
                FROM inventory_backhaul AS backhaul
                LEFT JOIN (
                    device_device AS device,
                    device_devicetype AS devicetype,
                    device_devicetechnology AS tech
                )
                ON (
                    device.id = backhaul.bh_switch_id
                    AND
                    tech.id = device.device_technology
                    AND
                    devicetype.id = device.device_type
                )
        ) AS bscon_info
        ) ON (bh_info.BHID = bscon_info.BHID)
        LEFT JOIN ((
                SELECT backhaul.id AS BHID,
                    device.id AS AGGR_DEVICE_ID,
                    device.device_name AS AGGR,
                    device.ip_address AS AGGR_IP,
                    devicetype.name AS AGGR_TYPE,
                    tech.name AS AGGR_TECH
                FROM inventory_backhaul AS backhaul
                LEFT JOIN (
                    device_device AS device,
                    device_devicetype AS devicetype,
                    device_devicetechnology AS tech
                )
                ON (
                    device.id = backhaul.aggregator_id
                    AND
                    tech.id = device.device_technology
                    AND
                    devicetype.id = device.device_type
                )
        ) AS aggr_info
        ) ON (bh_info.BHID = aggr_info.BHID)

    ) AS bh
    ON
        (bh.BHID = bs_info.BHID)

    {1}
     GROUP BY BSID,SECTOR_ID,CID;
        '''.format(added_device, rf_tech, where_bs)
    return gis


def convert_utc_to_local_timezone(datetime_obj=None):
    """
    Convert datetime object timezone from 'utc' to 'local'
    :param datetime_obj:
    Parameters:
        - datetime_obj ('datetime.datetime') - timestamp as datetime object for e.g. 2014-12-25 12:26:00+00:00

    Returns:
       - output (str) - output as a timestamp string for e.g. 12/25/14 (Dec) 17:56:03 (05:56 PM)
    """
    if USE_TZ:
        # get 'utc' timezone
        from_zone = tz.tzutc()

        # get 'local' timezone
        to_zone = tz.tzlocal()

        # output timestamp
        output = datetime_obj

        if output:
            try:
                # modify timezone info in datetime object to 'utc'
                output = output.replace(tzinfo=from_zone)

                # convert timezone from 'utc' to 'local'
                output = output.astimezone(to_zone)

                # format datetime string
                output = output.strftime(DATE_TIME_FORMAT)
            except Exception as e:
                log.error("Timezone conversion not possible. Exception: {0}".format(e.message))
    else:
        return datetime_obj.strftime(DATE_TIME_FORMAT)

    return output


def indexed_query_set(query_set, indexes, values, is_raw=False):
    """
    # since query sets are not evaluated by default, we will evaluate the query set
    # index the query set on a few attributes
    # and return a disctionary if indexes
    :param is_raw:
    :param query_set: the original query set and subclasses : Query set must be complete and must be having a db
    :param indexes: required indexes for indexing the query set
    :param values: required values of the query set
    :return: indexed results
    """
    if set(indexes).issubset(values):
        indexed_result = dict()
        if not is_raw:
            if query_set.exists():
                if query_set.values(*indexes).exists():  # check if the desired indexes exists
                    for qs in query_set.values(*values):  # check if the desired values exists
                        index = tuple(qs[x] for x in indexes)
                        if index not in indexed_result:
                            indexed_result[index] = list()
                        indexed_result[index].append(qs)
            else:
                return False

        else:
            # we have raw query results which are
            # list of dictionatry
            if len(query_set):
                for qs in query_set:
                    index = tuple(qs[x] for x in indexes)
                    if index not in indexed_result:
                        indexed_result[index] = list()
                    indexed_result[index].append(qs)
            else:
                return False
        return indexed_result
    else:
        return False


def check_item_is_list(items):
    """

    :param items: any item to check
    :return: list of items
    """
    if type(items) == type(list()):
        return items
    elif type(items) == type(set()):
        return list(items)
    else:
        return [items]


def is_lat_long_in_state(latitude, longitude, state):
    """

    :param latitude:
    :param longitude:
    :param state:
    :return: True
    """
    """
    if compare_geo:
        # commented because of goes package is not supported for python 2.7 on centos 6.5
        # check whether lat log lies in state co-ordinates or not
        if latitude and longitude and state:
            from device.models import StateGeoInfo

            try:
                project = partial(
                    pyproj.transform,
                    pyproj.Proj(init='epsg:4326'),
                    pyproj.Proj('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 \
                                +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs'))

                state_geo_info = StateGeoInfo.objects.filter(state_id=state)
                state_lat_longs = list()
                for geo_info in state_geo_info:
                    temp_lat_longs = list()
                    temp_lat_longs.append(geo_info.longitude)
                    temp_lat_longs.append(geo_info.latitude)
                    state_lat_longs.append(temp_lat_longs)

                poly = Polygon(tuple(state_lat_longs))
                point = Point(longitude, latitude)

                # Translate to spherical Mercator or Google projection
                poly_g = transform(project, poly)
                p1_g = transform(project, point)
                if not poly_g.contains(p1_g):
                    return False
                else:
                    return True
            except Exception as e:
                return False
    else:
        return False
    """
    return True


def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    :param signal_handler:
    Ref: http://stackoverflow.com/questions/15624817/have-loaddata-ignore-or-disable-post-save-signals
    """

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        if 'raw' in kwargs and kwargs['raw']:
            return
        signal_handler(*args, **kwargs)

    return wrapper


def logged_in_user_organizations(self_object):
    """
    If the user role is admin then append its descendants organization as well, otherwise not

    :param self_object:
    :params self_object:
    :return organization_list:
    """
    if self_object.request.user.is_superuser:
        return Organization.objects.all()

    logged_in_user = self_object.request.user.userprofile

    if logged_in_user.role.values_list('role_name', flat=True)[0] in ['admin', 'operator', 'viewer']:
        organizations = logged_in_user.organization.get_descendants(include_self=True)
    else:
        organizations = Organization.objects.filter(id=logged_in_user.organization.id)

    return organizations


def nocout_datatable_ordering(self_instance, qs, order_columns):
    """ 
     Get parameters from the request and prepare order by clause
    :param order_columns:
    :param self_instance:
    :param qs:
    """
    request = self_instance.request
    # Number of columns that are used in sorting
    try:
        i_sorting_cols = int(request.REQUEST.get('iSortingCols', 0))
    except Exception:
        i_sorting_cols = 0

    order = []

    for i in range(i_sorting_cols):
        # sorting column
        try:
            i_sort_col = int(request.REQUEST.get('iSortCol_%s' % i))
        except Exception:
            i_sort_col = 0
        # sorting order
        s_sort_dir = request.REQUEST.get('sSortDir_%s' % i)

        sdir = '-' if s_sort_dir == 'desc' else ''

        sortcol = order_columns[i_sort_col]
        if isinstance(sortcol, list):
            for sc in sortcol:
                order.append('%s%s' % (sdir, sc))
        else:
            order.append('%s%s' % (sdir, sortcol))
    if order:
        key_name = order[0][1:] if '-' in order[0] else order[0]
        # Try catch is added because in some cases 
        # we receive instead of queryset
        try:
            sorted_device_data = qs.order_by(*order)
        except Exception, e:
            try:
                sorted_device_data = sorted(
                    qs, 
                    key=itemgetter(key_name), 
                    reverse=True if '-' in order[0] else False
                )
            except Exception, e:
                sorted_device_data = qs
                log.info(e.message)
        return sorted_device_data
    return qs 


class HTMLTextExtractor(HTMLParser):
    """

    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.result = []

    def handle_data(self, d):
        """

        :param d:
        """
        self.result.append(d)

    def handle_charref(self, number):
        """

        :param number:
        """
        codepoint = int(number[1:], 16) if number[0] in (u'x', u'X') else int(number)
        self.result.append(unichr(codepoint))

    def handle_entityref(self, name):
        """

        :param name:
        """
        codepoint = htmlentitydefs.name2codepoint[name]
        self.result.append(unichr(codepoint))

    def get_text(self):
        """


        :return:
        """
        return u''.join(self.result)


def html_to_text(html):
    """

    :param html:
    :return:
    """
    s = HTMLTextExtractor()
    s.feed(html)
    return s.get_text()


@time_it()
def nocout_db_router(db='default', levels=0):
    """
    http://stackoverflow.com/questions/26608906/django-multiple-databases-fallback-to-master-if-slave-is-down
    defining utility to exatly choose a database to query from
    django routers are of no use
    we will pass in the machine name
    we will test the connection
    and we will return the results of the database to be used
    :param db: pass the name for the database
    :param levels: number of slaves available
    :return:the database to be queried on
    """
    db_slave_up = list()
    # can choose from master db as well
    db_slave_up.append(db)
    db_slave = db + "_slave"
    if levels and levels != -1:
        for x in range(1, levels):
            db_slave = db + "_slave_" + str(x)
            if test_connection_to_db(db_slave):
                db_slave_up.append(db_slave)
    elif levels == -1:
        return db
    else:
        if test_connection_to_db(db_slave):
            db_slave_up.append(db_slave)

    return random.choice(db_slave_up)


@time_it()
def nocout_query_results(query_set=None, using='default', levels=0):
    """

    :param query_set: query set to be executed
    :param using: the db alias
    :param levels: levels of slaves default = 0, that is one slave is present, -1 means no slave
    :return:
    """
    if query_set:
        # choose a random database : slave // master
        if levels == -1:
            return query_set.using(alias=using)
        else:
            db = nocout_db_router(db=using, levels=levels)
            return query_set.using(alias=db)
    return None


def fetch_ss_inventory(monitored_only=True, technology=None, device_name_list=None):
    """
    This function fetch SS inventory data except PTPBH SS.
    If any technology is given then fetch data for specific technology.
    """
    ss_query = get_inventory_ss_query(
        monitored_only=monitored_only,
        technology=technology,
        device_name_list=device_name_list
    )

    result_list = fetch_raw_result(ss_query)

    return create_specific_key_dict(
        result_list,
        'SSDEVICENAME'
    )


def fetch_ptpbh_ss_inventory(monitored_only=True, technology='P2P', device_name_list=None):
    """
    This function fetch PTP BH SS inventory data.
    If any technology is given then fetch data for specific technology.
    """
    ss_query = get_inventory_ss_query(
        monitored_only=monitored_only,
        technology=technology,
        device_name_list=device_name_list,
        is_ptpbh=True
    )

    result_list = fetch_raw_result(ss_query)

    return create_specific_key_dict(
        result_list,
        'SSDEVICENAME'
    )


def get_inventory_ss_query(monitored_only=True, technology=None, device_name_list=None, is_ptpbh=False):
    """
    This function return SQL query to get sub-station inventory 
    as per the given params
    """
    technology_condition = ''
    nms_device_condition = ''
    device_name_condition = ''
    circuit_type_condition = ''

    if monitored_only:
        nms_device_condition = ' AND device.is_added_to_nms = 1 '

    if technology:
        # Check that the given technology name is exists or not
        try:
            is_correct_technology = DeviceTechnology.objects.get(name=technology)
            technology_condition = ' AND technology.name = {0} '.format(technology)
        except Exception, e:
            technology_condition = ''

    if device_name_list and len(device_name_list):
        device_name_str = ', '.join(str(d_name) for d_name in device_name_list)
        device_name_condition = " device.device_name in (" + device_name_str + ") AND "

    if is_ptpbh:
        circuit_type_condition = " AND circuit.circuit_type LIKE '%backhaul%' "
    else:
        circuit_type_condition = " AND ( isnull(circuit.circuit_type) OR \
                                  circuit.circuit_type LIKE '%customer%' ) "

    ss_query = '''
        SELECT 
            IF(not isnull(bs.alias), bs.alias, 'NA') as BSALIAS,
            IF(not isnull(city.city_name), city.city_name, 'NA') as BSCITY,
            IF(not isnull(state.state_name), state.state_name, 'NA') as BSSTATE,
            bs.city_id as BSCITYID,
            bs.state_id as BSSTATEID,
            device_port.name as SECTOR_PORT,
            IF(
                not isnull(device_port.name),
                concat(
                    '(', upper(device_port.name), ') ', ss_info.SECTOR_SECTOR_ID
                ),
                ss_info.SECTOR_SECTOR_ID
            ) as SECTOR_PORT_SECTOR_ID,
            ss_info.*
        FROM (
            SELECT 
                sector.sector_id AS SECTOR_SECTOR_ID,
                sector.id AS SECTOR_ID,
                sector.sector_configured_on_port_id as sector_port_id,
                sector.base_station_id as BSID,
                sector_device.ip_address as SECTOR_CONF_ON_IP,
                sector_device.device_name as SECTOR_CONF_ON,
                sector_device.id as NEAR_DEVICE_ID,
                only_ss_info.*
            FROM (
                SELECT
                    circuit.sector_id AS SECT_ID,
                    circuit.circuit_id AS CCID,
                    circuit.id AS CID,
                    IF(circuit.qos_bandwidth, circuit.qos_bandwidth/1000, 'NA') AS CKT_QOS,
                    substation.alias AS SSALIAS,
                    substation.id AS SSID,
                    
                    customer.alias AS CUST,
                    customer.id AS CUSTID,

                    device.ip_address AS SSIP,
                    device.device_name AS SSDEVICENAME,
                    device.id AS DEVICE_ID,
                    device.id AS SS_DEVICE_ID,
                    
                    devicetype.name AS DEVICE_TYPE,
                    devicetype.id AS TYPEID,
                    
                    technology.name AS DEVICE_TECH,
                    technology.id AS TECHID
                FROM
                    inventory_circuit AS circuit
                LEFT JOIN (
                    inventory_substation AS substation,
                    inventory_customer AS customer,
                    device_device AS device,
                    device_devicetechnology AS technology,
                    device_devicetype AS devicetype
                )
                ON (
                    substation.id = circuit.sub_station_id
                    AND
                    customer.id = circuit.customer_id
                    AND
                    {2}
                    device.id = substation.device_id
                    AND
                    technology.id = device.device_technology
                    AND
                    devicetype.id = device.device_type
                    {0}
                )
                where 
                    device.is_deleted = 0
                    {1}
                    {3}
            ) as only_ss_info
            LEFT JOIN
                inventory_sector AS sector
            ON
                sector.id = only_ss_info.SECT_ID
            LEFT JOIN
                device_device AS sector_device
            ON
                sector_device.id = sector.sector_configured_on_id
        ) AS ss_info
        LEFT JOIN
            inventory_basestation AS bs
        ON
          bs.id = ss_info.BSID
        LEFT JOIN
            device_state AS state
        on 
            state.id = bs.state_id
        LEFT JOIN
            device_city AS city
        on 
            city.id = bs.city_id
        LEFT JOIN
            device_deviceport AS device_port
        ON
            device_port.id = ss_info.sector_port_id
        and
            not isnull(ss_info.sector_port_id);
        '''.format(
            technology_condition,
            nms_device_condition,
            device_name_condition,
            circuit_type_condition
        )

    return ss_query


def fetch_sector_inventory(monitored_only=True, technology=None, device_name_list=None, grouped_query=True):
    """
    This function fetch all the Sector inventory data.
    If any technology is given then fetch data for specific technology.
    """
    # Get the sector query as per the params
    sector_query = get_inventory_sector_query(
        monitored_only=monitored_only,
        technology=technology,
        device_name_list=device_name_list,
        grouped_query=grouped_query
    )

    result_list = fetch_raw_result(sector_query)

    return create_specific_key_dict(
        result_list,
        'SECTOR_CONF_ON_NAME'
    )


def fetch_dr_sector_inventory(monitored_only=True, technology='WiMAX', device_name_list=None, grouped_query=True):
    """
    This function fetch all the DR Sector inventory data.
    If any technology is given then fetch data for specific technology.
    """
    # Get the sector query as per the params
    dr_sector_query = get_inventory_sector_query(
        monitored_only=monitored_only,
        technology=technology,
        device_name_list=device_name_list,
        is_dr=True,
        grouped_query=grouped_query
    )

    result_list = fetch_raw_result(dr_sector_query)

    return create_specific_key_dict(
        result_list,
        'SECTOR_CONF_ON_NAME'
    )


def fetch_mrc_sector_inventory(monitored_only=True, technology='WiMAX', device_name_list=None, grouped_query=True):
    """
    This function fetch all the MRC enabled Sector inventory data.
    If any technology is given then fetch data for specific technology.
    """
    # Get the sector query as per the params
    mrc_sector_query = get_inventory_sector_query(
        monitored_only=monitored_only,
        technology=technology,
        device_name_list=device_name_list,
        is_mrc=True,
        grouped_query=grouped_query
    )

    result_list = fetch_raw_result(mrc_sector_query)

    return create_specific_key_dict(
        result_list,
        'SECTOR_CONF_ON_NAME'
    )


def get_inventory_sector_query(
    monitored_only=True,
    technology=None,
    device_name_list=None,
    is_dr=False,
    is_mrc=False,
    grouped_query=True
):
    """
    This function returns query to fetch sectors inventory
    """
    technology_condition = ""
    nms_device_condition = ""
    device_name_condition = ""
    dr_sector_id_prefix = " "
    dr_device_condition = ""
    device_condition = " device.id = sector.sector_configured_on_id "
    grouping_condition = ""
    concat_values = ""

    if monitored_only:
        nms_device_condition = ' AND device.is_added_to_nms = 1 '

    if technology:
        # Check that the given technology name is exists or not
        try:
            is_correct_technology = DeviceTechnology.objects.get(name=technology)
            technology_condition = ' AND technology.name = {0} '.format(technology)
        except Exception, e:
            technology_condition = ''

    if device_name_list and len(device_name_list):
        device_name_str = ', '.join(str(d_name) for d_name in device_name_list)
        device_name_condition = " device.device_name in (" + device_name_str + ") AND "

    if is_dr:
        dr_sector_id_prefix = "DR: "
        dr_device_condition = " AND sector.dr_site = 'yes' "
        device_condition = " device.id = sector.dr_configured_on_id "

    if is_mrc:
        dr_sector_id_prefix = "MRC: "
        dr_device_condition = " AND sector.mrc = 'yes' "

    if grouped_query:
        grouping_condition = " GROUP BY sector_info.SECTOR_CONF_ON_IP "
        concat_values = " CONCAT(' {0} ', group_concat(IF( \
                            not isnull(device_port.name), \
                            concat( \
                                '(', upper(device_port.name), ') ', sector_info.SECTOR_SECTOR_ID \
                            ), \
                            sector_info.SECTOR_SECTOR_ID \
                        ) SEPARATOR ' ')) \
                        as SECTOR_PORT_SECTOR_ID, ".format(dr_sector_id_prefix)
    else:
        grouping_condition = ''
        concat_values = " sector_info.SECTOR_SECTOR_ID AS SECTOR_PORT_SECTOR_ID , \
                         ".format(dr_sector_id_prefix)

    sector_query = '''
        SELECT 
            IF(not isnull(bs.alias), bs.alias, 'NA') as BSALIAS,
            IF(not isnull(city.city_name), city.city_name, 'NA') as BSCITY,
            IF(not isnull(state.state_name), state.state_name, 'NA') as BSSTATE,
            device_port.name as SECTOR_PORT,
            {3}
            bs.city_id as BSCITYID,
            bs.state_id as BSSTATEID,
            IF(not isnull(freq.value), freq.value, 'NA') AS FREQUENCY,
            sector_info.* 
        from
            (
                select
                    device.ip_address as SECTOR_CONF_ON_IP,
                    devicetype.name as DEVICE_TYPE,
                    
                    sector.base_station_id AS BSID,
                    sector.sector_id as SECTOR_SECTOR_ID,
                    sector.id as SECT_ID,
                    sector.base_station_id as SECTOR_BS_ID,
                    sector.planned_frequency as SECTOR_PLANNED_FREQUENCY,
                    sector.sector_configured_on_port_id as sector_port_id,
                    sector.frequency_id AS FREQ_ID,

                    technology.name as DEVICE_TECH,
                    technology.id as TECHID,
                    devicetype.id as TYPEID,

                    device.id as SECTOR_CONF_ON_ID,
                    device.id AS DEVICE_ID,
                    device.device_name as SECTOR_CONF_ON_NAME

                from 
                    inventory_sector as sector
                join (
                    device_device as device,
                    device_devicetechnology as technology,
                    device_devicetype as devicetype
                )
                on (
                    {5}
                    AND
                    {2}
                    technology.id = device.device_technology
                    {0}
                    AND
                    devicetype.id = device.device_type
                )
                where 
                    not isnull(sector.sector_configured_on_id)
                    AND
                    device.is_deleted = 0
                    {1}
                    {4}
            ) as sector_info
        LEFT JOIN
            device_devicefrequency as freq
        ON
            freq.id = sector_info.FREQ_ID
        LEFT JOIN
            inventory_basestation as bs
        ON
            bs.id = sector_info.BSID
        LEFT JOIN
            device_state AS state
        on 
            state.id = bs.state_id
        LEFT JOIN
            device_city AS city
        on 
            city.id = bs.city_id
        LEFT JOIN
            device_deviceport AS device_port
        ON
            device_port.id = sector_info.sector_port_id
        and
            not isnull(sector_info.sector_port_id)
        {6};

        '''.format(
            technology_condition,
            nms_device_condition,
            device_name_condition,
            concat_values,
            dr_device_condition,
            device_condition,
            grouping_condition
        )

    return sector_query


def fetch_ptp_sector_inventory(monitored_only=True, device_name_list=None):
    """

    """
    ptp_sector_query = get_ptp_sector_query(
        device_name_list=device_name_list
    )
    result_list = fetch_raw_result(ptp_sector_query)

    return create_specific_key_dict(
        result_list,
        'SECTOR_CONF_ON_NAME'
    )


def fetch_ptpbh_sector_inventory(monitored_only=True, device_name_list=None):
    """
    This function returns PTPBH sectors inventory.
    """
    ptpbh_sector_query = get_ptp_sector_query(
        device_name_list=device_name_list,
        is_ptpbh=True
    )
    result_list = fetch_raw_result(ptpbh_sector_query)

    return create_specific_key_dict(
        result_list,
        'SECTOR_CONF_ON_NAME'
    )


def get_ptp_sector_query(monitored_only=True, device_name_list=None, is_ptpbh=False):
    """
    This function return the SQL query to get PTP or PTP BH sectors
    """

    nms_device_condition = ''
    device_name_condition = ''
    ptp_condition = ''

    if monitored_only:
        nms_device_condition = ' AND device.is_added_to_nms = 1 '

    if device_name_list and len(device_name_list):
        device_name_str = ', '.join(str(d_name) for d_name in device_name_list)
        device_name_condition = " device.device_name in (" + device_name_str + ") AND "

    if is_ptpbh:
        ptp_condition = " circuit.circuit_type LIKE '%backhaul%' AND "
    else:
        ptp_condition = " circuit.circuit_type NOT LIKE '%backhaul%' AND "

    ptp_sector_query = '''
        SELECT 
            IF(not isnull(bs.alias), bs.alias, 'NA') AS BSALIAS,
            IF(not isnull(bs.id), bs.id, '0') AS BSID,
            IF(not isnull(city.city_name), city.city_name, 'NA') AS BSCITY,
            IF(not isnull(state.state_name), state.state_name, 'NA') AS BSSTATE,
            IF(not isnull(freq.value), freq.value, 'NA') AS FREQUENCY,
            bs.city_id AS BSCITYID,
            bs.state_id AS BSSTATEID,
            sector_info.* 
        FROM
            (
                SELECT
                    IF(not isnull(circuit.circuit_id), circuit.circuit_id, 'NA') AS CCID,
                    if(not isnull(customer.alias), customer.alias, 'NA') AS CUST,
                    customer.id AS CUSTID,
                    circuit.id AS CID,
                    IF(circuit.qos_bandwidth, circuit.qos_bandwidth/1000, 'NA') AS CKT_QOS,
                    sector_device_info.*
                FROM(
                        SELECT
                            device.ip_address AS SECTOR_CONF_ON_IP,
                            devicetype.name AS DEVICE_TYPE,
                            sector.id AS SECT_ID,
                            sector.base_station_id AS BSID,
                            sector.sector_id AS SECTOR_SECTOR_ID,
                            sector.id AS SECTOR_ID,
                            sector.frequency_id AS FREQ_ID,
                            sector.base_station_id AS SECTOR_BS_ID,
                            sector.planned_frequency AS SECTOR_PLANNED_FREQUENCY,
                            sector.sector_configured_on_port_id AS sector_port_id,

                            technology.name AS DEVICE_TECH,
                            technology.id AS TECHID,
                            devicetype.id AS TYPEID,

                            device.id AS NEAR_DEVICE_ID,
                            device.id AS DEVICE_ID,
                            device.device_name AS SECTOR_CONF_ON_NAME
                        FROM 
                            inventory_sector AS sector
                        JOIN (
                            device_device AS device,
                            device_devicetechnology AS technology,
                            device_devicetype AS devicetype
                        )
                        ON (
                            device.id = sector.sector_configured_on_id
                        AND
                            {1}
                            technology.id = device.device_technology
                        AND
                            devicetype.id = device.device_type
                        )
                        where 
                            device.is_deleted = 0
                            {0}
                ) as sector_device_info
                LEFT JOIN
                    inventory_circuit AS circuit
                ON
                    {2}
                    circuit.sector_id = sector_device_info.SECT_ID
                LEFT JOIN
                    inventory_customer AS customer
                ON
                    customer.id = circuit.customer_id
            ) as sector_info
        LEFT JOIN
            device_devicefrequency as freq
        ON
            freq.id = sector_info.FREQ_ID
        LEFT JOIN
            inventory_basestation AS bs
        ON
            bs.id = sector_info.BSID
        LEFT JOIN
            device_state AS state
        ON 
            state.id = bs.state_id
        LEFT JOIN
            device_city AS city
        ON 
            city.id = bs.city_id
        GROUP BY 
            sector_info.SECTOR_CONF_ON_IP;
    '''.format(
        nms_device_condition,
        device_name_condition,
        ptp_condition
    )

    return ptp_sector_query


def fetch_backhaul_inventory(monitored_only=True, device_name_list=None, type_rf='backhaul', grouped_query=True):
    """
    This funtion return Backhaul inventory
    """
    bh_query = get_bh_other_query(
        device_name_list=device_name_list,
        type_rf=type_rf,
        grouped_query=grouped_query
    )

    result_list = fetch_raw_result(bh_query)

    return create_specific_key_dict(
        result_list,
        'BHDEVICENAME'
    )


def get_bh_other_query(monitored_only=True, device_name_list=None, type_rf='backhaul', grouped_query=True):
    """
    This function return SQL query to fetch BH or Other devices inventory
    """
    nms_device_condition = ""
    device_name_condition = ""
    is_bh_condition = " bh.bh_configured_on_id = device.id AND "
    grouping_condition = " GROUP BY bh_info.BHIP "

    if monitored_only:
        nms_device_condition = ' AND device.is_added_to_nms = 1 '

    if device_name_list and len(device_name_list):
        device_name_str = ', '.join(str(d_name) for d_name in device_name_list)
        device_name_condition = " device.device_name in (" + device_name_str + ") AND "

    if type_rf != 'backhaul':
        is_bh_condition = " ( bh.pop_id = device.id OR \
                            bh.aggregator_id = device.id OR \
                            bh.bh_switch_id = device.id ) AND \
                        not isnull(bh.bh_configured_on_id) AND "

    if not grouped_query:
        grouping_condition = ""


    bh_query = '''
        SELECT 
            IF(not isnull(bs.alias), bs.alias , 'NA') AS BSALIAS,
            IF(not isnull(bs.id), bs.id , '0') AS BSID,
            IF(not isnull(bs.bh_capacity), bs.bh_capacity , 'NA') AS BHCAPACITY,
            IF(not isnull(bs.bh_port_name), bs.bh_port_name , 'NA') AS BHPORT,
            IF(not isnull(bs.city_id), bs.city_id , '0') AS BSCITYID,
            IF(not isnull(bs.state_id), bs.state_id , '0') AS BSSTATEID,
            IF(not isnull(city.city_name), city.city_name , 'NA') AS BSCITY,
            IF(not isnull(state.state_name), state.state_name , 'NA') AS BSSTATE,
            bh_info.* 
        FROM 
            (
                select
                    device.ip_address AS BHIP,
                    technology.name AS DEVICE_TECH,
                    devicetype.name AS DEVICE_TYPE,
                        
                    bh.id AS BHID,
                    bh.bh_connectivity AS BH_CONNECTIVITY,

                    technology.id AS TECHID,
                    devicetype.id AS TYPEID,
                    device.id AS DEVICE_ID,
                    device.device_name AS BHDEVICENAME
                from
                    inventory_backhaul AS bh
                JOIN (
                    device_device AS device,
                    device_devicetechnology AS technology,
                    device_devicetype AS devicetype
                )
                on (
                    {2}
                    {1}
                    device.device_type = devicetype.id
                    AND
                    device.device_technology = technology.id
                )
                WHERE
                    device.is_deleted = 0
                    {0}
            ) AS bh_info
        LEFT JOIN
            inventory_basestation AS bs
        ON
            bs.backhaul_id = bh_info.BHID
        LEFT JOIN
            device_state AS state
        ON
            state.id = bs.state_id
        LEFT JOIN
            device_city AS city
        ON
            city.id = bs.city_id
        {3};
    '''.format(
        nms_device_condition,
        device_name_condition,
        is_bh_condition,
        grouping_condition
    )

    return bh_query


def create_specific_key_dict(data_list, key_str):
    """
    This function create dict from list with key 
    as per given 'key_str' param
    """

    if not (data_list or len(data_list)):
        return data_list

    data_dict = dict()

    for data in data_list:
        try:
            dict_key = data.get(key_str)

            if dict_key and dict_key not in data_dict:
                data_dict[dict_key] = list()

            data_dict[dict_key].append(data)

        except Exception, e:
            continue

    return data_dict

