"""
========================================================
Module contains base url configuration for 'device' app.
========================================================

Location:
* /nocout_gis/nocout/device/urls.py
"""

# Caching GIS maps.
from django.views.decorators.cache import cache_page
from django.conf.urls import patterns, url
from device import views, api

urlpatterns = patterns('',
                       url(r'^$', views.DeviceList.as_view(), name='device_list'),
                       url(r'^(?P<pk>\d+)/$', views.DeviceDetail.as_view(), name='device_detail'),
                       url(r'^new/$', views.DeviceCreate.as_view(), name='device_new'),
                       url(r'^(?P<pk>\d+)/edit/$', views.DeviceUpdate.as_view(), name='device_edit'),
                       url(r'^(?P<pk>\d+)/delete/$', views.DeviceDelete.as_view(), name='device_delete'),

                       # url(r'^stats/$', cache_page(60 * 60)(api.DeviceStatsApi.as_view())),
                       url(r'^stats/$', api.DeviceStatsApi.as_view()),

                       # Cache the filters. They don't change.
                       url(r'^filter/(?P<for_map>\d+)/$', cache_page(60 * 60)(api.DeviceFilterApi.as_view())),

                       url(r'^lp_services/', api.LPServicesApi.as_view()),
                       url(r'^lp_service_data/', api.FetchLPDataApi.as_view()),
                       url(r'^lp_bulk_data/', api.BulkFetchLPDataApi.as_view()),
                       url(r'^ts_templates/', api.FetchThematicSettingsApi.as_view()),
                       url(r'^treeview/$', views.create_device_tree, name='device_tree_view'),
                       url(r'^operationaldevicelistingtable/', views.OperationalDeviceListingTable.as_view(),
                           name='OperationalDeviceListingTable'),
                       url(r'^nonoperationaldevicelistingtable/', views.NonOperationalDeviceListingTable.as_view(),
                           name='NonOperationalDeviceListingTable'),
                       url(r'^disableddevicelistingtable/', views.DisabledDeviceListingTable.as_view(),
                           name='DisabledDeviceListingTable'),
                       url(r'^archiveddevicelistingtable/', views.ArchivedDeviceListingTable.as_view(),
                           name='ArchivedDeviceListingTable'),
                       url(r'^alldevicelistingtable/', views.AllDeviceListingTable.as_view(),
                           name='AllDeviceListingTable'),

                       url(r'^select2/elements/$', views.SelectDeviceListView.as_view(),
                           name='select2-device-elements'),

                       url(r'^list/schedule/device/$', views.list_schedule_device, name='list-schedule-device'),
                       url(r'^select/schedule/device/$', views.select_schedule_device, name='select-schedule-device'),
                       url(r'^filter/selected/device/$', views.filter_selected_device, name='filter-selected-device/'),
                       )
