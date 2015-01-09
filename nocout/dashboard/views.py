import json
import datetime
from dateutil import relativedelta

from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.db.models.query import ValuesQuerySet
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView

from nocout.utils import logged_in_user_organizations
from device.models import DeviceTechnology, Device
from performance.models import ServiceStatus, NetworkAvailabilityDaily, UtilizationStatus, Topology

#inventory utils
from inventory.utils.util import organization_customer_devices, organization_network_devices,\
    organization_sectors, prepare_machines
#inventory utils

from dashboard.models import DashboardSetting, MFRDFRReports, DFRProcessed, MFRProcessed, MFRCauseCode
from dashboard.forms import DashboardSettingForm, MFRDFRReportsForm
from dashboard.utils import get_service_status_results, get_dashboard_status_range_counter, get_pie_chart_json_response_dict,\
    get_dashboard_status_sector_range_counter, get_pie_chart_json_response_sector_dict, \
    get_topology_status_results
from dashboard.config import dashboards
from nocout.mixins.user_action import UserLogDeleteMixin
from nocout.mixins.permissions import SuperUserRequiredMixin
from nocout.mixins.datatable import DatatableSearchMixin, ValuesQuerySetMixin


class DashbaordSettingsListView(TemplateView):
    """
    Class Based View for the Dashboard data table rendering.

    In this view no data is passed to datatable while rendering template.
    Another ajax call is made to fill in datatable.
    """
    template_name = 'dashboard/dashboard_settings_list.html'

    def get_context_data(self, **kwargs):
        """
        Preparing the Context Variable required in the template rendering.
        """
        context = super(DashbaordSettingsListView, self).get_context_data(**kwargs)
        datatable_headers = [
            {'mData': 'page_name', 'sTitle': 'Page Name', 'sWidth': 'auto', },
            {'mData': 'technology__name', 'sTitle': 'Technology Name', 'sWidth': 'auto', },
            {'mData': 'name', 'sTitle': 'Dashboard Name', 'sWidth': 'auto', },
            {'mData': 'range1', 'sTitle': 'Range 1', 'sWidth': 'auto', 'bSortable': False },
            {'mData': 'range2', 'sTitle': 'Range 2', 'sWidth': 'auto', 'bSortable': False },
            {'mData': 'range3', 'sTitle': 'Range 3', 'sWidth': 'auto', 'bSortable': False },
            {'mData': 'range4', 'sTitle': 'Range 4', 'sWidth': 'auto', 'bSortable': False },
            {'mData': 'range5', 'sTitle': 'Range 5', 'sWidth': 'auto', 'bSortable': False },
            {'mData': 'range6', 'sTitle': 'Range 6', 'sWidth': 'auto', 'bSortable': False },
            {'mData': 'range7', 'sTitle': 'Range 7', 'sWidth': 'auto', 'bSortable': False },
            {'mData': 'range8', 'sTitle': 'Range 8', 'sWidth': 'auto', 'bSortable': False },
            {'mData': 'range9', 'sTitle': 'Range 9', 'sWidth': 'auto', 'bSortable': False },
            {'mData': 'range10', 'sTitle': 'Range 10', 'sWidth': 'auto', 'bSortable': False },
        ]

        #if the user is superuser then the action column will appear on the datatable
        if self.request.user.is_superuser:
            datatable_headers.append({'mData': 'actions', 'sTitle': 'Actions', 'sWidth': '5%', 'bSortable': False })

        context['datatable_headers'] = json.dumps(datatable_headers)
        return context


