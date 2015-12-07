# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
        ('service', '0001_initial'),
        ('organization', '0001_initial'),
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Antenna',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Antenna Name')),
                ('alias', models.CharField(max_length=250, verbose_name=b'Antenna Alias')),
                ('antenna_type', models.CharField(max_length=100, null=True, verbose_name=b'Antenna Type', blank=True)),
                ('height', models.FloatField(help_text=b'(mtr) Enter a number.', null=True, verbose_name=b'Antenna Height', blank=True)),
                ('polarization', models.CharField(max_length=50, null=True, verbose_name=b'Polarization', blank=True)),
                ('tilt', models.FloatField(help_text=b'Enter a number.', null=True, verbose_name=b'Tilt', blank=True)),
                ('gain', models.FloatField(help_text=b'(dBi) Enter a number.', null=True, verbose_name=b'Gain', blank=True)),
                ('mount_type', models.CharField(max_length=100, null=True, verbose_name=b'Mount Type', blank=True)),
                ('beam_width', models.FloatField(help_text=b'Enter a number.', null=True, verbose_name=b'Beam Width', blank=True)),
                ('azimuth_angle', models.FloatField(help_text=b'Enter a number.', null=True, verbose_name=b'Azimuth Angle', blank=True)),
                ('reflector', models.CharField(max_length=100, null=True, verbose_name=b'Lens/Reflector', blank=True)),
                ('splitter_installed', models.CharField(max_length=4, null=True, verbose_name=b'Splitter Installed', blank=True)),
                ('sync_splitter_used', models.CharField(max_length=4, null=True, verbose_name=b'Sync Splitter User', blank=True)),
                ('make_of_antenna', models.CharField(max_length=40, null=True, verbose_name=b'Make Of Antenna', blank=True)),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('organization', models.ForeignKey(default=inventory.models.get_default_org, to='organization.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Backhaul',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Backhaul Name')),
                ('alias', models.CharField(max_length=250, verbose_name=b'Backhaul Alias')),
                ('bh_port_name', models.CharField(max_length=40, null=True, verbose_name=b' BH Port Name', blank=True)),
                ('bh_port', models.IntegerField(null=True, verbose_name=b'BH Port', blank=True)),
                ('bh_type', models.CharField(max_length=250, null=True, verbose_name=b'BH Type', blank=True)),
                ('switch_port_name', models.CharField(max_length=40, null=True, verbose_name=b'Switch Port Name', blank=True)),
                ('switch_port', models.IntegerField(null=True, verbose_name=b'Switch Port', blank=True)),
                ('pop_port_name', models.CharField(max_length=40, null=True, verbose_name=b'POP Port Name', blank=True)),
                ('pop_port', models.IntegerField(null=True, verbose_name=b'POP Port', blank=True)),
                ('aggregator_port_name', models.CharField(max_length=40, null=True, verbose_name=b'Aggregator Port Name', blank=True)),
                ('aggregator_port', models.IntegerField(null=True, verbose_name=b'Aggregator Port', blank=True)),
                ('pe_hostname', models.CharField(max_length=250, null=True, verbose_name=b'PE Hostname', blank=True)),
                ('pe_ip', models.IPAddressField(null=True, verbose_name=b'PE IP Address', blank=True)),
                ('bh_connectivity', models.CharField(max_length=40, null=True, verbose_name=b'BH Connectivity', blank=True)),
                ('bh_circuit_id', models.CharField(max_length=250, null=True, verbose_name=b'BH Circuit ID', blank=True)),
                ('bh_capacity', models.IntegerField(help_text=b'Enter a number.', null=True, verbose_name=b'BH Capacity', blank=True)),
                ('ttsl_circuit_id', models.CharField(max_length=250, null=True, verbose_name=b'TTSL Circuit ID', blank=True)),
                ('dr_site', models.CharField(max_length=150, null=True, verbose_name=b'DR Site', blank=True)),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('aggregator', models.ForeignKey(related_name='backhaul_aggregator', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='device.Device', null=True)),
                ('bh_configured_on', models.ForeignKey(related_name='backhaul', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='device.Device', null=True)),
                ('bh_switch', models.ForeignKey(related_name='backhaul_switch', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='device.Device', null=True)),
                ('organization', models.ForeignKey(default=inventory.models.get_default_org, to='organization.Organization')),
                ('pop', models.ForeignKey(related_name='backhaul_pop', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='device.Device', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BaseStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Name')),
                ('alias', models.CharField(max_length=250, verbose_name=b'Alias')),
                ('bs_site_id', models.CharField(max_length=250, null=True, verbose_name=b'BS Site ID', blank=True)),
                ('bs_site_type', models.CharField(max_length=100, null=True, verbose_name=b'BS Site Type', blank=True)),
                ('bh_port_name', models.CharField(max_length=40, null=True, verbose_name=b' BH Port Name', blank=True)),
                ('bh_port', models.IntegerField(null=True, verbose_name=b'BH Port', blank=True)),
                ('bh_capacity', models.IntegerField(help_text=b'Enter a number.', null=True, verbose_name=b'BH Capacity', blank=True)),
                ('bs_type', models.CharField(max_length=40, null=True, verbose_name=b'BS Type', blank=True)),
                ('bh_bso', models.CharField(max_length=40, null=True, verbose_name=b'BH BSO', blank=True)),
                ('hssu_used', models.CharField(max_length=40, null=True, verbose_name=b'HSSU Used', blank=True)),
                ('hssu_port', models.CharField(max_length=40, null=True, verbose_name=b'HSSU Port', blank=True)),
                ('latitude', models.FloatField(null=True, verbose_name=b'Latitude', blank=True)),
                ('longitude', models.FloatField(null=True, verbose_name=b'Longitude', blank=True)),
                ('infra_provider', models.CharField(max_length=100, null=True, verbose_name=b'Infra Provider', blank=True)),
                ('gps_type', models.CharField(max_length=100, null=True, verbose_name=b'GPS Type', blank=True)),
                ('building_height', models.FloatField(help_text=b'(mtr) Enter a number.', null=True, verbose_name=b'Building Height', blank=True)),
                ('tower_height', models.FloatField(help_text=b'(mtr) Enter a number.', null=True, verbose_name=b'Tower Height', blank=True)),
                ('address', models.TextField(null=True, verbose_name=b'Address', blank=True)),
                ('maintenance_status', models.CharField(max_length=250, null=True, verbose_name=b'Maintenance Status', blank=True)),
                ('provisioning_status', models.CharField(max_length=250, null=True, verbose_name=b'Provisioning Status', blank=True)),
                ('tag1', models.CharField(max_length=60, null=True, verbose_name=b'Tag 1', blank=True)),
                ('tag2', models.CharField(max_length=60, null=True, verbose_name=b'Tag 2', blank=True)),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('backhaul', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='inventory.Backhaul', null=True)),
                ('bs_switch', models.ForeignKey(related_name='bs_switch', blank=True, to='device.Device', null=True)),
                ('city', models.ForeignKey(blank=True, to='device.City', null=True)),
                ('country', models.ForeignKey(blank=True, to='device.Country', null=True)),
                ('organization', models.ForeignKey(default=inventory.models.get_default_org, to='organization.Organization')),
                ('state', models.ForeignKey(blank=True, to='device.State', null=True)),
            ],
            options={
                'ordering': ['city', 'state'],
            },
        ),
        migrations.CreateModel(
            name='Circuit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Name')),
                ('alias', models.CharField(max_length=250, verbose_name=b'Alias')),
                ('circuit_type', models.CharField(max_length=250, null=True, verbose_name=b'Type', blank=True)),
                ('circuit_id', models.CharField(max_length=250, null=True, verbose_name=b'Circuit ID', blank=True)),
                ('qos_bandwidth', models.FloatField(help_text=b'(kbps) Enter a number.', null=True, verbose_name=b'QOS(BW)', blank=True)),
                ('dl_rssi_during_acceptance', models.CharField(max_length=100, null=True, verbose_name=b'RSSI During Acceptance', blank=True)),
                ('dl_cinr_during_acceptance', models.CharField(max_length=100, null=True, verbose_name=b'CINR During Acceptance', blank=True)),
                ('jitter_value_during_acceptance', models.CharField(max_length=100, null=True, verbose_name=b'Jitter Value During Acceptance', blank=True)),
                ('throughput_during_acceptance', models.CharField(max_length=100, null=True, verbose_name=b'Throughput During Acceptance', blank=True)),
                ('date_of_acceptance', models.DateField(null=True, verbose_name=b'Date of Acceptance', blank=True)),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CircuitL2Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Name')),
                ('file_name', models.FileField(max_length=512, upload_to=inventory.models.uploaded_report_name)),
                ('added_on', models.DateTimeField(auto_now_add=True, verbose_name=b'Added On', null=True)),
                ('type_id', models.IntegerField(verbose_name=b'Type ID')),
                ('is_public', models.BooleanField(default=True, verbose_name=b'Is Public')),
                ('report_type', models.CharField(max_length=15, verbose_name=b'Type')),
                ('user_id', models.ForeignKey(to='user_profile.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Name')),
                ('alias', models.CharField(max_length=250, verbose_name=b'Alias')),
                ('address', models.TextField(null=True, verbose_name=b'Address', blank=True)),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('organization', models.ForeignKey(default=inventory.models.get_default_org, to='organization.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='GISExcelDownload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_path', models.CharField(max_length=250, null=True, verbose_name=b'Inventory File', blank=True)),
                ('status', models.IntegerField(null=True, verbose_name=b'Status', blank=True)),
                ('base_stations', models.CharField(max_length=250, null=True, verbose_name=b'Base Stations', blank=True)),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('downloaded_by', models.CharField(max_length=100, null=True, verbose_name=b'Downloaded By', blank=True)),
                ('added_on', models.DateTimeField(null=True, verbose_name=b'Added On', blank=True)),
                ('modified_on', models.DateTimeField(null=True, verbose_name=b'Modified On', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GISInventoryBulkImport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_filename', models.CharField(max_length=250, null=True, verbose_name=b'Inventory', blank=True)),
                ('valid_filename', models.CharField(max_length=250, null=True, verbose_name=b'Valid', blank=True)),
                ('invalid_filename', models.CharField(max_length=250, null=True, verbose_name=b'Invalid', blank=True)),
                ('status', models.IntegerField(null=True, verbose_name=b'Status', blank=True)),
                ('sheet_name', models.CharField(max_length=100, null=True, verbose_name=b'Sheet Name', blank=True)),
                ('technology', models.CharField(max_length=40, null=True, verbose_name=b'Technology', blank=True)),
                ('upload_status', models.IntegerField(null=True, verbose_name=b'Upload Status', blank=True)),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('uploaded_by', models.CharField(max_length=100, null=True, verbose_name=b'Uploaded By', blank=True)),
                ('added_on', models.DateTimeField(null=True, verbose_name=b'Added On', blank=True)),
                ('modified_on', models.DateTimeField(null=True, verbose_name=b'Modified On', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='IconSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Name')),
                ('alias', models.CharField(max_length=250, verbose_name=b'Alias')),
                ('upload_image', models.ImageField(upload_to=inventory.models.uploaded_file_name)),
            ],
        ),
        migrations.CreateModel(
            name='LivePollingSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Name')),
                ('alias', models.CharField(max_length=250, verbose_name=b'Alias')),
                ('data_source', models.ForeignKey(to='service.ServiceDataSource')),
                ('service', models.ForeignKey(to='service.Service')),
                ('technology', models.ForeignKey(to='device.DeviceTechnology')),
            ],
        ),
        migrations.CreateModel(
            name='PingThematicSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Name')),
                ('alias', models.CharField(max_length=250, verbose_name=b'Alias')),
                ('service', models.CharField(max_length=250, verbose_name=b'Service')),
                ('data_source', models.CharField(max_length=250, verbose_name=b'Data Source')),
                ('range1_start', models.CharField(max_length=20, null=True, verbose_name=b'Range1 Start', blank=True)),
                ('range1_end', models.CharField(max_length=20, null=True, verbose_name=b'Range1 End', blank=True)),
                ('range2_start', models.CharField(max_length=20, null=True, verbose_name=b'Range2 Start', blank=True)),
                ('range2_end', models.CharField(max_length=20, null=True, verbose_name=b'Range2 End', blank=True)),
                ('range3_start', models.CharField(max_length=20, null=True, verbose_name=b'Range3 Start', blank=True)),
                ('range3_end', models.CharField(max_length=20, null=True, verbose_name=b'Range3 End', blank=True)),
                ('range4_start', models.CharField(max_length=20, null=True, verbose_name=b'Range4 Start', blank=True)),
                ('range4_end', models.CharField(max_length=20, null=True, verbose_name=b'Range4 End', blank=True)),
                ('range5_start', models.CharField(max_length=20, null=True, verbose_name=b'Range5 Start', blank=True)),
                ('range5_end', models.CharField(max_length=20, null=True, verbose_name=b'Range5 End', blank=True)),
                ('range6_start', models.CharField(max_length=20, null=True, verbose_name=b'Range6 Start', blank=True)),
                ('range6_end', models.CharField(max_length=20, null=True, verbose_name=b'Range6 End', blank=True)),
                ('range7_start', models.CharField(max_length=20, null=True, verbose_name=b'Range7 Start', blank=True)),
                ('range7_end', models.CharField(max_length=20, null=True, verbose_name=b'Range7 End', blank=True)),
                ('range8_start', models.CharField(max_length=20, null=True, verbose_name=b'Range8 Start', blank=True)),
                ('range8_end', models.CharField(max_length=20, null=True, verbose_name=b'Range8 End', blank=True)),
                ('range9_start', models.CharField(max_length=20, null=True, verbose_name=b'Range9 Start', blank=True)),
                ('range9_end', models.CharField(max_length=20, null=True, verbose_name=b'Range9 End', blank=True)),
                ('range10_start', models.CharField(max_length=20, null=True, verbose_name=b'Range10 Start', blank=True)),
                ('range10_end', models.CharField(max_length=20, null=True, verbose_name=b'Range10 End', blank=True)),
                ('icon_settings', models.TextField(default=b'NULL')),
                ('is_global', models.BooleanField(default=False, verbose_name=b'Global Setting')),
                ('technology', models.ForeignKey(to='device.DeviceTechnology')),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Name')),
                ('alias', models.CharField(max_length=250, verbose_name=b'Alias')),
                ('sector_id', models.CharField(max_length=250, null=True, verbose_name=b'Sector ID', blank=True)),
                ('dr_site', models.CharField(max_length=150, null=True, verbose_name=b'DR Site', blank=True)),
                ('mrc', models.CharField(max_length=4, null=True, verbose_name=b'MRC', blank=True)),
                ('tx_power', models.FloatField(help_text=b'(dB) Enter a number.', null=True, verbose_name=b'TX Power', blank=True)),
                ('rx_power', models.FloatField(help_text=b'(dB) Enter a number.', null=True, verbose_name=b'RX Power', blank=True)),
                ('rf_bandwidth', models.FloatField(help_text=b'(kbps) Enter a number.', max_length=250, null=True, verbose_name=b'RF Bandwidth', blank=True)),
                ('frame_length', models.FloatField(help_text=b'(mtr) Enter a number.', null=True, verbose_name=b'Frame Length', blank=True)),
                ('cell_radius', models.FloatField(help_text=b'(mtr) Enter a number.', null=True, verbose_name=b'Cell Radius', blank=True)),
                ('planned_frequency', models.CharField(max_length=250, null=True, verbose_name=b'Planned Frequency', blank=True)),
                ('modulation', models.CharField(max_length=250, null=True, verbose_name=b'Modulation', blank=True)),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('antenna', models.ForeignKey(related_name='antenna', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='inventory.Antenna', null=True)),
                ('base_station', models.ForeignKey(related_name='sector', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='inventory.BaseStation', null=True)),
                ('bs_technology', models.ForeignKey(blank=True, to='device.DeviceTechnology', null=True)),
                ('dr_configured_on', models.ForeignKey(related_name='dr_configured_on', blank=True, to='device.Device', max_length=250, null=True)),
                ('frequency', models.ForeignKey(blank=True, to='device.DeviceFrequency', null=True)),
                ('organization', models.ForeignKey(default=inventory.models.get_default_org, to='organization.Organization')),
                ('sector_configured_on', models.ForeignKey(related_name='sector_configured_on', on_delete=django.db.models.deletion.SET_NULL, to='device.Device', max_length=250, null=True)),
                ('sector_configured_on_port', models.ForeignKey(blank=True, to='device.DevicePort', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Name')),
                ('alias', models.CharField(max_length=250, verbose_name=b'Alias')),
                ('version', models.CharField(max_length=40, null=True, verbose_name=b'Version', blank=True)),
                ('serial_no', models.CharField(max_length=250, null=True, verbose_name=b'Serial No.', blank=True)),
                ('building_height', models.FloatField(help_text=b'(mtr) Enter a number.', null=True, verbose_name=b'Building Height', blank=True)),
                ('tower_height', models.FloatField(help_text=b'(mtr) Enter a number.', null=True, verbose_name=b'Tower Height', blank=True)),
                ('ethernet_extender', models.CharField(max_length=250, null=True, verbose_name=b'Ethernet Extender', blank=True)),
                ('cable_length', models.FloatField(help_text=b'(mtr) Enter a number.', null=True, verbose_name=b'Cable Length', blank=True)),
                ('latitude', models.FloatField(null=True, verbose_name=b'Latitude', blank=True)),
                ('longitude', models.FloatField(null=True, verbose_name=b'Longitude', blank=True)),
                ('mac_address', models.CharField(max_length=100, null=True, verbose_name=b'MAC Address', blank=True)),
                ('address', models.TextField(null=True, verbose_name=b'Address', blank=True)),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('antenna', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='inventory.Antenna', null=True)),
                ('city', models.ForeignKey(blank=True, to='device.City', null=True)),
                ('country', models.ForeignKey(blank=True, to='device.Country', null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='device.Device', null=True)),
                ('organization', models.ForeignKey(default=inventory.models.get_default_org, to='organization.Organization')),
                ('state', models.ForeignKey(blank=True, to='device.State', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThematicSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Name')),
                ('alias', models.CharField(max_length=250, verbose_name=b'Alias')),
                ('icon_settings', models.TextField(default=b'NULL')),
                ('is_global', models.BooleanField(default=False, verbose_name=b'Global Setting')),
            ],
        ),
        migrations.CreateModel(
            name='ThresholdConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name=b'Name')),
                ('alias', models.CharField(max_length=250, verbose_name=b'Alias')),
                ('service_type', models.CharField(default=b'INT', max_length=3, verbose_name=b'Service Type', choices=[(b'INT', b'Numeric'), (b'STR', b'String')])),
                ('range1_start', models.CharField(max_length=20, null=True, verbose_name=b'Range1 Start', blank=True)),
                ('range1_end', models.CharField(max_length=20, null=True, verbose_name=b'Range1 End', blank=True)),
                ('range2_start', models.CharField(max_length=20, null=True, verbose_name=b'Range2 Start', blank=True)),
                ('range2_end', models.CharField(max_length=20, null=True, verbose_name=b'Range2 End', blank=True)),
                ('range3_start', models.CharField(max_length=20, null=True, verbose_name=b'Range3 Start', blank=True)),
                ('range3_end', models.CharField(max_length=20, null=True, verbose_name=b'Range3 End', blank=True)),
                ('range4_start', models.CharField(max_length=20, null=True, verbose_name=b'Range4 Start', blank=True)),
                ('range4_end', models.CharField(max_length=20, null=True, verbose_name=b'Range4 End', blank=True)),
                ('range5_start', models.CharField(max_length=20, null=True, verbose_name=b'Range5 Start', blank=True)),
                ('range5_end', models.CharField(max_length=20, null=True, verbose_name=b'Range5 End', blank=True)),
                ('range6_start', models.CharField(max_length=20, null=True, verbose_name=b'Range6 Start', blank=True)),
                ('range6_end', models.CharField(max_length=20, null=True, verbose_name=b'Range6 End', blank=True)),
                ('range7_start', models.CharField(max_length=20, null=True, verbose_name=b'Range7 Start', blank=True)),
                ('range7_end', models.CharField(max_length=20, null=True, verbose_name=b'Range7 End', blank=True)),
                ('range8_start', models.CharField(max_length=20, null=True, verbose_name=b'Range8 Start', blank=True)),
                ('range8_end', models.CharField(max_length=20, null=True, verbose_name=b'Range8 End', blank=True)),
                ('range9_start', models.CharField(max_length=20, null=True, verbose_name=b'Range9 Start', blank=True)),
                ('range9_end', models.CharField(max_length=20, null=True, verbose_name=b'Range9 End', blank=True)),
                ('range10_start', models.CharField(max_length=20, null=True, verbose_name=b'Range10 Start', blank=True)),
                ('range10_end', models.CharField(max_length=20, null=True, verbose_name=b'Range10 End', blank=True)),
                ('live_polling_template', models.ForeignKey(to='inventory.LivePollingSettings')),
            ],
        ),
        migrations.CreateModel(
            name='UserPingThematicSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thematic_technology', models.ForeignKey(to='device.DeviceTechnology', null=True)),
                ('thematic_template', models.ForeignKey(to='inventory.PingThematicSettings')),
                ('user_profile', models.ForeignKey(to='user_profile.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='UserThematicSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thematic_technology', models.ForeignKey(to='device.DeviceTechnology', null=True)),
                ('thematic_template', models.ForeignKey(to='inventory.ThematicSettings')),
                ('user_profile', models.ForeignKey(to='user_profile.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='thematicsettings',
            name='threshold_template',
            field=models.ForeignKey(to='inventory.ThresholdConfiguration'),
        ),
        migrations.AddField(
            model_name='thematicsettings',
            name='user_profile',
            field=models.ManyToManyField(to='user_profile.UserProfile', through='inventory.UserThematicSettings'),
        ),
        migrations.AddField(
            model_name='pingthematicsettings',
            name='user_profile',
            field=models.ManyToManyField(to='user_profile.UserProfile', through='inventory.UserPingThematicSettings'),
        ),
        migrations.AddField(
            model_name='circuit',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='inventory.Customer', null=True),
        ),
        migrations.AddField(
            model_name='circuit',
            name='organization',
            field=models.ForeignKey(default=inventory.models.get_default_org, to='organization.Organization'),
        ),
        migrations.AddField(
            model_name='circuit',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='inventory.Sector', null=True),
        ),
        migrations.AddField(
            model_name='circuit',
            name='sub_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='inventory.SubStation', null=True),
        ),
    ]
