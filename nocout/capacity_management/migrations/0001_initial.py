# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SectorCapacityStatus'
        db.create_table(u'capacity_management_sectorcapacitystatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Sector'])),
            ('sector_sector_id', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=64, null=True, blank=True)),
            ('sector_capacity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('current_in_per', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('current_in_val', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('avg_in_per', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('avg_in_val', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('peak_in_per', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('peak_in_val', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('peak_in_timestamp', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('current_out_per', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('current_out_val', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('avg_out_per', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('avg_out_val', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('peak_out_per', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('peak_out_val', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('peak_out_timestamp', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sys_timestamp', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organization.Organization'])),
            ('severity', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'capacity_management', ['SectorCapacityStatus'])


    def backwards(self, orm):
        # Deleting model 'SectorCapacityStatus'
        db.delete_table(u'capacity_management_sectorcapacitystatus')


    models = {
        u'capacity_management.sectorcapacitystatus': {
            'Meta': {'ordering': "['-sys_timestamp']", 'object_name': 'SectorCapacityStatus'},
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avg_in_per': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avg_in_val': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avg_out_per': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avg_out_val': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'current_in_per': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'current_in_val': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'current_out_per': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'current_out_val': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Organization']"}),
            'peak_in_per': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'peak_in_timestamp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'peak_in_val': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'peak_out_per': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'peak_out_timestamp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'peak_out_val': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Sector']"}),
            'sector_capacity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sector_sector_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'severity': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'sys_timestamp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
        },
        u'command.command': {
            'Meta': {'object_name': 'Command'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'command_line': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'device.city': {
            'Meta': {'object_name': 'City'},
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.State']", 'null': 'True', 'blank': 'True'})
        },
        u'device.country': {
            'Meta': {'object_name': 'Country'},
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'device.device': {
            'Meta': {'ordering': "['machine']", 'object_name': 'Device'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.Country']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_alias': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'device_model': ('django.db.models.fields.IntegerField', [], {}),
            'device_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'device_technology': ('django.db.models.fields.IntegerField', [], {}),
            'device_type': ('django.db.models.fields.IntegerField', [], {}),
            'device_vendor': ('django.db.models.fields.IntegerField', [], {}),
            'dhcp_state': ('django.db.models.fields.CharField', [], {'default': "'Disable'", 'max_length': '200'}),
            'gateway': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'host_priority': ('django.db.models.fields.CharField', [], {'default': "'Normal'", 'max_length': '200'}),
            'host_state': ('django.db.models.fields.CharField', [], {'default': "'Enable'", 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'unique': 'True', 'max_length': '15'}),
            'is_added_to_nms': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'is_deleted': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'is_monitored_on_nms': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mac_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['machine.Machine']", 'null': 'True', 'blank': 'True'}),
            'netmask': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Organization']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'device_children'", 'null': 'True', 'to': u"orm['device.Device']"}),
            'ports': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['device.DevicePort']", 'null': 'True', 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'site_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site_instance.SiteInstance']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.State']", 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'Asia/Kolkata'", 'max_length': '100'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'device.devicefrequency': {
            'Meta': {'object_name': 'DeviceFrequency'},
            'color_hex_value': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'frequency_radius': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'device.devicemodel': {
            'Meta': {'object_name': 'DeviceModel'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'device_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['device.DeviceType']", 'null': 'True', 'through': u"orm['device.ModelType']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'device.deviceport': {
            'Meta': {'object_name': 'DevicePort'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'device.devicetechnology': {
            'Meta': {'object_name': 'DeviceTechnology'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'device_vendors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['device.DeviceVendor']", 'null': 'True', 'through': u"orm['device.TechnologyVendor']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'device.devicetype': {
            'Meta': {'object_name': 'DeviceType'},
            'agent_tag': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'device_gmap_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'device_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'device_port': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['device.DevicePort']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'normal_check_interval': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'packets': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pl_critical': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pl_warning': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rta_critical': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rta_warning': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['service.Service']", 'null': 'True', 'through': u"orm['device.DeviceTypeService']", 'blank': 'True'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'device.devicetypeservice': {
            'Meta': {'object_name': 'DeviceTypeService'},
            'device_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.DeviceType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['service.ServiceParameters']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['service.Service']"}),
            'service_data_sources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['service.ServiceDataSource']", 'through': u"orm['device.DeviceTypeServiceDataSource']", 'symmetrical': 'False'})
        },
        u'device.devicetypeservicedatasource': {
            'Meta': {'object_name': 'DeviceTypeServiceDataSource'},
            'critical': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'device_type_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.DeviceTypeService']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_data_sources': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['service.ServiceDataSource']"}),
            'warning': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'device.devicevendor': {
            'Meta': {'object_name': 'DeviceVendor'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'device_models': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['device.DeviceModel']", 'null': 'True', 'through': u"orm['device.VendorModel']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'device.modeltype': {
            'Meta': {'object_name': 'ModelType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.DeviceModel']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.DeviceType']"})
        },
        u'device.state': {
            'Meta': {'object_name': 'State'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.Country']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'device.technologyvendor': {
            'Meta': {'object_name': 'TechnologyVendor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'technology': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.DeviceTechnology']"}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.DeviceVendor']"})
        },
        u'device.vendormodel': {
            'Meta': {'object_name': 'VendorModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.DeviceModel']"}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.DeviceVendor']"})
        },
        u'inventory.antenna': {
            'Meta': {'object_name': 'Antenna'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'antenna_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'azimuth_angle': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beam_width': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gain': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'make_of_antenna': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'mount_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Organization']"}),
            'polarization': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'reflector': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'splitter_installed': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'sync_splitter_used': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'tilt': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'inventory.backhaul': {
            'Meta': {'object_name': 'Backhaul'},
            'aggregator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'backhaul_aggregator'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['device.Device']"}),
            'aggregator_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'aggregator_port_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'bh_capacity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bh_circuit_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'bh_configured_on': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'backhaul'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['device.Device']"}),
            'bh_connectivity': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'bh_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bh_port_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'bh_switch': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'backhaul_switch'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['device.Device']"}),
            'bh_type': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dr_site': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Organization']"}),
            'pe_hostname': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'pe_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'pop': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'backhaul_pop'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['device.Device']"}),
            'pop_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pop_port_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'switch_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'switch_port_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'ttsl_circuit_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'inventory.basestation': {
            'Meta': {'ordering': "['city', 'state']", 'object_name': 'BaseStation'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'backhaul': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['inventory.Backhaul']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'bh_bso': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'bh_capacity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bh_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bh_port_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'bs_site_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'bs_site_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bs_switch': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bs_switch'", 'null': 'True', 'to': u"orm['device.Device']"}),
            'bs_type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'building_height': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.Country']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gps_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hssu_used': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infra_provider': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'maintenance_status': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Organization']"}),
            'provisioning_status': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.State']", 'null': 'True', 'blank': 'True'}),
            'tag1': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'tag2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'tower_height': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'inventory.sector': {
            'Meta': {'object_name': 'Sector'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'antenna': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'antenna'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['inventory.Antenna']"}),
            'base_station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sector'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['inventory.BaseStation']"}),
            'bs_technology': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.DeviceTechnology']", 'null': 'True', 'blank': 'True'}),
            'cell_radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dr_configured_on': ('django.db.models.fields.related.ForeignKey', [], {'max_length': '250', 'related_name': "'dr_configured_on'", 'null': 'True', 'blank': 'True', 'to': u"orm['device.Device']"}),
            'dr_site': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'frame_length': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.DeviceFrequency']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modulation': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'mrc': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Organization']"}),
            'planned_frequency': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'rf_bandwidth': ('django.db.models.fields.FloatField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'rx_power': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sector_configured_on': ('django.db.models.fields.related.ForeignKey', [], {'max_length': '250', 'related_name': "'sector_configured_on'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['device.Device']"}),
            'sector_configured_on_port': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['device.DevicePort']", 'null': 'True', 'blank': 'True'}),
            'sector_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'tx_power': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'machine.machine': {
            'Meta': {'object_name': 'Machine'},
            'agent_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'organization.organization': {
            'Meta': {'object_name': 'Organization'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'organization_children'", 'null': 'True', 'to': u"orm['organization.Organization']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'service.protocol': {
            'Meta': {'object_name': 'Protocol'},
            'auth_password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'auth_protocol': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'port': ('django.db.models.fields.IntegerField', [], {}),
            'private_pass_phase': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'private_phase': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'protocol_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'read_community': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'security_level': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'security_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'write_community': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'service.service': {
            'Meta': {'object_name': 'Service'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'command': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['command.Command']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parameters': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['service.ServiceParameters']"}),
            'service_data_sources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['service.ServiceDataSource']", 'through': u"orm['service.ServiceSpecificDataSource']", 'symmetrical': 'False'})
        },
        u'service.servicedatasource': {
            'Meta': {'object_name': 'ServiceDataSource'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'chart_color': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'chart_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'critical': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'data_source_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'formula': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'show_gis': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_max': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_min': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'valuesuffix': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'valuetext': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'warning': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'service.serviceparameters': {
            'Meta': {'object_name': 'ServiceParameters'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_check_attempts': ('django.db.models.fields.IntegerField', [], {}),
            'normal_check_interval': ('django.db.models.fields.IntegerField', [], {}),
            'parameter_description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'protocol': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['service.Protocol']"}),
            'retry_check_interval': ('django.db.models.fields.IntegerField', [], {})
        },
        u'service.servicespecificdatasource': {
            'Meta': {'object_name': 'ServiceSpecificDataSource'},
            'critical': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['service.Service']"}),
            'service_data_sources': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['service.ServiceDataSource']"}),
            'warning': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'site_instance.siteinstance': {
            'Meta': {'object_name': 'SiteInstance'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_status_tcp_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['machine.Machine']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'web_service_port': ('django.db.models.fields.IntegerField', [], {'default': '80'})
        }
    }

    complete_apps = ['capacity_management']