class DashbaordSettingsListingTable(DatatableSearchMixin, ValuesQuerySetMixin, BaseDatatableView):
    """
    Class based View to render Dashboard Settings Data table.
    """
    model = DashboardSetting
    columns = ['page_name', 'name', 'technology__name', 'range1', 'range2', 'range3', 'range4', 'range5', 'range6', 'range7', 'range8', 'range9', 'range10']
    keys = ['page_name', 'technology__name', 'name', 'range1_start', 'range2_start', 'range3_start', 'range4_start', 'range5_start', 'range6_start', 'range7_start', 'range8_start', 'range9_start', 'range10_start', 'range1_end', 'range2_end', 'range3_end', 'range4_end', 'range5_end', 'range6_end', 'range7_end', 'range8_end', 'range9_end', 'range10_end', 'range1_color_hex_value', 'range2_color_hex_value', 'range3_color_hex_value', 'range4_color_hex_value', 'range5_color_hex_value', 'range6_color_hex_value', 'range7_color_hex_value', 'range8_color_hex_value', 'range9_color_hex_value', 'range10_color_hex_value']
    order_columns = ['page_name', 'name', 'technology__name']
    columns = ['page_name', 'technology__name', 'name', 'range1_start', 'range2_start', 'range3_start', 'range4_start', 'range5_start', 'range6_start', 'range7_start', 'range8_start', 'range9_start', 'range10_start', 'range1_end', 'range2_end', 'range3_end', 'range4_end', 'range5_end', 'range6_end', 'range7_end', 'range8_end', 'range9_end', 'range10_end', 'range1_color_hex_value', 'range2_color_hex_value', 'range3_color_hex_value', 'range4_color_hex_value', 'range5_color_hex_value', 'range6_color_hex_value', 'range7_color_hex_value', 'range8_color_hex_value', 'range9_color_hex_value', 'range10_color_hex_value']

    def prepare_results(self, qs):
        """
        Preparing the final result after fetching from the data base to render on the data table.

        :param qs:
        :return qs

        """
        json_data = [{key: val if val else "" for key, val in dct.items()} for dct in qs]
        for obj in json_data:
            for i in range(1, 11):
                range_start = obj.pop('range%d_start' %i)
                range_end = obj.pop('range%d_end' %i)
                color_hex_value = obj.pop('range%d_color_hex_value' %i)
                range_color = "<div style='display:block; height:20px; width:20px;\
                        background:{0}'></div>".format(color_hex_value)
                if range_start:
                    obj.update({'range%d' %i : "(%s -<br>%s)<br>%s" % (range_start, range_end, range_color)})
                else:
                    obj.update({'range%d' %i : ""})

                # Add actions to obj.
            obj_id = obj.pop('id')
            edit_url = reverse_lazy('dashboard-settings-update', kwargs={'pk': obj_id})
            delete_url = reverse_lazy('dashboard-settings-delete', kwargs={'pk': obj_id})
            edit_action = '<a href="%s"><i class="fa fa-pencil text-dark"></i></a>' % edit_url
            delete_action = '<a href="%s"><i class="fa fa-trash-o text-danger"></i></a>' % delete_url
            obj.update({'actions': edit_action + ' ' + delete_action})
        return json_data


class DashbaordSettingsCreateView(SuperUserRequiredMixin, CreateView):
    """
    Class based view to create new Dashboard Setting.
    """
    model = DashboardSetting
    form_class = DashboardSettingForm
    template_name = "dashboard/dashboard_settings_new.html"
    success_url = reverse_lazy('dashboard-settings')

    def get_context_data(self, **kwargs):
        context = super(DashbaordSettingsCreateView, self).get_context_data(**kwargs)
        context['dashboards'] = json.dumps(dashboards)
        technology_options = dict(DeviceTechnology.objects.values_list('name', 'id'))
        context['technology_options'] = json.dumps(technology_options)
        return context


class DashbaordSettingsDetailView(DetailView):
    """
    Class based view to render the Dashboard Setting detail.
    """
    model = DashboardSetting
    template_name = 'dashboard/dashboard_detail.html'


class DashbaordSettingsUpdateView(SuperUserRequiredMixin, UpdateView):
    """
    Class based view to update Dashboard Setting.
    """
    model = DashboardSetting
    form_class = DashboardSettingForm
    template_name = "dashboard/dashboard_settings_update.html"
    success_url = reverse_lazy('dashboard-settings')

    def get_context_data(self, **kwargs):
        context = super(DashbaordSettingsUpdateView, self).get_context_data(**kwargs)
        context['dashboards'] = json.dumps(dashboards)
        technology_options = dict(DeviceTechnology.objects.values_list('name', 'id'))
        context['technology_options'] = json.dumps(technology_options)
        return context


class DashbaordSettingsDeleteView(SuperUserRequiredMixin, UserLogDeleteMixin, DeleteView):
    """
    Class based View to delete the Dashboard Setting.

    """
    model = DashboardSetting
    template_name = 'dashboard/dashboard_settings_delete.html'
    success_url = reverse_lazy('dashboard-settings')
    obj_alias = 'name'

#****************************************** RF PERFORMANCE DASHBOARD ********************************************


