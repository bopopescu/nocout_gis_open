from django.conf.urls import url
import api

urlpatterns = [
	url(r'^get_data_source_save/$', api.CustomDashboardCreate.as_view(),name='create_custom_db'),
	url(r'^get_data_source_list/$', api.CustomDashboardList.as_view(),name='list_custom_db'),   
	url(r'^get_data_source_delete/$', api.CustomDashboardDelete.as_view(),name='delete_ds'),
	url(r'^ping_stability_testing/$', api.StartPingStabilityTest.as_view(),name='start_ping_stability_test'),
]