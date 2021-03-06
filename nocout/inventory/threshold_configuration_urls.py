from django.conf.urls import patterns, url
from inventory import views

urlpatterns = patterns('',
  url(r'^$', views.ThresholdConfigurationList.as_view(), name='threshold_configuration_list'),
  url(r'^(?P<pk>\d+)/$', views.ThresholdConfigurationDetail.as_view(), name='threshold_configuration_detail'),
  url(r'^new/$', views.ThresholdConfigurationCreate.as_view(), name='threshold_configuration_new'),
  url(r'^(?P<pk>\d+)/edit/$', views.ThresholdConfigurationUpdate.as_view(), name='threshold_configuration_edit'),
  url(r'^(?P<pk>\d+)/delete/$', views.ThresholdConfigurationDelete.as_view(), name='threshold_configuration_delete'),
  url(r'^ThresholdConfigurationlistingtable/(?P<technology>\w+)$', views.ThresholdConfigurationListingTable.as_view(), name='ThresholdConfigurationListingTable'),
)