class PerformanceDashboardMixin(object):
    """
    Provide common method get for Performance Dashboard.

    To use this Mixin set `template_name` and implement method get_init_data to provide following attributes:

        - data_source_config
        - technology
        - devices_method_to_call
        - devices_method_kwargs
    """

    def get(self, request):
        """
        Handles the get request

        :param request:
        :return Http response object:
        """
        data_source_config, technology, devices_method_to_call, devices_method_kwargs, is_bh = self.get_init_data()
        template_dict = {'data_sources': json.dumps(data_source_config.keys())}

        data_source = request.GET.get('data_source')
        if not data_source:
            return render(self.request, self.template_name, dictionary=template_dict)

        # Get Service Name from queried data_source
        try:
            service_name = data_source_config[data_source]['service_name']
            model = data_source_config[data_source]['model']
        except KeyError as e:
            return render(self.request, self.template_name, dictionary=template_dict)

        try:
            dashboard_setting = DashboardSetting.objects.get(technology=technology, page_name='rf_dashboard', name=data_source, is_bh=is_bh)
        except DashboardSetting.DoesNotExist as e:
            return HttpResponse(json.dumps({
                "message": "Corresponding dashboard seting is not available.",
                "success": 0
            }))

        # Get User's organizations
        # (admin : organization + sub organization)
        # (operator + viewer : same organization)
        user_organizations = logged_in_user_organizations(self)

        # Get Devices of User's Organizations. [and are Sub Station]
        user_devices = devices_method_to_call(user_organizations, technology, **devices_method_kwargs)

        service_status_results = get_service_status_results(
            user_devices, model=model, service_name=service_name, data_source=data_source
        )

        range_counter = get_dashboard_status_range_counter(dashboard_setting, service_status_results)

        response_dict = get_pie_chart_json_response_dict(dashboard_setting, data_source, range_counter)

        return HttpResponse(json.dumps(response_dict))


class WiMAX_Performance_Dashboard(PerformanceDashboardMixin, View):
    """
    The Class based View to get performance dashboard page requested.

    """

    template_name = 'rf_performance/wimax.html'

    def get_init_data(self):
        """
        Handles the get request

        :param request:
        :return Http response object:
        """
        data_source_config = {
            'ul_rssi': {'service_name': 'wimax_ul_rssi', 'model': ServiceStatus},
            'dl_rssi': {'service_name': 'wimax_dl_rssi', 'model': ServiceStatus},
            'ul_cinr': {'service_name': 'wimax_ul_cinr', 'model': ServiceStatus},
            'dl_cinr': {'service_name': 'wimax_dl_cinr', 'model': ServiceStatus},
        }
        technology = DeviceTechnology.objects.get(name__icontains='WiMAX').id
        devices_method_to_call = organization_customer_devices
        devices_method_kwargs = dict(specify_ptp_type='all')
        is_bh = False
        return data_source_config, technology, devices_method_to_call, devices_method_kwargs, is_bh


class PMP_Performance_Dashboard(PerformanceDashboardMixin, View):
    """
    The Class based View to get performance dashboard page requested.

    """
    template_name = 'rf_performance/pmp.html'

    def get_init_data(self):
        """
        Provide data for mixin's get method.
        """

        data_source_config = {
            'ul_jitter': {'service_name': 'cambium_ul_jitter', 'model': ServiceStatus},
            'dl_jitter': {'service_name': 'cambium_dl_jitter', 'model': ServiceStatus},
            'rereg_count': {'service_name': 'cambium_rereg_count', 'model': ServiceStatus},
            'ul_rssi': {'service_name': 'cambium_ul_rssi', 'model': ServiceStatus},
            'dl_rssi': {'service_name': 'cambium_dl_rssi', 'model': ServiceStatus},
        }
        technology = DeviceTechnology.objects.get(name='PMP').id
        devices_method_to_call = organization_customer_devices
        devices_method_kwargs = dict(specify_ptp_type='all')
        is_bh = False
        return data_source_config, technology, devices_method_to_call, devices_method_kwargs, is_bh


class PTP_Performance_Dashboard(PerformanceDashboardMixin, View):
    """
    The Class based View to get performance dashboard page requested.

    """
    template_name = 'rf_performance/ptp.html'

    def get_init_data(self):
        """
        Provide data for mixin's get method.
        """

        data_source_config = {
            'rssi': {'service_name': 'radwin_rssi', 'model': ServiceStatus},
            'uas': {'service_name': 'radwin_uas', 'model': ServiceStatus},
        }
        technology = DeviceTechnology.objects.get(name='P2P').id
        devices_method_to_call = organization_customer_devices
        devices_method_kwargs = dict(specify_ptp_type='ss')
        is_bh = False
        return data_source_config, technology, devices_method_to_call, devices_method_kwargs, is_bh


class PTPBH_Performance_Dashboard(PerformanceDashboardMixin, View):
    """
    The Class based View to get performance dashboard page requested.

    """
    template_name = 'rf_performance/ptp_bh.html'

    def get_init_data(self):
        """
        Provide data for mixin's get method.
        """

        data_source_config = {
            'rssi': {'service_name': 'radwin_rssi', 'model': ServiceStatus},
            'availability': {'service_name': 'availability', 'model': NetworkAvailabilityDaily},
            'uas': {'service_name': 'radwin_uas', 'model': ServiceStatus},
        }
        technology = DeviceTechnology.objects.get(name='P2P').id
        devices_method_to_call = organization_network_devices
        devices_method_kwargs = dict(specify_ptp_bh_type='ss')
        is_bh = True
        return data_source_config, technology, devices_method_to_call, devices_method_kwargs, is_bh


