# -*- coding: utf-8 -*-
import json, logging, datetime, xlwt, csv
from django.db.models import Count
from django.db.models.query import ValuesQuerySet
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.views.generic import ListView, View
from django.template import RequestContext
from django_datatables_view.base_datatable_view import BaseDatatableView
from device.models import Device, City, State, DeviceTechnology, DeviceType
from inventory.models import BaseStation, Sector, SubStation, Circuit, Backhaul
from performance.models import PerformanceNetwork, EventNetwork, EventService, NetworkStatus

from performance.views import ptp_device_circuit_backhaul, \
    organization_customer_devices, \
    organization_network_devices, \
    organization_backhaul_devices, \
    indexed_gis_devices, \
    combined_indexed_gis_devices,\
    indexed_polled_results,\
    filter_devices,\
    prepare_machines,\
    prepare_gis_devices

from django.utils.dateformat import format
from django.db.models import Q

from django.conf import settings
from nocout.settings import P2P, WiMAX, PMP, DEBUG

from nocout.utils.util import fetch_raw_result, dict_fetchall, \
    format_value, cache_for, \
    cached_all_gis_inventory,query_all_gis_inventory

# going deep with sql cursor to fetch the db results. as the RAW query executes everythong it is recursively used
from django.db import connections

# for raw query optmisation we will use ceil
import math

# sort the list of dictionaries
# http://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python
from operator import itemgetter

from multiprocessing import Process, Queue

logger = logging.getLogger(__name__)


