SET FOREIGN_KEY_CHECKS=0;

drop table inventory_substation;
drop table inventory_sector;
drop table inventory_customer;
drop table inventory_circuit;
drop table inventory_basestation;
drop table inventory_backhaul;
drop table inventory_antenna;
drop table device_device;


CREATE TABLE `device_device` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`device_name` varchar(200) NOT NULL,
`device_alias` varchar(200) NOT NULL,
`machine_id` int(11) DEFAULT NULL,
`site_instance_id` int(11) DEFAULT NULL,
`organization_id` int(11) NOT NULL,
`device_technology` int(11) NOT NULL,
`device_vendor` int(11) NOT NULL,
`device_model` int(11) NOT NULL,
`device_type` int(11) NOT NULL,
`parent_id` int(11) DEFAULT NULL,
`ip_address` char(15) NOT NULL,
`mac_address` varchar(100) DEFAULT NULL,
`netmask` char(15) DEFAULT NULL,
`gateway` char(15) DEFAULT NULL,
`dhcp_state` varchar(200) NOT NULL,
`host_priority` varchar(200) NOT NULL,
`host_state` varchar(200) NOT NULL,
`latitude` double DEFAULT NULL,
`longitude` double DEFAULT NULL,
`timezone` varchar(100) NOT NULL,
`country` int(11) DEFAULT NULL,
`state` int(11) DEFAULT NULL,
`city` int(11) DEFAULT NULL,
`address` longtext,
`description` longtext,
`is_deleted` int(11) NOT NULL,
`is_added_to_nms` int(11) NOT NULL,
`is_monitored_on_nms` int(11) NOT NULL,
`lft` int(10) unsigned NOT NULL,
`rght` int(10) unsigned NOT NULL,
`tree_id` int(10) unsigned NOT NULL,
`level` int(10) unsigned NOT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `device_name` (`device_name`),
UNIQUE KEY `ip_address` (`ip_address`),
KEY `device_device_dbaea34e` (`machine_id`),
KEY `device_device_a74b81df` (`site_instance_id`),
KEY `device_device_de772da3` (`organization_id`),
KEY `device_device_410d0aac` (`parent_id`),
KEY `device_device_329f6fb3` (`lft`),
KEY `device_device_e763210f` (`rght`),
KEY `device_device_ba470c4a` (`tree_id`),
KEY `device_device_20e079f4` (`level`),
CONSTRAINT `machine_id_refs_id_b0012bcd` FOREIGN KEY (`machine_id`) REFERENCES `machine_machine` (`id`),
CONSTRAINT `organization_id_refs_id_0a0a8b43` FOREIGN KEY (`organization_id`) REFERENCES `organization_organization` (`id`),
CONSTRAINT `parent_id_refs_id_0679e3c1` FOREIGN KEY (`parent_id`) REFERENCES `device_device` (`id`),
CONSTRAINT `site_instance_id_refs_id_7810d5e5` FOREIGN KEY (`site_instance_id`) REFERENCES `site_instance_siteinstance` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `inventory_antenna` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(250) NOT NULL,
`alias` varchar(250) NOT NULL,
`antenna_type` varchar(100) DEFAULT NULL,
`height` double DEFAULT NULL,
`polarization` varchar(50) DEFAULT NULL,
`tilt` double DEFAULT NULL,
`gain` double DEFAULT NULL,
`mount_type` varchar(100) DEFAULT NULL,
`beam_width` double DEFAULT NULL,
`azimuth_angle` double DEFAULT NULL,
`reflector` varchar(100) DEFAULT NULL,
`splitter_installed` varchar(4) DEFAULT NULL,
`sync_splitter_used` varchar(4) DEFAULT NULL,
`make_of_antenna` varchar(40) DEFAULT NULL,
`description` longtext,
`organization_id` int(11) NOT NULL DEFAULT '1',
PRIMARY KEY (`id`),
UNIQUE KEY `name` (`name`),
KEY `inventory_antenna_de772da3` (`organization_id`),
CONSTRAINT `organization_id_refs_id_677e2570` FOREIGN KEY (`organization_id`) REFERENCES `organization_organization` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `inventory_backhaul` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(250) NOT NULL,
`alias` varchar(250) NOT NULL,
`bh_configured_on_id` int(11) DEFAULT NULL,
`bh_port_name` varchar(40) DEFAULT NULL,
`bh_port` int(11) DEFAULT NULL,
`bh_type` varchar(250) DEFAULT NULL,
`bh_switch_id` int(11) DEFAULT NULL,
`switch_port_name` varchar(40) DEFAULT NULL,
`switch_port` int(11) DEFAULT NULL,
`pop_id` int(11) DEFAULT NULL,
`pop_port_name` varchar(40) DEFAULT NULL,
`pop_port` int(11) DEFAULT NULL,
`aggregator_id` int(11) DEFAULT NULL,
`aggregator_port_name` varchar(40) DEFAULT NULL,
`aggregator_port` int(11) DEFAULT NULL,
`pe_hostname` varchar(250) DEFAULT NULL,
`pe_ip` char(15) DEFAULT NULL,
`bh_connectivity` varchar(40) DEFAULT NULL,
`bh_circuit_id` varchar(250) DEFAULT NULL,
`bh_capacity` int(11) DEFAULT NULL,
`ttsl_circuit_id` varchar(250) DEFAULT NULL,
`description` longtext,
`dr_site` varchar(150),
`organization_id` int(11) NOT NULL DEFAULT '1',
PRIMARY KEY (`id`),
UNIQUE KEY `name` (`name`),
KEY `inventory_backhaul_366352e4` (`bh_configured_on_id`),
KEY `inventory_backhaul_af705a25` (`bh_switch_id`),
KEY `inventory_backhaul_25fe84e8` (`pop_id`),
KEY `inventory_backhaul_3fedd201` (`aggregator_id`),
KEY `inventory_backhaul_de772da3` (`organization_id`),
CONSTRAINT `aggregator_id_refs_id_1a6887f3` FOREIGN KEY (`aggregator_id`) REFERENCES `device_device` (`id`),
CONSTRAINT `bh_configured_on_id_refs_id_1a6887f3` FOREIGN KEY (`bh_configured_on_id`) REFERENCES `device_device` (`id`),
CONSTRAINT `bh_switch_id_refs_id_1a6887f3` FOREIGN KEY (`bh_switch_id`) REFERENCES `device_device` (`id`),
CONSTRAINT `pop_id_refs_id_1a6887f3` FOREIGN KEY (`pop_id`) REFERENCES `device_device` (`id`),
CONSTRAINT `organization_id_refs_id_82871406` FOREIGN KEY (`organization_id`) REFERENCES `organization_organization` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `inventory_basestation` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(250) NOT NULL,
`alias` varchar(250) NOT NULL,
`bs_site_id` varchar(250) DEFAULT NULL,
`bs_site_type` varchar(100) DEFAULT NULL,
`bs_switch_id` int(11) DEFAULT NULL,
`backhaul_id` int(11) DEFAULT NULL,
`bs_type` varchar(40) DEFAULT NULL,
`bh_bso` varchar(40) DEFAULT NULL,
`hssu_used` varchar(40) DEFAULT NULL,
`latitude` double DEFAULT NULL,
`longitude` double DEFAULT NULL,
`infra_provider` varchar(100) DEFAULT NULL,
`gps_type` varchar(100) DEFAULT NULL,
`building_height` double DEFAULT NULL,
`tower_height` double DEFAULT NULL,
`country` int(11) DEFAULT NULL,
`state` int(11) DEFAULT NULL,
`city` int(11) DEFAULT NULL,
`address` longtext,
`description` longtext,
`organization_id` int(11) NOT NULL DEFAULT '1',
PRIMARY KEY (`id`),
UNIQUE KEY `name` (`name`),
KEY `inventory_basestation_2d94f56c` (`bs_switch_id`),
KEY `inventory_basestation_f4d00402` (`backhaul_id`),
KEY `inventory_basestation_de772da3` (`organization_id`),
CONSTRAINT `backhaul_id_refs_id_b88aec53` FOREIGN KEY (`backhaul_id`) REFERENCES `inventory_backhaul` (`id`),
CONSTRAINT `bs_switch_id_refs_id_519fe049` FOREIGN KEY (`bs_switch_id`) REFERENCES `device_device` (`id`),
CONSTRAINT `organization_id_refs_id_75df2c48` FOREIGN KEY (`organization_id`) REFERENCES `organization_organization` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `inventory_sector` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(250) NOT NULL,
`alias` varchar(250) NOT NULL,
`sector_id` varchar(250) DEFAULT NULL,
`base_station_id` int(11) DEFAULT NULL,
`bs_technology_id` int(11) DEFAULT NULL,
`sector_configured_on_id` int(11) DEFAULT NULL,
`sector_configured_on_port_id` int(11) DEFAULT NULL,
`antenna_id` int(11) DEFAULT NULL,
`mrc` varchar(4) DEFAULT NULL,
`tx_power` double DEFAULT NULL,
`rx_power` double DEFAULT NULL,
`rf_bandwidth` double DEFAULT NULL,
`frame_length` double DEFAULT NULL,
`cell_radius` double DEFAULT NULL,
`frequency_id` int(11) DEFAULT NULL,
`modulation` varchar(250) DEFAULT NULL,
`description` longtext,
`dr_site` varchar(150),
`organization_id` int(11) NOT NULL DEFAULT '1',
PRIMARY KEY (`id`),
UNIQUE KEY `name` (`name`),
KEY `inventory_sector_2ae13a96` (`base_station_id`),
KEY `inventory_sector_b75ab1be` (`bs_technology_id`),
KEY `inventory_sector_b01ef1b5` (`sector_configured_on_id`),
KEY `inventory_sector_597d1d65` (`sector_configured_on_port_id`),
KEY `inventory_sector_c42a47b3` (`antenna_id`),
KEY `inventory_sector_80359b49` (`frequency_id`),
KEY `inventory_sector_de772da3` (`organization_id`),
CONSTRAINT `antenna_id_refs_id_17c7ec16` FOREIGN KEY (`antenna_id`) REFERENCES `inventory_antenna` (`id`),
CONSTRAINT `base_station_id_refs_id_623a0db0` FOREIGN KEY (`base_station_id`) REFERENCES `inventory_basestation` (`id`),
CONSTRAINT `bs_technology_id_refs_id_353403d2` FOREIGN KEY (`bs_technology_id`) REFERENCES `device_devicetechnology` (`id`),
CONSTRAINT `frequency_id_refs_id_ce9d28af` FOREIGN KEY (`frequency_id`) REFERENCES `device_devicefrequency` (`id`),
CONSTRAINT `sector_configured_on_id_refs_id_589ca1cf` FOREIGN KEY (`sector_configured_on_id`) REFERENCES `device_device` (`id`),
CONSTRAINT `sector_configured_on_port_id_refs_id_52f2e9fd` FOREIGN KEY (`sector_configured_on_port_id`) REFERENCES `device_deviceport` (`id`),
CONSTRAINT `organization_id_refs_id_da99cdd1` FOREIGN KEY (`organization_id`) REFERENCES `organization_organization` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `inventory_substation` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(250) NOT NULL,
`alias` varchar(250) NOT NULL,
`device_id` int(11) NOT NULL,
`antenna_id` int(11) DEFAULT NULL,
`version` varchar(40) DEFAULT NULL,
`serial_no` varchar(250) DEFAULT NULL,
`building_height` double DEFAULT NULL,
`tower_height` double DEFAULT NULL,
`ethernet_extender` varchar(250) DEFAULT NULL,
`cable_length` double DEFAULT NULL,
`latitude` double DEFAULT NULL,
`longitude` double DEFAULT NULL,
`mac_address` varchar(100) DEFAULT NULL,
`country` int(11) DEFAULT NULL,
`state` int(11) DEFAULT NULL,
`city` int(11) DEFAULT NULL,
`address` longtext,
`description` longtext,
`organization_id` int(11) NOT NULL DEFAULT '1',
PRIMARY KEY (`id`),
UNIQUE KEY `name` (`name`),
KEY `inventory_substation_b6860804` (`device_id`),
KEY `inventory_substation_c42a47b3` (`antenna_id`),
KEY `inventory_substation_de772da3` (`organization_id`),
CONSTRAINT `antenna_id_refs_id_c73aea92` FOREIGN KEY (`antenna_id`) REFERENCES `inventory_antenna` (`id`),
CONSTRAINT `device_id_refs_id_b9846ee6` FOREIGN KEY (`device_id`) REFERENCES `device_device` (`id`),
CONSTRAINT `organization_id_refs_id_d968c5c7` FOREIGN KEY (`organization_id`) REFERENCES `organization_organization` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE `inventory_customer` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(250) NOT NULL,
`alias` varchar(250) NOT NULL,
`address` longtext,
`description` longtext,
`organization_id` int(11) NOT NULL DEFAULT '1',
PRIMARY KEY (`id`),
UNIQUE KEY `name` (`name`),
KEY `inventory_customer_de772da3` (`organization_id`),
CONSTRAINT `organization_id_refs_id_cfbc7962` FOREIGN KEY (`organization_id`) REFERENCES `organization_organization` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `inventory_circuit` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(250) NOT NULL,
`alias` varchar(250) NOT NULL,
`circuit_type` varchar(250) DEFAULT NULL,
`circuit_id` varchar(250) DEFAULT NULL,
`sector_id` int(11) DEFAULT NULL,
`customer_id` int(11) DEFAULT NULL,
`sub_station_id` int(11) DEFAULT NULL,
`qos_bandwidth` double DEFAULT NULL,
`dl_rssi_during_acceptance` varchar(100) DEFAULT NULL,
`dl_cinr_during_acceptance` varchar(100) DEFAULT NULL,
`jitter_value_during_acceptance` varchar(100) DEFAULT NULL,
`throughput_during_acceptance` varchar(100) DEFAULT NULL,
`date_of_acceptance` date DEFAULT NULL,
`description` longtext,
`organization_id` int(11) NOT NULL DEFAULT '1',
PRIMARY KEY (`id`),
UNIQUE KEY `name` (`name`),
KEY `inventory_circuit_663ed8c9` (`sector_id`),
KEY `inventory_circuit_09847825` (`customer_id`),
KEY `inventory_circuit_abc593bb` (`sub_station_id`),
KEY `inventory_circuit_de772da3` (`organization_id`),
CONSTRAINT `customer_id_refs_id_eba5adb0` FOREIGN KEY (`customer_id`) REFERENCES `inventory_customer` (`id`),
CONSTRAINT `sector_id_refs_id_1b7c0cea` FOREIGN KEY (`sector_id`) REFERENCES `inventory_sector` (`id`),
CONSTRAINT `sub_station_id_refs_id_eedc5892` FOREIGN KEY (`sub_station_id`) REFERENCES `inventory_substation` (`id`),
CONSTRAINT `organization_id_refs_id_619c1ddf` FOREIGN KEY (`organization_id`) REFERENCES `organization_organization` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




SET FOREIGN_KEY_CHECKS=1;