######################################## MFR DFR Reports ########################################

class MFRDFRReportsListView(TemplateView):
    """
    Class Based View for the MFR-DFR-Reports data table rendering.

    In this view no data is passed to datatable while rendering template.
    Another ajax call is made to fill in datatable.
    """
    template_name = 'mfrdfr/mfr_dfr_reports_list.html'

    def get_context_data(self, **kwargs):
        """
        Preparing the Context Variable required in the template rendering.
        """
        context = super(MFRDFRReportsListView, self).get_context_data(**kwargs)
        datatable_headers = [
            {'mData': 'name', 'sTitle': 'Report Name', 'sWidth': 'auto', },
            {'mData': 'type', 'sTitle': 'Report Type', 'sWidth': 'auto'},
            {'mData': 'is_processed', 'sTitle': 'Processed', 'sWidth': 'auto'},
            {'mData': 'process_for', 'sTitle': 'Process For', 'sWidth': 'auto'},
        ]

        #if the user is superuser then the action column will appear on the datatable
        if self.request.user.is_superuser:
            datatable_headers.append({'mData': 'actions', 'sTitle': 'Actions', 'sWidth': '5%', 'bSortable': False })

        context['datatable_headers'] = json.dumps(datatable_headers)
        return context


class MFRDFRReportsListingTable(DatatableSearchMixin, ValuesQuerySetMixin, BaseDatatableView):
    model = MFRDFRReports
    columns = ['name', 'type', 'is_processed', 'process_for']
    search_columns = ['name', 'type', 'is_processed']
    order_columns = ['name', 'type', 'is_processed', 'process_for']

    def prepare_results(self, qs):
        """
        Preparing the final result after fetching from the data base to render on the data table.

        :param qs:
        :return qs

        """
        json_data = [{key: val if val else "" for key, val in dct.items()} for dct in qs]
        for obj in json_data:
            obj['is_processed'] = 'Yes' if obj['is_processed'] else 'No'
            obj_id = obj.pop('id')
            delete_url = reverse_lazy('mfr-dfr-reports-delete', kwargs={'pk': obj_id})
            delete_action = '<a href="%s"><i class="fa fa-trash-o text-danger"></i></a>' % delete_url
            obj.update({'actions': delete_action})
        return json_data


class MFRDFRReportsCreateView(CreateView):
    model = MFRDFRReports
    form_class = MFRDFRReportsForm
    template_name = "mfrdfr/mfr_dfr_reports_upload.html"
    success_url = reverse_lazy('mfr-dfr-reports-list')

    def form_valid(self, form):
        response = super(MFRDFRReportsCreateView, self).form_valid(form)
        self.object.absolute_path = self.object.upload_to.path
        self.object.save()
        return response


class MFRDFRReportsDeleteView(UserLogDeleteMixin, DeleteView):
    """
    Class based View to delete the Dashboard Setting.

    """
    model = MFRDFRReports
    template_name = 'mfrdfr/mfr_dfr_reports_delete.html'
    success_url = reverse_lazy('mfr-dfr-reports-list')
    obj_alias = 'name'


class DFRProcessedListView(TemplateView):
    """
    Class Based View for the DFR-Processed data table rendering.

    In this view no data is passed to datatable while rendering template.
    Another ajax call is made to fill in datatable.
    """
    template_name = 'mfrdfr/dfr_processed_list.html'

    def get_context_data(self, **kwargs):
        """
        Preparing the Context Variable required in the template rendering.
        """
        context = super(DFRProcessedListView, self).get_context_data(**kwargs)
        datatable_headers = [
            {'mData': 'processed_for__name', 'sTitle': 'Uploaded Report Name', 'sWidth': 'auto', },
            {'mData': 'processed_for__process_for', 'sTitle': 'Report Processed For', 'sWidth': 'auto'},
            {'mData': 'processed_on', 'sTitle': 'Processed On (Date)', 'sWidth': 'auto'},
            {'mData': 'processed_key', 'sTitle': 'Key for Processing', 'sWidth': 'auto'},
            {'mData': 'processed_value', 'sTitle': 'Value for Processing', 'sWidth': 'auto'},
            {'mData': 'processed_report_path', 'sTitle': 'Processed Report', 'sWidth': 'auto', 'bSortable': False},
        ]

        context['datatable_headers'] = json.dumps(datatable_headers)
        return context