def getCustomerAlertDetail(request):
    """
    get request to render customer detail list
    :params request object:
    :return Http Response Object::

    """
    datatable_headers = [
        {'mData': 'severity', 'sTitle': '', 'sWidth': '40px', 'bSortable': True},
        {'mData': 'ip_address', 'sTitle': 'IP', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True},
        {'mData': 'device_type', 'sTitle': 'Device type', 'sWidth': 'auto', 'sClass': 'hidden-xs',
        'bSortable': True},
        {'mData': 'bs_name', 'sTitle': 'Base Station', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True},
        {'mData': 'circuit_id', 'sTitle': 'Circuit ID', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True},
        {'mData': 'sector_id', 'sTitle': 'Sector ID', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True},
        {'mData': 'city', 'sTitle': 'City', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True},
        {'mData': 'state', 'sTitle': 'State', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True},
        {'mData': 'data_source_name', 'sTitle': 'Data Source Name', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True},
        {'mData': 'current_value', 'sTitle': 'Value', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True, "sSortDataType": "dom-text", "sType": "numeric" },
        {'mData': 'sys_timestamp', 'sTitle': 'Timestamp', 'sWidth': 'auto', 'bSortable': True},
        {'mData': 'customer_name', 'sTitle': 'Customer Name', 'sWidth': 'auto', 'bSortable': True},
        {'mData': 'action', 'sTitle': 'Action', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': False},
        ]

    context = {'datatable_headers': json.dumps(datatable_headers)}
    return render(request, 'alert_center/customer_alert_details_list.html', context)


class GetCustomerAlertDetail(BaseDatatableView):
    """
    Generic Class Based View for the Alert Center Customer Listing Tables.
    """
    model = EventNetwork
    columns = ['device_name', 'device_type', 'machine_name', 'site_name', 'ip_address', 'severity',
               'current_value', 'sys_timestamp', 'description', 'customer_name']
    order_columns = ['device_name', 'device_type', 'machine_name', 'site_name', 'ip_address', 'severity',
                     'current_value', 'sys_timestamp', 'description', 'customer_name']

    def filter_queryset(self, qs):
        """
        The filtering of the queryset with respect to the search keyword entered.

        :param qs:
        :return result_list:

        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            result_list = list()
            for dictionary in qs:
                for key in dictionary.keys():
                    if sSearch.lower() in str(dictionary[key]).lower():
                        result_list.append(dictionary)

            return result_list

        return qs

    def get_initial_queryset(self):
        """
        Preparing  Initial Queryset for the for rendering the data table.

        """
        if not self.model:
            raise NotImplementedError("Need to provide a model or implement get_initial_queryset!")

        logged_in_user = self.request.user.userprofile

        organization_devices = filter_devices(logged_in_user, self.request.GET.get('data_tab'), page_type="customer")

        required_data_columns = ["id",
                                 "ip_address",
                                 "service_name",
                                 "device_name",
                                 "data_source",
                                 "severity",
                                 "current_value",
                                 "max_value",
                                 "sys_timestamp",
                                 "age"
                                 # "description"
                                ]
        # Unique machine from the sector_configured_on_devices
        unique_machine_list = { device['machine_name']: True for device in organization_devices }.keys()

        machine_dict = dict()
        # Creating the machine as a key and device_name as a list for that machine.
        for machine in unique_machine_list:
            machine_dict[machine] = [ device['device_name'] for device in organization_devices if
                                      device['machine_name'] == machine ]

        #Fetching the data for the device w.r.t to their machine.
        device_list, performance_data, device_data = list(), list(), list()
        for machine, machine_device_list in machine_dict.items():
            data_sources_list = []
            device_data += self.collective_query_result(
                machine=machine,
                table_name="performance_servicestatus",
                devices=machine_device_list,
                data_sources=data_sources_list,
                columns=required_data_columns)

        if device_data:
            # sorted_device_data = sorted(device_data, key=itemgetter('sys_timestamp'), reverse=True)
            # return sorted_device_data
            return device_data

        return device_list


    def collective_query_result(self, machine, table_name, devices, data_sources, columns):

        performance_data = list()
        performance_data = raw_prepare_result(performance_data=performance_data,
                                              machine=machine,
                                              table_name=table_name,
                                              devices=devices,
                                              data_sources=data_sources,
                                              columns=columns)


        device_list = []

        # now considering all the cases. we should also consider this that there is a normal case
        # when all the devices are substations
        # and another case where we are getting the sector devices as well
        # and those sector devices are as said PTP !!!
        # we should start with getting the
        # device and substation

        device_list = prepare_raw_alert_results(device_list, performance_data)

        return device_list


    def prepare_results(self, qs):
        """
        Preparing the final result after fetching from the data base to render on the data table.

        :param qs:
        :return queryset
        """

        if qs:
            qs = [{key: val if val else "" for key, val in dct.items()} for dct in qs]

            service_tab_name = 'service'
            for dct in qs:
                device_object = Device.objects.get(device_name=dct['device_name'])
                device_id = device_object.id

                dct.update(action=''
                    '<a href="/alert_center/customer/device/{0}/service_tab/{1}/" title="Device Alerts">'
                    '<i class="fa fa-warning text-warning"></i>'
                    '</a>'
                    '<a href="/performance/customer_live/{0}/" title="Device Performance">'
                    '<i class="fa fa-bar-chart-o text-info"></i>'
                    '</a>'
                    '<a href="/device/{0}" title="Device Inventory">'
                    '<i class="fa fa-dropbox text-muted"></i>'
                    '</a>'.format(device_id, service_tab_name))


        return common_prepare_results(qs)


    def get_context_data(self, *args, **kwargs):
        """
        The maine function call to fetch, search, ordering , prepare and display the data on the data table.

        """

        request = self.request
        self.initialize(*args, **kwargs)

        qs = self.get_initial_queryset()

        # number of records before filtering
        total_records = len(qs)

        qs = self.filter_queryset(qs)

        # number of records after filtering
        total_display_records = len(qs)

        # qs = self.ordering(qs)
        # qs = self.paging(qs)
        # if the qs is empty then JSON is unable to serialize the empty ValuesQuerySet.Therefore changing its type to list.
        if not qs and isinstance(qs, ValuesQuerySet):
            qs = list(qs)

        # prepare output data
        aaData = self.prepare_results(qs)
        ret = {
               'sEcho': int(request.REQUEST.get('sEcho', 0)),
               'iTotalRecords': total_records,
               'iTotalDisplayRecords': total_display_records,
               'aaData': aaData
              }
        return ret


def getNetworkAlertDetail(request):
    """
    get request to render network detail list
    :params request object:
    :return Http Response Object:
    """
    datatable_headers = [
        {'mData': 'severity', 'sTitle': '', 'sWidth': '40px', 'bSortable': True},
        {'mData': 'ip_address', 'sTitle': 'IP', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True},
        {'mData': 'device_type', 'sTitle': 'Device Type', 'sWidth': 'auto', 'sClass': 'hidden-xs',
        'bSortable': True},
        {'mData': 'bs_name', 'sTitle': 'Base Station', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True},
        {'mData': 'city', 'sTitle': 'City', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True},
        {'mData': 'state', 'sTitle': 'State', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True},
        {'mData': 'data_source_name', 'sTitle': 'Data Source Name', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True},
        {'mData': 'current_value', 'sTitle': 'Value', 'sWidth': 'auto', 'sClass': 'hidden-xs',
         'bSortable': True, "sSortDataType": "dom-text", "sType": "numeric" },
        {'mData': 'sys_timestamp', 'sTitle': 'Timestamp', 'sWidth': 'auto', 'bSortable': True},
        {'mData': 'action', 'sTitle': 'Action', 'sWidth': 'auto', 'bSortable': True},
        ]

    context = {'datatable_headers': json.dumps(datatable_headers)}
    return render(request, 'alert_center/network_alert_details_list.html', context)


class GetNetworkAlertDetail(BaseDatatableView):
    """
    Generic Class Based View for the Alert Center Network  Detail Listing Tables.

    """
    model = EventNetwork
    columns = ['device_name', 'device_type', 'machine_name', 'site_name', 'ip_address', 'severity',
               'current_value', 'sys_time', 'sys_date', 'description']
    order_columns = ['device_name', 'device_type', 'machine_name', 'site_name', 'ip_address', 'severity',
                     'current_value', 'sys_time', 'sys_date', 'description']

    def filter_queryset(self, qs):

        """
        The filtering of the queryset with respect to the search keyword entered.

        :param qs:
        :return result_list:
        """

        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            result_list = list()
            for dictionary in qs:
                for key in dictionary.keys():
                    if sSearch.lower() in str(dictionary[key]).lower():
                        result_list.append(dictionary)
                        break
            return result_list
        return qs

    def get_initial_queryset(self):
        """
        Preparing  Initial Queryset for the for rendering the data table.

        """
        if not self.model:
            raise NotImplementedError("Need to provide a model or implement get_initial_queryset!")

        logged_in_user = self.request.user.userprofile

        if logged_in_user.role.values_list('role_name', flat=True)[0] == 'admin':
            organizations = list(logged_in_user.organization.get_descendants(include_self=True))
        else:
            organizations = [logged_in_user.organization]
        sector_configured_on_devices_ids = list()
        #here we would have to get the TAB wise content
        # we need to check the tabs
        # we need to check the data requested
        tab_id = None
        if self.request.GET.get("data_source"):
            tab_id = self.request.GET.get("data_source")
        else:
            return []

        sector_configured_on_devices = []

        if tab_id:
            device_list = []
            if tab_id == "P2P":
                technology = int(P2P.ID)
                #need to add device with Circuit Type as : Backhaul
                # (@TODO: make this a dropdown menu item and must for the user)
                #INVALID :::: for technology = PTP and Circuit Type as Backhaul get the Device BH Configured On ::: INVALID
                #VALID :::: confusion HERE. What we want is that CIRCUIT TYPE BACKHAUL's both SS and BS elements should
                #be visible on network alert center ::: VALID
            elif tab_id == "WiMAX":
                technology = int(WiMAX.ID)
            elif tab_id == "PMP":
                technology = int(PMP.ID)
            else:
                return []

            device_list = organization_network_devices(organizations, technology=technology)
            sector_configured_on_devices = [
                                {'device_name': device.device_name, 'machine__name': device.machine.name}
                                for device in device_list
            ]
        else:
            return []


        device_list, performance_data, data_sources_list = list(), list(), list()

        required_data_columns = ["id",
                                 "ip_address",
                                 "service_name",
                                 "device_name",
                                 "data_source",
                                 "severity",
                                 "current_value",
                                 "max_value",
                                 "sys_timestamp",
                                 "age"
                                 # "description"
                                ]

        # Unique machine from the sector_configured_on_devices
        unique_device_machine_list = {device['machine__name']: True for device in sector_configured_on_devices}.keys()

        machine_dict, device_data = dict(), list()
        # Creating the machine as a key and device_name as a list for that machine.

        for machine in unique_device_machine_list:
            machine_dict[machine] = [device['device_name']
                                     for device in sector_configured_on_devices
                                     if device['machine__name'] == machine]

        #Fetching the data for the device w.r.t to their machine.
        for machine, machine_device_list in machine_dict.items():

            # data_sources_list = ['rta', 'pl']
            #
            # device_data += self.collective_query_result(
            #     machine = machine,
            #     table_name = "performance_networkstatus",
            #     devices = machine_device_list,
            #     data_sources = data_sources_list,
            #     columns = required_data_columns
            # )

            data_sources_list = []
            device_data += self.collective_query_result(
                machine = machine,
                table_name = "performance_servicestatus",
                devices = machine_device_list,
                data_sources = data_sources_list,
                columns = required_data_columns
            )

        if device_data:
            # sorted_device_data = sorted(device_data, key=itemgetter('sys_timestamp'), reverse=True)
            # return sorted_device_data
            return device_data

        return device_list

    def collective_query_result(self, machine, table_name, devices, data_sources, columns):

        performance_data = list()
        performance_data = raw_prepare_result(performance_data=performance_data,
                                              machine=machine,
                                              table_name=table_name,
                                              devices=devices,
                                              data_sources=data_sources,
                                              columns=columns)


        device_list = []

        # now considering all the cases. we should also consider this that there is a normal case
        # when all the devices are substations
        # and another case where we are getting the sector devices as well
        # and those sector devices are as said PTP !!!
        # we should start with getting the
        # device and substation

        device_list = prepare_raw_alert_results(device_list, performance_data)

        return device_list

    def prepare_results(self, qs):
        """
        Preparing the final result after fetching from the data base to render on the data table.

        :param qs:
        :return queryset.
        """

        if qs:
            qs = [{key: val if val else "" for key, val in dct.items()} for dct in qs]
            service_tab_name = 'service'
            for dct in qs:
                device_id = Device.objects.get(device_name=dct['device_name']).id
                dct.update(action='<a href="/alert_center/network/device/{0}/service_tab/{1}/" title="Device Alerts"><i class="fa fa-warning text-warning"></i></a>\
                                   <a href="/performance/network_live/{0}/" title="Device Performance"><i class="fa fa-bar-chart-o text-info"></i></a>\
                                   <a href="/device/{0}" title="Device Inventory"><i class="fa fa-dropbox text-muted"></i></a>'.format(device_id,
                                                                                                              service_tab_name))

        return common_prepare_results(qs)

    def get_context_data(self, *args, **kwargs):
        """
        The maine function call to fetch, search, prepare and display the data on the data table.

        """

        request = self.request
        self.initialize(*args, **kwargs)

        qs = self.get_initial_queryset()

        # number of records before filtering
        total_records = len(qs)

        qs = self.filter_queryset(qs)

        # number of records after filtering
        total_display_records = len(qs)

        # qs = self.ordering(qs)
        # qs = self.paging(qs)  # Removing pagination as of now to render all the data at once.
        # if the qs is empty then JSON is unable to serialize the empty ValuesQuerySet.Therefore changing its type to list.
        if not qs and isinstance(qs, ValuesQuerySet):
            qs = list(qs)

        # prepare output data
        aaData = self.prepare_results(qs)
        ret = {'sEcho': int(request.REQUEST.get('sEcho', 0)),
               'iTotalRecords': total_records,
               'iTotalDisplayRecords': total_display_records,
               'aaData': aaData
        }
        return ret


# **************************************** Latency *********************************************
class AlertCenterListing(ListView):
    """
    Class Based View to render Alert Center Network Listing page with latency, packet drop
    down and service impact alert tabs.

    """
    model = EventNetwork
    template_name = 'alert_center/alerts_list.html'


    def get_context_data(self, **kwargs):
        """
        Preparing the Context Variable required in the template rendering.

        """

        context = super(AlertCenterListing, self).get_context_data(**kwargs)

        page_type = self.kwargs.get('page_type')

        data_source=self.kwargs.get('data_source')

        data_source_title = "Latency Avg (ms) " \
                            if data_source == "latency" \
                            else ("value".title() if data_source in ["service"] else "packet drop (%)".title())

        data_tab=self.kwargs.get('data_tab')

        datatable_headers = [
            {'mData': 'severity', 'sTitle': '', 'sWidth': '40px', 'bSortable': True},
            {'mData': 'ip_address', 'sTitle': 'IP', 'sWidth': 'auto', 'sClass': 'hidden-xs', 'bSortable': True},
            # {'mData': 'device_technology', 'sTitle': 'Tech', 'sWidth': 'auto', 'sClass': 'hidden-xs',
            #  'bSortable': True},
            {'mData': 'device_type', 'sTitle': 'Type', 'sWidth': 'auto', 'sClass': 'hidden-xs',
             'bSortable': True},
            # {'mData': 'sub_station', 'sTitle': 'Sub Station', 'sWidth': 'auto', 'sClass': 'hidden-xs',
            #  'bSortable': True},
            {'mData': 'city', 'sTitle': 'City', 'sWidth': 'auto', 'sClass': 'hidden-xs',
             'bSortable': True},
            {'mData': 'state', 'sTitle': 'State', 'sWidth': 'auto', 'sClass': 'hidden-xs',
             'bSortable': True},
            {'mData': 'bs_name', 'sTitle': 'Base Station', 'sWidth': 'auto', 'sClass': 'hidden-xs',
             'bSortable': True},
            ]
        if data_tab == 'P2P' or data_tab is None:
            datatable_headers += [
                {'mData': 'circuit_id',
                'sTitle': 'Circuit ID',
                'sWidth': 'auto',
                'sClass': 'hidden-xs',
                'bSortable': True
                },
            ]

        if data_tab != 'P2P' or data_tab is not None:
            datatable_headers += [
                {'mData': 'sector_id',
                'sTitle': 'Sector ID',
                'sWidth': 'auto',
                'sClass': 'hidden-xs',
                'bSortable': True
                },
            ]

        if page_type == 'customer' or data_tab == 'P2P' or data_tab is None:
            datatable_headers += [
                {
                    'mData': 'customer_name',
                    'sTitle': 'Customer Name',
                    'sWidth': 'auto',
                    'bSortable': True
                },
            ]

        if data_source == 'service':
            datatable_headers += [
            {'mData': 'data_source_name',
             'sTitle': 'Data Source',
             'sWidth': 'auto',
             'sClass': 'hidden-xs',
             'bSortable': True }
            ]

        datatable_headers += [
            {'mData': 'current_value',
             'sTitle': '{0}'.format(data_source_title),
             'sWidth': 'auto',
             'sClass': 'hidden-xs',
             'bSortable': True, "sSortDataType": "dom-text", "sType": "numeric" },
        ]

        if data_source == "latency":
            datatable_headers += [
                {
                    'mData': 'max_value',
                    'sTitle': 'Latency Max (ms)',
                    'sWidth': 'auto',
                    'sClass': 'hidden-xs',
                    'bSortable': True,
                    "sSortDataType": "dom-text",
                    "sType": "numeric"
                }
            ]
        datatable_headers += [
            {'mData': 'sys_timestamp', 'sTitle': 'Timestamp', 'sWidth': 'auto', 'bSortable': True},
            {'mData': 'age', 'sTitle': 'Age', 'sWidth': 'auto', 'bSortable': True},
            {'mData': 'action', 'sTitle': 'Action', 'sWidth': 'auto', 'bSortable': True},
            ]

        context['datatable_headers'] = json.dumps(datatable_headers)
        context['data_source'] = " ".join(self.kwargs['data_source'].split('_')).title()
        context['page_type'] = page_type
        return context


class AlertListingTable(BaseDatatableView):
    """
    Generic Class Based View for the Alert Center Network Listing Tables.

    """
    is_polled = False
    model = EventNetwork
    columns = ['device_name', 'device_type', 'machine_name', 'site_name', 'ip_address', 'severity',
               'current_value', 'max_value', 'sys_timestamp', 'description']
    order_columns = ['device_name', 'device_type', 'machine_name', 'site_name', 'ip_address', 'severity',
                     'current_value', 'max_value', 'sys_timestamp', 'description']

    polled_columns = ["id",
                      "ip_address",
                      "data_source",
                      "device_name",
                      "severity",
                      "current_value",
                      "max_value",
                      "sys_timestamp",
                      "age"
                      # "description"
    ]

    def get_initial_queryset(self):
        """
        Preparing  Initial Queryset for the for rendering the data table.

        """
        if not self.model:
            raise NotImplementedError("Need to provide a model or implement get_initial_queryset!")
        else:
            if self.request.user.userprofile.role.values_list('role_name', flat=True)[0] == 'admin':
                organizations = list(self.request.user.userprofile.organization.get_descendants(include_self=True))
            else:
                organizations = [self.request.user.userprofile.organization]

            return self.get_initial_query_set_data(organizations=organizations)

    def get_initial_query_set_data(self, **kwargs):
        """
        Generic function required to fetch the initial data with respect to the page_type parameter in the get request requested.

        :param device_association:
        :param kwargs:
        :return: list of devices
        """

        page_type = self.request.GET.get('page_type')

        required_value_list = ['id','machine__name','device_name','ip_address']

        device_tab_technology = self.request.GET.get('data_tab')

        devices = filter_devices(organizations=kwargs['organizations'],
                                 data_tab=device_tab_technology,
                                 page_type=page_type,
                                 required_value_list=required_value_list
        )

        return devices

    def prepare_devices(self,qs):
        """

        :param device_list:
        :return:
        """
        page_type = self.request.GET['page_type']
        return prepare_gis_devices(qs, page_type)

    def prepare_machines(self, qs):
        """
        """
        device_list = []
        for device in qs:
            device_list.append(
                {
                    'device_name': device['device_name'],
                    'device_machine': device['machine_name'],
                    'id': device['id'],
                    'ip_address': device['ip_address']
                }
            )

        return prepare_machines(device_list)

    def prepare_polled_results(self, qs, machine_dict={}):
        """
        preparing polled results
        after creating static inventory first
        """
        device_tab_technology = self.request.GET.get('data_tab')
        device_technology_id = DeviceTechnology.objects.get(name__icontains=device_tab_technology).id

        page_type = self.request.GET.get('page_type')
        data_source = self.request.GET.get('data_source')

        device_list, performance_data, data_sources_list = list(), list(), list()

        search_table = "performance_networkstatus"

        data_sources_list = list()

        extra_query_condition = None

        if data_source == 'latency':
            extra_query_condition = ' AND (`{0}`.`current_value` > 0 ) '
            extra_query_condition += ' AND `{0}`.`severity` in ("down","warning","critical","warn","crit") '
            data_sources_list = ['rta']
        elif data_source == 'packet_drop':
            data_sources_list = ['pl']
            extra_query_condition = ' AND (`{0}`.`current_value` BETWEEN 1 AND 99 ) '
            extra_query_condition += ' AND `{0}`.`severity` in ("down","warning","critical","warn","crit") '
        elif data_source == 'down':
            data_sources_list = ['pl']
            extra_query_condition = ' AND (`{0}`.`current_value` >= 100 ) '
            extra_query_condition += ' AND `{0}`.`severity` in ("down") '
            search_table = "performance_networkstatus"
        elif data_source == 'service':
            extra_query_condition = ' AND `{0}`.`severity` in ("down","warning","critical","warn","crit") '
            search_table = "performance_servicestatus"

        required_data_columns = self.polled_columns

        sorted_device_list = list()

        #Fetching the data for the device w.r.t to their machine.
        for machine, machine_device_list in machine_dict.items():
            device_list = list()
            performance_data = list()
            performance_data = raw_prepare_result(performance_data=performance_data,
                                                  machine=machine,
                                                  table_name=search_table,
                                                  devices=machine_device_list,
                                                  data_sources=data_sources_list,
                                                  columns=required_data_columns,
                                                  condition=extra_query_condition if extra_query_condition else None
            )


            device_list = prepare_raw_alert_results(device_list,performance_data)

            # sorted_device_list += sorted(device_list, key=itemgetter('sys_timestamp'), reverse=True)
            sorted_device_list += device_list

        return sorted_device_list

    def prepare_results(self, qs):
        """
        Preparing the final result after fetching from the data base to render on the data table.

        :param qs:
        :return queryset
        """

        page_type=self.request.GET.get('page_type')

        if qs:
            qs = [{key: val if val else "" for key, val in dct.items()} for dct in qs]
            data_unit = "%"
            service_tab = 'down'
            # figure out which tab call is made.
            data_source = self.request.GET.get('data_source', '')
            if 'latency' == data_source:
                service_tab = 'latency'
                data_unit = "ms"
            elif 'packet_drop' == data_source:
                service_tab = 'packet_drop'
            elif 'service' == data_source:
                data_unit=''
                service_tab = 'service'

            for dct in qs:
                device = Device.objects.get(device_name= dct['device_name'])
                try:
                    dct.update(current_value = float(dct["current_value"]))
                except:
                    dct.update(current_value = dct["current_value"] + " " + data_unit)
                dct.update(action='<a href="/alert_center/{2}/device/{0}/service_tab/{1}/" title="Device Alerts"><i class="fa fa-warning text-warning"></i></a>\
                                       <a href="/performance/{2}_live/{0}/" title="Device Performance"><i class="fa fa-bar-chart-o text-info"></i></a>\
                                       <a href="/device/{0}" title="Device Inventory"><i class="fa fa-dropbox text-muted"></i></a>'.
                               format(device.id, service_tab, page_type ))

            return common_prepare_results(qs)

        return []

    def get_context_data(self, *args, **kwargs):
        """
        The maine function call to fetch, search, prepare and display the data on the data table.

        """

        request = self.request
        self.initialize(*args, **kwargs)

        qs = self.get_initial_queryset()

        #machines dict
        machines = self.prepare_machines(qs)
        #machines dict

        #prepare the polled results
        qs = self.prepare_polled_results(qs, machine_dict=machines)
        # this is query set with complete polled result

        #this function is for mapping to GIS inventory
        qs = self.prepare_devices(qs)
        #this function is for mapping to GIS inventory

        # number of records before filtering
        total_records = len(qs)

        # number of records after filtering
        total_display_records = len(qs)

        # qs = self.ordering(qs)
        # qs = self.paging(qs) #Removing pagination as of now to render all the data at once.
        # if the qs is empty then JSON is unable to serialize the empty ValuesQuerySet.Therefore changing its type to list.
        if not qs and isinstance(qs, ValuesQuerySet):
            qs = list(qs)

        # prepare output data
        aaData = self.prepare_results(qs)
        ret = {'sEcho': int(request.REQUEST.get('sEcho', 0)),
               'iTotalRecords': total_records,
               'iTotalDisplayRecords': total_display_records,
               'aaData': aaData
        }
        return ret


class SingleDeviceAlertDetails(View):
    """
    Generic Class for Network and Customer to render the details page for a single device.
    """

    def get(self, request, page_type, device_id, service_name):

        logged_in_user, devices_result = request.user.userprofile, list()

        if 'admin' in logged_in_user.role.values_list('role_name', flat=True):
            organizations = list(logged_in_user.organization.get_descendants(include_self=True))
        else:
            organizations = [logged_in_user.organization]

        devices_result += self.get_result(page_type, organizations)

        start_date= self.request.GET.get('start_date','')
        end_date= self.request.GET.get('end_date','')
        isSet = False

        if len(start_date) and len(end_date):
            start_date_object= datetime.datetime.strptime( start_date +" 00:00:00", "%d-%m-%Y %H:%M:%S" )
            end_date_object= datetime.datetime.strptime( end_date + " 23:59:59", "%d-%m-%Y %H:%M:%S" )
            start_date= format( start_date_object, 'U')
            end_date= format( end_date_object, 'U')
            isSet = True
            if start_date == end_date:
                # Converting the end date to the highest time in a day.
                end_date_object = datetime.datetime.strptime(end_date + " 23:59:59", "%d-%m-%Y %H:%M:%S")
        else:
            # The end date is the end limit we need to make query till.
            end_date_object = datetime.datetime.now()
            # The start date is the last monday of the week we need to calculate from.
            start_date_object = end_date_object - datetime.timedelta(days=end_date_object.weekday())
            # Replacing the time, to start with the 00:00:00 of the last monday obtained.
            start_date_object = start_date_object.replace(hour=00, minute=00, second=00, microsecond=00)
            # Converting the date to epoch time or Unix Timestamp
            end_date = format(end_date_object, 'U')
            start_date = format(start_date_object, 'U')
            isSet = True


        device_obj = Device.objects.get(id= device_id)
        device_name = device_obj.device_name
        machine_name = device_obj.machine.name

        data_list = None
        required_columns = ["device_name",
                            "ip_address",
                            "service_name",
                            "data_source",
                            "severity",
                            "current_value",
                            "sys_timestamp",
                            "description"
        ]

        is_ping = False

        if service_name == 'latency':
            data_list = EventNetwork.objects. \
                filter(device_name=device_name,
                       data_source='rta',
                       sys_timestamp__gte=start_date,
                       sys_timestamp__lte=end_date). \
                order_by("-sys_timestamp"). \
                values(*required_columns).using(alias=machine_name)

        elif service_name == 'packetdrop' or service_name == 'packet_drop':
            data_list = EventNetwork.objects. \
                filter(device_name=device_name,
                       data_source='pl',
                       sys_timestamp__gte=start_date,
                       sys_timestamp__lte=end_date). \
                order_by("-sys_timestamp"). \
                values(*required_columns).using(alias=machine_name)

        elif service_name == 'down':
            data_list = EventNetwork.objects. \
                filter(device_name=device_name,
                       data_source='pl',
                       current_value=100, #need to show up and down both
                       severity='DOWN',
                       sys_timestamp__gte=start_date,
                       sys_timestamp__lte=end_date). \
                order_by("-sys_timestamp"). \
                values(*required_columns).using(alias=machine_name)

        elif service_name == 'service':
            data_list = EventService.objects. \
                filter(device_name=device_name,
                       sys_timestamp__gte=start_date,
                       sys_timestamp__lte=end_date). \
                order_by("-sys_timestamp"). \
                values(*required_columns).using(alias=machine_name)

        elif service_name == 'ping':

            in_string = lambda x: "'" + str(x) + "'"
            col_string = lambda x: "`" + str(x) + "`"
            is_ping = True
            # raw query is required here so as to get data
            query = " "\
                    " SELECT " \
                    " original_table.`device_name`," \
                    " original_table.`ip_address`," \
                    " original_table.`service_name`," \
                    " original_table.`severity`," \
                    " original_table.`current_value` as latency," \
                    " `derived_table`.`current_value` as packet_loss, " \
                    " `original_table`.`sys_timestamp`," \
                    " original_table.`description` " \
                    " FROM `performance_eventnetwork` as original_table "\
                    " INNER JOIN (`performance_eventnetwork` as derived_table) "\
                    " ON( "\
                    "    original_table.`data_source` <> derived_table.`data_source` "\
                    "    AND "\
                    "   original_table.`sys_timestamp` = derived_table.`sys_timestamp` "\
                    "    AND "\
                    "    original_table.`device_name` = derived_table.`device_name` "\
                    " ) "\
                    " WHERE( "\
                    "    original_table.`device_name`= '{0}' "\
                    "    AND "\
                    "    original_table.`sys_timestamp` BETWEEN {1} AND {2} "\
                    " ) "\
                    " GROUP BY original_table.`sys_timestamp` "\
                    " ORDER BY original_table.`sys_timestamp` DESC ".format(
                    # (',').join(["original_table.`" + col_name + "`" for col_name in required_columns]),
                    device_name,
                    start_date,
                    end_date
                    )
            data_list = fetch_raw_result(query, machine_name)

        required_columns = [
            "device_name",
            "ip_address",
            "service_name",
            "data_source",
            "severity",
            "current_value",
            "alert_date_time",
            # "alert_time",
            "description"
        ]

        if is_ping:
            required_columns = [
                "device_name",
                "ip_address",
                "service_name",
                "severity",
                "latency",
                "packet_loss",
                "alert_date_time",
                # "alert_time",
                "description"
            ]

        for data in data_list:
            # data["alert_date"] = datetime.datetime. \
            #     fromtimestamp(float(data["sys_timestamp"])). \
            #     strftime("%d/%B/%Y")
            # data["alert_time"] = datetime.datetime. \
            #     fromtimestamp(float(data["sys_timestamp"])). \
            #     strftime("%I:%M %p")
            data["alert_date_time"] = datetime.datetime. \
                fromtimestamp(float(data["sys_timestamp"])). \
                strftime("%d/%B/%Y %I:%M %p")
                
            del (data["sys_timestamp"])

        download_excel = self.request.GET.get('download_excel', '')
        download_csv = self.request.GET.get('download_csv', '')

        if download_excel:

            workbook = xlwt.Workbook()
            worksheet = workbook.add_sheet('report')
            style = xlwt.XFStyle()

            borders = xlwt.Borders()
            borders.bottom = xlwt.Borders.DASHED
            style.borders = borders

            column_length = len(required_columns)
            row_length = len(data_list) - 1
            # Writing headers first for the excel file.
            for column in range(column_length):
                worksheet.write(0, column, required_columns[column], style=style)
            # Writing rest of the rows.
            for row in range(1, row_length):
                for column in range(column_length):
                    worksheet.write(row, column, data_list[row][required_columns[column]], style=style)

            response = HttpResponse(mimetype='application/vnd.ms-excel', content_type='text/plain')
            start_date_string = datetime.datetime.fromtimestamp(float(start_date)).strftime("%d/%B/%Y")
            end_date_string = datetime.datetime.fromtimestamp(float(end_date)).strftime("%d/%B/%Y")
            response['Content-Disposition'] = 'attachment; filename=alert_report_{0}_{1}_to_{2}.xls' \
                .format(device_name, start_date_string, end_date_string)
            workbook.save(response)
            return response

        elif download_csv:

            response = HttpResponse(content_type='text/csv')
            start_date_string = datetime.datetime.fromtimestamp(float(start_date)).strftime("%d/%B/%Y")
            end_date_string = datetime.datetime.fromtimestamp(float(end_date)).strftime("%d/%B/%Y")
            response['Content-Disposition'] = 'attachment; filename=alert_report_{0}_{1}_to_{2}.csv' \
                .format(device_name, start_date_string, end_date_string)

            writer = csv.writer(response)
            headers = map(lambda x: x.replace('_', ' '), required_columns)
            writer.writerow(headers)
            column_length = len(required_columns)
            row_length = len(data_list) - 1

            for row in range(1, row_length):
                row_list = list()
                for column in range(0, column_length):
                    row_list.append(data_list[row][required_columns[column]])
                writer.writerow(row_list)
            return response

        else:

            required_columns = map(lambda x: x.replace('_', ' '), required_columns)
            context = dict(is_ping=is_ping,
                           devices=devices_result,
                           current_device_id=device_id,
                           get_status_url='performance/get_inventory_device_status/' + page_type + '/device/' + str(device_id),
                           current_device_name=device_name,
                           page_type=page_type,
                           table_data=data_list,
                           table_header=required_columns,
                           service_name=service_name,
                           start_date_object=start_date_object,
                           end_date_object=end_date_object,
                           )

            return render(request, 'alert_center/single_device_alert.html', context)

    def get_result(self, page_type, organizations):
        """
        Generic function to return the result w.r.t the page_type and organization of the current logged in user.

        :param page_type:
        :param organization:
        return result
        """

        device_result = []

        if page_type == "customer" :
            device_result = organization_customer_devices(organizations=organizations)

        elif page_type == "network":
            device_result = organization_network_devices(organizations=organizations)

        result = list()
        for device in device_result:
            result.append({'id': device.id,
                           'name':  device.device_name,
                           'alias': device.device_alias,
                           'technology': DeviceTechnology.objects.get(id=device.device_technology).name
            }
            )
        return result


# misc utility functions

def prepare_query(table_name=None,
                  devices=None,
                  data_sources=["pl", "rta"],
                  columns=None, condition=None,
                  offset=None,
                  limit=None):
    """

    :param table_name:
    :param devices:
    :param data_sources:
    :param columns:
    :param condition:
    :param offset:
    :param limit:
    :return:
    """
    in_string = lambda x: "'" + str(x) + "'"
    # col_string = lambda x,y: ("%s`" + str(x) + "`") %(y)
    query = None

    if not columns:
        return None

    if table_name and devices:
        query = "SELECT {0} FROM {1} as original_table " \
                "LEFT OUTER JOIN ({1} as derived_table) " \
                "ON ( " \
                "        original_table.data_source = derived_table.data_source " \
                "    AND original_table.device_name = derived_table.device_name " \
                "    AND original_table.id < derived_table.id" \
                ") " \
                "WHERE ( " \
                "        derived_table.id is null " \
                "    AND original_table.device_name in ( {2} ) " \
                "    {3}" \
                "    {4}" \
                ")" \
                "ORDER BY original_table.id DESC " \
                "".format(
            (',').join(["original_table.`" + col_name + "`" for col_name in columns]),
            table_name,
            (",".join(map(in_string, devices))),
            "AND original_table.data_source in ( {0} )".format(
                (',').join(map(in_string, data_sources))
            ) if data_sources else "",
            condition.format("original_table") if condition else "",
            )
        if limit is not None and offset is not None:
            query += "LIMIT {0}, {1}".format(offset, limit)

    return query


def common_get_performance_data(model=EventNetwork,
                                table_name="performance_networkstatus",
                                device_list=[],
                                data_sources_list=["pl", "rta"],
                                columns=None):
    """



    :param model:
    :param table_name:
    :param columns:
    :param data_sources_list:
    :param device_list:
    :return:
    """
    if not columns:
        columns = ["id", "service_name", "ip_address", "device_name", "data_source", "severity", "current_value", "sys_timestamp",
                   #"description"
        ]

    query = prepare_query(table_name=table_name,
                          devices=device_list,
                          data_sources=data_sources_list,
                          columns=columns
    )

    device_result = {}
    perf_result = {"severity": "N/A", "current_value": "N/A", "sys_timestamp": "N/A", "description": "N/A"}

    performance_data = model.objects.raw(query)

    for device in device_list:
        if device not in device_result:
            device_result[device] = perf_result

    for device in device_result:
        perf_result = {"severity": "N/A", "current_value": "N/A", "sys_timestamp": "N/A", "description": "N/A"}

        for data in performance_data:
            if str(data.device_name).strip().lower() == str(device).strip().lower():
                d_src = str(data.data_source).strip().lower()
                current_val = str(data.current_value)

                perf_result["severity"] = str(data.severity).strip().upper()

                perf_result["current_value"] = current_val

                perf_result["sys_timestamp"] = str(datetime.datetime.fromtimestamp(float(data.sys_timestamp)))

                perf_result["description"] = ''#data.description

                device_result[device] = perf_result

    return device_result


def common_prepare_results(qs):
    """
    Common function to prepare result on query set

    :params qs:
    :return qs:
    """

    for dct in qs:
        current_value = dct['current_value']
        try:
            current_value = float(current_value)
        except:
            pass
        if dct['severity'].upper() == 'DOWN' \
                or "CRITICAL" in dct['description'].upper() \
                or dct['severity'].upper() == 'CRITICAL':
            dct['severity'] = '<i class="fa fa-circle red-dot" value="1" title="Critical"><span style="display:none">1</span></i>'
            dct['current_value'] = current_value
            dct['description'] = '<span class="text-danger">%s</span>' % (dct['description'])

        elif dct['severity'].upper() == 'WARNING' \
                or "WARNING" in dct['description'].upper() \
                or "WARN" in dct['description'].upper():
            dct['severity'] = '<i class="fa fa-circle orange-dot" value="2" title="Warning"><span style="display:none">2</span></i>'
            dct['current_value'] = current_value
            dct['description'] = '<span class="text-warning">%s</span>' % (dct['description'])

        elif dct['severity'].upper() == 'UP' \
                or "OK" in dct['description'].upper():
            dct['severity'] = '<i class="fa fa-circle green-dot" value="3" title="Ok"><span style="display:none">3</span></i>'
            dct['current_value'] = current_value
            dct['description'] = '<span class="text-success">%s</span>' % (dct['description'])

        else:
            dct['severity'] = '<i class="fa fa-circle grey-dot" value="4" title="Ok"><span style="display:none">4</span></i>'
            dct['current_value'] = current_value
            dct['description'] = '<span class="text-muted">%s</span>' % (dct['description'])

    return qs


def severity_level_check(list_to_check):
    """

    :return:
    """
    severity_check = ['DOWN', 'CRITICAL', 'WARNING', "WARN", "CRIT"]
    for item in list_to_check:
        for severity in severity_check:
            if severity.lower() in item.lower():
                return True


@cache_for(300)
def raw_prepare_result(performance_data,
                       machine,
                       table_name=None,
                       devices=None,
                       data_sources=["pl", "rta"],
                       columns=None,
                       condition=None,
                       offset=0,
                       limit=5000
    ):
    """

    :param performance_data:
    :param machine:
    :param table_name:
    :param devices:
    :param data_sources:
    :param columns:
    :param condition:
    :param offset:
    :param limit:
    :return:
    """

    st = datetime.datetime.now()
    if DEBUG:
        logger.debug("ALERT : Preparing Query Results")
        logger.debug("START TIME : %s" %st)

    count = 0

    while count <= math.ceil(len(devices) / limit):

        query = prepare_query(table_name=table_name,
                              devices=devices[limit * count:limit * (count + 1)],# spilicing the devices here
                              data_sources=data_sources,
                              columns=columns,
                              condition=condition,
                              offset=offset,
                              limit=limit
        )
        # print(query)
        if query:
            performance_data += fetch_raw_result(query, machine)
        else:
            break

        count += 1

    if DEBUG:
        endtime = datetime.datetime.now()
        elapsed = endtime - st
        logger.debug("TIME TAKEN : {}".format(divmod(elapsed.total_seconds(), 60)))
        logger.debug("ALERT : Preparing Query Results : COMPLETED")

    return performance_data


@cache_for(300)
def indexed_alert_results(performance_data):
    """

    :param performance_data:
    :return:
    """

    st = datetime.datetime.now()
    if DEBUG:
        logger.debug("ALERT : Preparing INDEXED Results")
        logger.debug("START TIME : %s" %st)

    indexed_raw_results = {}

    for data in performance_data:
        #this would be a unique combination
        if data['data_source'] is not None and data['device_name'] is not None:
            defined_index = data['device_name'], data['data_source']
            if defined_index not in indexed_raw_results:
                indexed_raw_results[defined_index] = None
            indexed_raw_results[defined_index] = data

    if DEBUG:
        endtime = datetime.datetime.now()
        elapsed = endtime - st
        logger.debug("TIME TAKEN : {}".format(divmod(elapsed.total_seconds(), 60)))
        logger.debug("ALERT : Preparing INDEXED Results : COMPLETED")

    return indexed_raw_results


@cache_for(300)
def prepare_raw_alert_results(device_list=[], performance_data=None):
    """
    prepare GIS result using raw query

    :param device_list:
    :param performance_data:
    :return:
    """
    st = datetime.datetime.now()
    if DEBUG:
        logger.debug("ALERT : Preparing ALERT POLLED Results")
        logger.debug("START TIME : %s" %st)

    indexed_alert_data = indexed_alert_results(performance_data)

    for device_alert in indexed_alert_data:
        # the data would be a tuple of ("device_name"."data_source")
        #sample index data
        #{(u'511', u'pl'): {
        # 'data_source': u'pl',
        # 'severity': u'down',
        # 'max_value': u'0',
        # 'age': 1416309593L,
        # 'device_name': u'511',
        # 'sys_timestamp': 0L,
        # 'current_value': u'49',
        # 'ip_address': u'10.157.66.9',
        # 'id': 59440L}
        # }

        device_name, data_source = device_alert

        data = indexed_alert_data[device_alert]

        static_gis_keys = {
                "page_type": "NA",
                "device_type": "NA",
                "severity": "NA",
                "bs_name": "NA",
                "circuit_id": "NA",
                "sector_id": "NA",
                "city": "NA",
                "state": "NA",
                "customer_name": "NA",
                "data_source_name": "NA",
                "current_value": "NA",
                "max_value": "NA",
                "sys_timestamp": "NA",
                "age": "NA",
                'description': "NA"
        }

        if severity_level_check(list_to_check=[data['severity']]):
            device_events = static_gis_keys
            device_events.update({
                'device_name': device_name,
                'severity': data['severity'],
                'ip_address': data["ip_address"],
                'data_source_name': " ".join(map(lambda a: a.title(), data_source.split("_"))),
                'current_value': data["current_value"],
                'max_value': data["max_value"],
                'sys_timestamp': datetime.datetime.fromtimestamp(
                    float(data["sys_timestamp"])).strftime("%m/%d/%y (%b) %H:%M:%S (%I:%M %p)"),
                'age': datetime.datetime.fromtimestamp(
                    float(data["age"])).strftime("%d days %H:%M:%S")
                    if data["age"]
                    else "",
                'description': ''#data['description']
            })

            device_list.append(device_events)

    if DEBUG:
        endtime = datetime.datetime.now()
        elapsed = endtime - st
        logger.debug("TIME TAKEN : {}".format(divmod(elapsed.total_seconds(), 60)))
        logger.debug("ALERT : Preparing ALERT POLLED Results : COMPLETED")

    return device_list