class DFRProcessedListingTable(DatatableSearchMixin, ValuesQuerySetMixin, BaseDatatableView):
    model = DFRProcessed
    columns = ['processed_for__name', 'processed_for__process_for', 'processed_on', 'processed_key', 'processed_value']
    search_columns = ['processed_for__name', 'processed_key', 'processed_value']
    order_columns = ['processed_for__name', 'processed_for__process_for', 'processed_on', 'processed_key', 'processed_value']

    def prepare_results(self, qs):
        """
        Preparing the final result after fetching from the data base to render on the data table.

        :param qs:
        :return qs

        """
        json_data = [{key: val if val else "" for key, val in dct.items()} for dct in qs]
        for obj in json_data:
            processed_report_path = reverse('dfr-processed-reports-download', kwargs={'pk': obj.pop('id')})
            obj['processed_report_path'] = '<a href="' + processed_report_path + '" target="_blank">' + \
                    '<img src="/static/img/ms-office-icons/excel_2013_green.png" ' + \
                    'style="float:left; display:block; height:25px; width:25px;"></a>'
        return json_data


def dfr_processed_report_download(request, pk):
    dfr_processed = DFRProcessed.objects.get(id=pk)

    f = file(dfr_processed.processed_report_path, 'r')
    response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="dfr_report_' + str(dfr_processed.processed_for.process_for) + '.xlsx"'
    return response

#***************************************** DFR-REPORTS *******************************************************

class DFRReportsListView(TemplateView):
    """
    Class Based View for the DFR-Reports data table rendering.

    In this view no data is passed to datatable while rendering template.
    Another ajax call is made to fill in datatable.
    """
    template_name = 'dfr/dfr_reports_list.html'

    def get_context_data(self, **kwargs):
        """
        Preparing the Context Variable required in the template rendering.
        """
        context = super(DFRReportsListView, self).get_context_data(**kwargs)
        datatable_headers = [
            {'mData': 'name', 'sTitle': 'Report Name', 'sWidth': 'auto', },
            {'mData': 'is_processed', 'sTitle': 'Processed', 'sWidth': 'auto'},
            {'mData': 'process_for', 'sTitle': 'Process For', 'sWidth': 'auto'},
        ]

        #if the user is superuser then the action column will appear on the datatable
        if self.request.user.is_superuser:
            datatable_headers.append({'mData': 'actions', 'sTitle': 'Actions', 'sWidth': '5%', 'bSortable': False })

        context['datatable_headers'] = json.dumps(datatable_headers)
        return context


class DFRReportsListingTable(DatatableSearchMixin, ValuesQuerySetMixin, BaseDatatableView):
    model = MFRDFRReports
    columns = ['name', 'is_processed', 'process_for']
    search_columns = ['name', 'is_processed']
    order_columns = ['name', 'is_processed', 'process_for']

    def get_initial_queryset(self):
        qs = super(DFRReportsListingTable, self).get_initial_queryset()
        qs = qs.filter(type='DFR')
        return qs

    def prepare_results(self, qs):
        """
        Preparing the final result after fetching from the data base to render on the data table.

        :param qs:
        :return qs

        """
        json_data = [{key: val if val else "" for key, val in dct.items()} for dct in qs]
        for obj in json_data:
            obj['is_processed'] = 'Yes' if obj['is_processed'] else 'No'
            obj_id = obj.pop('id')
            delete_url = reverse_lazy('dfr-reports-delete', kwargs={'pk': obj_id})
            delete_action = '<a href="%s"><i class="fa fa-trash-o text-danger"></i></a>' % delete_url
            obj.update({'actions': delete_action})
        return json_data


class DFRReportsDeleteView(UserLogDeleteMixin, DeleteView):
    """
    Class based View to delete the Dashboard Setting.

    """
    model = MFRDFRReports
    template_name = 'mfrdfr/mfr_dfr_reports_delete.html'
    success_url = reverse_lazy('dfr-reports-list')
    obj_alias = 'name'


#********************************************** MFR-Reports ************************************************


class MFRReportsListView(TemplateView):
    """
    Class Based View for the MFR-Reports data table rendering.

    In this view no data is passed to datatable while rendering template.
    Another ajax call is made to fill in datatable.
    """
    template_name = 'mfr/mfr_reports_list.html'

    def get_context_data(self, **kwargs):
        """
        Preparing the Context Variable required in the template rendering.
        """
        context = super(MFRReportsListView, self).get_context_data(**kwargs)
        datatable_headers = [
            {'mData': 'name', 'sTitle': 'Report Name', 'sWidth': 'auto', },
            {'mData': 'is_processed', 'sTitle': 'Processed', 'sWidth': 'auto'},
            {'mData': 'process_for', 'sTitle': 'Process For', 'sWidth': 'auto'},
        ]

        #if the user is superuser then the action column will appear on the datatable
        if self.request.user.is_superuser:
            datatable_headers.append({'mData': 'actions', 'sTitle': 'Actions', 'sWidth': '5%', 'bSortable': False })

        context['datatable_headers'] = json.dumps(datatable_headers)
        return context


class MFRReportsListingTable(DatatableSearchMixin, ValuesQuerySetMixin, BaseDatatableView):
    model = MFRDFRReports
    columns = ['name', 'is_processed', 'process_for']
    search_columns = ['name', 'is_processed']
    order_columns = ['name', 'is_processed', 'process_for']

    def get_initial_queryset(self):
        qs = super(MFRReportsListingTable, self).get_initial_queryset()
        qs = qs.filter(type='MFR')
        return qs

    def prepare_results(self, qs):
        """
        Preparing the final result after fetching from the data base to render on the data table.

        :param qs:
        :return qs

        """
        json_data = [{key: val if val else "" for key, val in dct.items()} for dct in qs]
        for obj in json_data:
            obj['is_processed'] = 'Yes' if obj['is_processed'] else 'No'
            obj_id = obj.pop('id')
            delete_url = reverse_lazy('dfr-reports-delete', kwargs={'pk': obj_id})
            delete_action = '<a href="%s"><i class="fa fa-trash-o text-danger"></i></a>' % delete_url
            obj.update({'actions': delete_action})
        return json_data


class MFRReportsDeleteView(UserLogDeleteMixin, DeleteView):
    """
    Class based View to delete the Dashboard Setting.

    """
    model = MFRDFRReports
    template_name = 'mfrdfr/mfr_dfr_reports_delete.html'
    success_url = reverse_lazy('mfr-reports-list')
    obj_alias = 'name'


#**************************************** Main Dashbaord ***************************************#


class MainDashboard(View):
    """
    The Class based View to return Main Dashboard.

    Following are charts included in main-dashboard:

        - WiMAX Sector Capicity
        - PMP Sector Capicity
        - WiMAX Sales Oppurtunity
        - PMP Sales Oppurtunity
        - WiMAX Backhaul Capicity
        - PMP Backhaul Capicity
        - Current Alarm (WiMAX, PMP, PTP BH and All)
        - Network Latency (WiMAX, PMP, PTP BH and All)
        - Packet Drop (WiMAX, PMP, PTP BH and All)
        - Temperature (WiMAX, PMP, PTP BH and All)
        - PTP RAP Backhaul
        - City Charter
        - MFR Cause Code
        - MFR Processed
    """
    template_name = 'main_dashboard/home.html'

    def get(self, request):
        """
        Handles the get request

        :param request:
        :return Http response object:
        """
        mfr_cause_code_chart = self.get_mfr_cause_code_chart_results()

        mfr_processed_chart = self.get_mfr_processed_chart_results()

        return render(self.request, self.template_name, dictionary=dict(
                mfr_cause_code_chart = json.dumps(mfr_cause_code_chart),
                mfr_processed_chart = json.dumps(mfr_processed_chart),
            )
        )

    def get_mfr_cause_code_chart_results(self):

        mfr_reports = MFRDFRReports.objects.order_by('-process_for').filter(is_processed=1)

        if mfr_reports.exists():
            last_mfr_report = mfr_reports[0]
        else:
            return []

        chart_data = []
        results = MFRCauseCode.objects.filter(processed_for=last_mfr_report).values('processed_key', 'processed_value')
        for result in results:
            chart_data.append([
                "%s : %s" % (result['processed_key'], result['processed_value']),
                int(result['processed_value'])
            ])
        return chart_data

    def get_mfr_processed_chart_results(self):
        # Start Calculations for MFR Processed.
        # Last 12 Months
        year_before = datetime.date.today() - datetime.timedelta(days=365)
        year_before = datetime.date(year_before.year, year_before.month, 1)

        mfr_processed_results = MFRProcessed.objects.filter(processed_for__process_for__gte=year_before).values(
                'processed_key', 'processed_value', 'processed_for__process_for')

        day = year_before
        area_chart_categories = []
        processed_key_dict = {result['processed_key']: [] for result in mfr_processed_results}

        while day <= datetime.date.today():
            area_chart_categories.append(datetime.date.strftime(day, '%b %y'))

            processed_keys = processed_key_dict.keys()
            for result in mfr_processed_results:
                result_date = result['processed_for__process_for']
                if result_date.year == day.year and result_date.month == day.month:
                    processed_key_dict[result['processed_key']].append(int(result['processed_value']))
                    processed_keys.remove(result['processed_key'])

            # If no result is available for a processed_key put its value zero for (day.month, day.year)
            for key in processed_keys:
                processed_key_dict[key].append(0)

            day += relativedelta.relativedelta(months=1)

        area_chart_series = []
        for key, value in processed_key_dict.items():
            area_chart_series.append({'name': key, 'data': value})

        return {'categories': area_chart_categories, 'series': area_chart_series}

class WIMAX_Sector_Capacity(View):
    """
    The Class based View to get main dashboard page requested.

    """

    def get(self, request):
        """
        Handles the get request

        :param request:
        :return Http response object:
        """
        # data_source_config, technology, sector_method_to_call = self.get_wimax_init_data()
        technology = 'WIMAX'
        data_source_config = {
            'pmp1_ul_util_kpi': {'service_name': 'wimax_pmp1_ul_util_kpi', 'model': UtilizationStatus},
            'pmp1_dl_util_kpi': {'service_name': 'wimax_pmp1_dl_util_kpi', 'model': UtilizationStatus},
            'pmp2_ul_util_kpi': {'service_name': 'wimax_pmp2_ul_util_kpi', 'model': UtilizationStatus},
            'pmp2_dl_util_kpi': {'service_name': 'wimax_pmp2_dl_util_kpi', 'model': UtilizationStatus},
        }
        technology = DeviceTechnology.objects.get(name=technology).id
        sector_method_to_call = organization_sectors

        # Get User's organizations
        # (admin : organization + sub organization)
        # (operator + viewer : same organization)
        user_organizations = logged_in_user_organizations(self)

        # Get Sector of User's Organizations. [and are Sub Station]
        user_sector_list = sector_method_to_call(user_organizations, technology)

        port_dict = {
            'pmp1': ['pmp1_ul_util_kpi', 'pmp1_dl_util_kpi'],
            'pmp2': ['pmp2_ul_util_kpi', 'pmp2_dl_util_kpi'],
        }

        service_status_results = []
        for port in port_dict.keys():

            data_source_list = port_dict[port]

            user_sector = user_sector_list.filter(sector_configured_on_port__name__icontains=port)

            for data_source in data_source_list:
                # Get Service Name from queried data_source
                try:
                    service_name = data_source_config[data_source]['service_name']
                    model = data_source_config[data_source]['model']
                except KeyError as e:
                    continue

                # Get device of User's Organizations. [and are Sub Station]
                user_devices = Device.objects.filter(id__in=user_sector.\
                                values_list('sector_configured_on', flat=True))

                service_status_results += get_service_status_results(
                    user_devices, model=model, service_name=service_name, data_source=data_source
                )


        range_counter = get_dashboard_status_sector_range_counter(service_status_results)

        response_dict = get_pie_chart_json_response_sector_dict(data_source, range_counter)

        return HttpResponse(json.dumps(response_dict))


#********************************************** main dashboard sales opportunity ************************************************

class SalesOpportunityMixin(object):
    """
    Provide common method get for Performance Dashboard.

    To use this Mixin set `template_name` and implement method get_init_data to provide following attributes:

        - data_source_config
        - sector_method_to_call
        - devices_method_kwargs
    """

    def get(self, request):
        """
        Handles the get request

        :param request:
        :return Http response object:
        """
        is_bh = False
        tech = ['PMP', 'WiMAX']
        data_source_config, sector_method_to_call = self.get_init_data()

        data_source = data_source_config.keys()[0]
        # Get Service Name from queried data_source
        try:
            service_name = data_source_config[data_source]['service_name']
            model = data_source_config[data_source]['model']
        except KeyError as e:
            return render(self.request, self.template_name, dictionary=dict(data_source="", pie_chart=""))

        # Get User's organizations
        # (admin : organization + sub organization)
        # (operator + viewer : same organization)
        user_organizations = logged_in_user_organizations(self)

        result_dict = dict()
        for tech_name in tech:
            technology = DeviceTechnology.objects.get(name=tech_name).id
            # convert the data source in format topology_pmp/topology_wimax
            data_source = '%s-%s' % (data_source_config.keys()[0], tech_name.lower())
            try:
                dashboard_setting = DashboardSetting.objects.get(technology=technology, page_name='main_dashboard', name=data_source, is_bh=is_bh)
            except DashboardSetting.DoesNotExist as e:
                dashboard_setting = DashboardSetting.objects.none()

            # Get Sector of User's Organizations. [and are Sub Station]
            user_sector = sector_method_to_call(user_organizations, technology)
            # Get device of User's Organizations. [and are Sub Station]
            sector_devices = Device.objects.filter(id__in=user_sector.\
                            values_list('sector_configured_on', flat=True))

            service_status_results = get_topology_status_results(
                sector_devices, model=model, service_name=service_name, data_source=data_source, user_sector=user_sector
            )
            if dashboard_setting:
                range_counter = get_dashboard_status_range_counter(dashboard_setting, service_status_results)

                response_dict = get_pie_chart_json_response_dict(dashboard_setting, data_source, range_counter)
                result_dict.update({'%s_sales_opportunity' %(tech_name.lower()): json.dumps(response_dict)})

            if tech_name == 'PMP':
                sector_capacity = self.get_pmp_sector_capacity(sector_devices)
                if sector_capacity['success']:
                    result_dict.update({'%s_sector_capacity' %(tech_name.lower()): json.dumps(sector_capacity)})

            if tech_name == 'WiMAX':
                sector_capacity = self.get_wimax_sector_capacity(user_sector)
                if sector_capacity['success']:
                    result_dict.update({'%s_sector_capacity' %(tech_name.lower()): json.dumps(sector_capacity)})

        return render(self.request, self.template_name, dictionary=result_dict)


    def get_pmp_sector_capacity(self, sector_devices):
        """
        return the pie chart data for the pmp sector capacity.
        """
        pmp_data_source_config = {
            'cam_ul_util_kpi': {'service_name': 'cambium_ul_util_kpi', 'model': UtilizationStatus},
            'cam_dl_util_kpi': {'service_name': 'cambium_dl_util_kpi', 'model': UtilizationStatus},
        }

        data_source_list = pmp_data_source_config.keys()
        user_devices = sector_devices

        service_status_results = []
        for data_source in data_source_list:
            # Get Service Name from queried data_source
            service_name = pmp_data_source_config[data_source]['service_name']
            model = pmp_data_source_config[data_source]['model']

            service_status_results += get_service_status_results(
                user_devices, model=model, service_name=service_name, data_source=data_source
            )

        range_counter = get_dashboard_status_sector_range_counter(service_status_results)

        response_dict = get_pie_chart_json_response_sector_dict(data_source, range_counter)

        return response_dict

    def get_wimax_sector_capacity(self, user_sector):
        """
        return the pie chart data for the pmp sector capacity.
        """
        wimax_data_source_config = {
            'pmp1_ul_util_kpi': {'service_name': 'wimax_pmp1_ul_util_kpi', 'model': UtilizationStatus},
            'pmp1_dl_util_kpi': {'service_name': 'wimax_pmp1_dl_util_kpi', 'model': UtilizationStatus},
            'pmp2_ul_util_kpi': {'service_name': 'wimax_pmp2_ul_util_kpi', 'model': UtilizationStatus},
            'pmp2_dl_util_kpi': {'service_name': 'wimax_pmp2_dl_util_kpi', 'model': UtilizationStatus},
        }
        # Get Sector of User's Organizations. [and are Sub Station]
        user_sector_list = user_sector

        port_dict = {
            'pmp1': ['pmp1_ul_util_kpi', 'pmp1_dl_util_kpi'],
            'pmp2': ['pmp2_ul_util_kpi', 'pmp2_dl_util_kpi'],
        }

        service_status_results = []
        for port in port_dict.keys():

            data_source_list = port_dict[port]
            user_sector = user_sector_list.filter(sector_configured_on_port__name__icontains=port)

            for data_source in data_source_list:
                # Get Service Name from queried data_source
                service_name = wimax_data_source_config[data_source]['service_name']
                model = wimax_data_source_config[data_source]['model']

                # Get device of User's Organizations. [and are Sub Station]
                user_devices = Device.objects.filter(id__in=user_sector.\
                                values_list('sector_configured_on', flat=True))

                service_status_results += get_service_status_results(
                    user_devices, model=model, service_name=service_name, data_source=data_source
                )

        range_counter = get_dashboard_status_sector_range_counter(service_status_results)

        response_dict = get_pie_chart_json_response_sector_dict(data_source, range_counter)

        return response_dict


class Main_Sales_Opportunity(SalesOpportunityMixin, View):
    """
    The Class based View to get main dashboard page requested.

    """
    template_name = 'dashboard/sales_opportunity.html'

    def get_init_data(self):
        """
        Provide data for mixin's get method.
        """

        data_source_config = {
            'topology': {'service_name': 'topology', 'model': Topology},
        }
        sector_method_to_call = organization_sectors
        return data_source_config, sector_method_to_call

