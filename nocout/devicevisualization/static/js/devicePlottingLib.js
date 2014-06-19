/*Global Variables*/
var mapInstance = "",
	that = "",
	currentDomElement = "",
	oms = "",
	pathConnector = "",
	infowindow = "",
	devicesObject = {},
	metaData = {},
	hitCounter = 1,
	showLimit = 0,
	devicesCount = 0,
	remainingDevices = 0,
	cityArray = [],
	stateArray = [],
	vendorArray = [],
	techArray = [],
	devices = [],
	masterMarkersObj = [],
	slaveMarkersObj = [],
	pathLineArray = [],
	counter = -999,
	totalCalls = 1,
	clusterIcon = "",
	masterClusterInstance = "",
	slaveClusterInstance = "",
	polygonSelectedDevices = [],
	pathArray = [],
	polygon = "",
	pointsArray = [],
	currentPolygon = {},
	drawingManager = "",
	dataArray = [],
	leftMargin = 0,
	sectorArray = [],
	circleArray = [],
	arrayCounter = 0,
	latLongArray = [],
	depthStep = 6,
	fr = 900, //MHZ
	sol = 299792458,
	HEIGHT_CHANGED = false,
	clear_factor = 100,
	antenaHight1 = 40.0,
	antenaHight2 = 45.0,
	pinPointsColor = 'rgb(170,102,102)',
	altitudeColor = '#EDC240',
	losColor = 'rgb(203,75,75)',
	fresnel1Color = 'rgba(82, 172, 82, 0.99)',
	fresnel2Color = 'rgb(148,64,237)';

/**
 * This class is used to plot the BS & SS on the google maps & show information on click
 * @class networkMap
 * @uses jQuery
 * @uses Google Maps
 * Coded By :- Yogender Purohit
 */
function networkMapClass() {

	/*Store the reference of current pointer in a global variable*/
	that = this;

	/**
	 * This function creates the base google map with the lat long of India
	 * @function createMap
	 * @class networkMap
	 * @param domElement "String" It the the dom element on which the map is to be create
	 */
	this.createMap = function(domElement) {

		/*Store the reference of current pointer in a global variable*/
		that = this;

		/*Save the dom element in the global variable*/
		currentDomElement = domElement;

		var mapObject = {
			center    : new google.maps.LatLng(21.1500,79.0900),
			zoom      : 5
		};    
		/*Create Map Type Object*/
		mapInstance = new google.maps.Map(document.getElementById(domElement),mapObject);

		/*Search text box object*/
		var searchTxt = document.getElementById('searchTxt');

		/*google search object for search text box*/
		var searchBox = new google.maps.places.SearchBox(searchTxt);

		/*Event listener for search text box*/
		google.maps.event.addListener(new google.maps.places.SearchBox(searchTxt), 'places_changed', function() {
			/*place object returned from map API*/
    		var places = searchBox.getPlaces();
    		/*initialize bounds object*/
    		var bounds = new google.maps.LatLngBounds();
    		/*point bounds to the place location*/
    		bounds.extend(places[0].geometry.location);
    		/*call fitbounts for the mapInstance with the place location bounds object*/
    		mapInstance.fitBounds(bounds)
    		/*Listener to reset zoom level if it exceeds to particular value*/
    		var listener = google.maps.event.addListener(mapInstance, "idle", function() { 
    			/*check for current zoom level*/
				if (mapInstance.getZoom() > 8) {
					mapInstance.setZoom(8);
				}
				google.maps.event.removeListener(listener);
			});
		});

		/*Create a instance of OverlappingMarkerSpiderfier*/
		oms = new OverlappingMarkerSpiderfier(mapInstance,{markersWontMove: true, markersWontHide: true});		

		/*Create a instance of google map info window*/
		infowindow = new google.maps.InfoWindow();		

		oms.addListener('click', function(marker,e) {
			
			var windowPosition = new google.maps.LatLng(marker.position.k,marker.position.A);
			/*Call the function to create info window content*/
			var content = that.makeWindowContent(marker);
			/*Set the content for infowindow*/
			infowindow.setContent(content);
			/*Set The Position for InfoWindow*/
			infowindow.setPosition(windowPosition);
			/*Open the info window*/
			infowindow.open(mapInstance);
		});
		/*Event when the markers cluster expands or spiderify*/
		oms.addListener('spiderfy', function(e,markers) {

			/*Change the markers icon from cluster icon to thrie own icon*/
			for(var i=0;i<e.length;i++) {
				e[i].setOptions({"icon":e[i].oldIcon});
			}

			infowindow.close();
		});
		/*Event when markers cluster is collapsed or unspiderify*/
		oms.addListener('unspiderfy', function(e,markers) {

			/*Reset the marker icon to cluster icon*/
			for(var i=0;i<e.length;i++) {
				e[i].setOptions({"icon":clusterIcon});
			}
		});
	};

	/**
	 * This function plots the BS & SS network on the created google map
	 * @function getDevicesData
	 * @class networkMap
	 */
	this.getDevicesData = function(username) {

		/*Store the reference of current pointer in a global variable*/
		that = this;

		if(counter > 0 || counter == -999) {
			/*Show The loading Icon*/
			$("#loadingIcon").show();

			/*Disable the refresh button*/
			$("#resetFilters").button("loading");

			/*To Enable The Cross Domain Request*/
			$.support.cors = true;
			
			/*Ajax call to the API*/
			$.ajax({
				crossDomain: true,
				// url : "../../device/stats/?username="+username+"&page_number="+hitCounter+"&limit="+showLimit,
				url : "../../static/new_format.json",
				type : "GET",
				dataType : "json",
				/*If data fetched successful*/
				success : function(result) {

					if(result.data.objects != null) {

						hitCounter = hitCounter + 1;
						/*First call case*/
						if(devicesObject.data == undefined) {

							/*Save the result json to the global variable for global access*/
							devicesObject = result;
							/**/
							devices = devicesObject.data.objects.children;
						} else {

							devices = devices.concat(result.data.objects.children);
						}

						/*Update the device count with the received data*/
						devicesCount = devicesObject.data.meta.total_count;

						/*Update the device count with the received data*/
						showLimit = devicesObject.data.meta.limit;

						if(counter == -999) {
							counter = Math.round(devicesCount/showLimit);
						}
						
						if(devicesObject.success == 1) {

							/*If cluster icon exist then save it to global variable else make the global variable blank*/
							if(devicesObject.data.objects.data.unspiderfy_icon == undefined) {
								clusterIcon = "";
							} else {
								clusterIcon = "../../"+devicesObject.data.objects.data.unspiderfy_icon;
							}

							/*Call the populateNetwork to show the markers on the map*/
							that.populateNetwork(devices);
							
							/*Call the getDevicesFilter function to seperate the filter values from the object array*/
							//that.getDevicesFilter(devices);

							/*Call the function after 3 sec.*/
							setTimeout(function() {
									
								that.getDevicesData(username);
							},3000);

						} else {

							that.recallServer();
						}
						/*Decrement the counter*/
						counter = counter - 1;

					} else {

						that.recallServer();
					}
				},
				/*If data not fetched*/
				error : function(err) {
					console.log(err.responseText);
					that.recallServer();
					console.log(err.statusText);
				}
			});
		} else {

			/*Recall the server after the defined time*/
			that.recallServer();
		}
	};

	/**
     * This function is used to populate the markers on the google maps
     * @class netowrkMap
     * @method populateNetwork
     * @param resultantMarkers [JSON Objet Array] It is the devies object array
	 */
	this.populateNetwork = function(resultantMarkers) {

		/*Store the reference of current pointer in a global variable*/
		that = this;

		/*Assign the potting devices to the 'devices' global variables*/
		devices = resultantMarkers;

		for(var i=0;i<resultantMarkers.length;i++) {

			var master_label_content = "";
			master_label_content = "<div class='labelContainer'>";

			for(var lbl=0;lbl<resultantMarkers[i].data.labels.length;lbl++) {

				if(resultantMarkers[i].data.labels[lbl].show == 1) {

					if($.trim(resultantMarkers[i].data.labels[lbl].position) == "up") {
						console.log(resultantMarkers[i].data.labels[lbl].show);
						master_label_content += "<div class='topLabel'>"+resultantMarkers[i].data.labels[lbl].name+" : "+resultantMarkers[i].data.labels[lbl].value+"</div>";
					} else if($.trim(resultantMarkers[i].data.labels[lbl].position) == "down") {
						master_label_content += "<div class='bottomLabel'>"+resultantMarkers[i].data.labels[lbl].name+" : "+resultantMarkers[i].data.labels[lbl].value+"</div>";
					}
				}
			}
			master_label_content += "</div>";

			/*Create Master Marker Object*/
			var masterMarkerObject = {
		    	position  	  : new google.maps.LatLng(resultantMarkers[i].data.lat,resultantMarkers[i].data.lon),
		    	map       	  : mapInstance,
		    	icon 	  	  : "../../"+resultantMarkers[i].data.markerUrl,//"https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=|fcfcfc|",
		    	oldIcon 	  : "../../"+resultantMarkers[i].data.markerUrl,
		    	pointType	  : "bs",
		    	labelContent  : master_label_content,
				labelAnchor   : new google.maps.Point(0, 62),
				labelClass    : "markerLabels",
				labelStyle	  : {opacity: 0.85},
				perf 		  : resultantMarkers[i].data.perf,
				dataset 	  : resultantMarkers[i].data.param.base_station,
				antena_height : resultantMarkers[i].data.antena_height
			};

			/*Create Master Marker*/
		    // var masterMarker = new google.maps.Marker(masterMarkerObject);
		    var masterMarker = new MarkerWithLabel(masterMarkerObject);
		    /*Add the master marker to the global master markers array*/
		    masterMarkersObj.push(masterMarker);
		    /*Add parent markers to the OverlappingMarkerSpiderfier*/
		    oms.addMarker(masterMarker);

		    /*Call createCircle function to create backhual circle around BS & SS pt.*/
	    	that.createCircle(resultantMarkers[i].data.lat,resultantMarkers[i].data.lon,resultantMarkers[i].data.circle_radius,resultantMarkers[i].data.circle_color,"backhual","bs",resultantMarkers[i].data.param.backhual);

		    var slaveCount = resultantMarkers[i].children.length;  
		    /*Loop for the number of slave & their links with the master*/
		    for(var j=0;j<slaveCount;j++) {

		    	var slave_label_content = "";
				slave_label_content = "<div class='labelContainer'>";

				for(var lbl=0;lbl<resultantMarkers[i].children[j].data.labels.length;lbl++) {

					if(resultantMarkers[i].children[j].data.labels[lbl].show == 1) {

						if($.trim(resultantMarkers[i].children[j].data.labels[lbl].position) == "up") {
							slave_label_content += "<div class='topLabel'>"+resultantMarkers[i].children[j].data.labels[lbl].name+" : "+resultantMarkers[i].children[j].data.labels[lbl].value+"</div>";
						} else if($.trim(resultantMarkers[i].children[j].data.labels[lbl].position) == "down") {
							slave_label_content += "<div class='bottomLabel'>"+resultantMarkers[i].children[j].data.labels[lbl].name+" : "+resultantMarkers[i].children[j].data.labels[lbl].value+"</div>";
						}
					}
				}
				slave_label_content += "</div>";

		    	/*Create Slave Marker Object*/
			    var slaveMarkerObject = {
			    	position  	  : new google.maps.LatLng(resultantMarkers[i].children[j].data.lat,resultantMarkers[i].children[j].data.lon),
			    	map       	  : mapInstance,
			    	icon 	  	  : "../../"+resultantMarkers[i].children[j].data.markerUrl,
			    	oldIcon 	  : "../../"+resultantMarkers[i].children[j].data.markerUrl,
			    	pointType	  : "ss",
			    	labelContent  : slave_label_content,
					labelAnchor   : new google.maps.Point(0, 62),
					labelClass    : "markerLabels",
					labelStyle	  : {opacity: 0.85},
					perf 		  : resultantMarkers[i].data.perf,
					dataset  	  : resultantMarkers[i].children[j].data.param.sub_station,
					antena_height : resultantMarkers[i].children[j].data.antena_height
				};

				/*Create Slave Marker*/
			    // var slaveMarker = new google.maps.Marker(slaveMarkerObject);
			    var slaveMarker = new MarkerWithLabel(slaveMarkerObject);
			    /*Add the slave marker to the global slave array*/
		    	slaveMarkersObj.push(slaveMarker);
			    /*Add child markers to the OverlappingMarkerSpiderfier*/
				oms.addMarker(slaveMarker);

				/*Call createCircle function to create frequency circle around BS & SS pt.*/
	    		that.createCircle(resultantMarkers[i].children[j].data.lat,resultantMarkers[i].children[j].data.lon,resultantMarkers[i].children[j].data.circle_radius,resultantMarkers[i].children[j].data.circle_color,"frequency","ss",resultantMarkers[i].children[j].data.param.backhual);

				/*Call createCircle function to create the circle aroung BS & SS pt.*/
	    		that.createCircle(resultantMarkers[i].children[j].data.lat,resultantMarkers[i].children[j].data.lon,resultantMarkers[i].children[j].data.circle_radius,resultantMarkers[i].children[j].data.circle_color,"backhual","ss",resultantMarkers[i].children[j].data.param.backhual);

				var pathDataObject = [];
				/*If device are of P2P type*/
				if(resultantMarkers[i].type == "P2P") {
					/*Create object for Link Line Between Master & Slave*/
					pathDataObject = [
						new google.maps.LatLng(resultantMarkers[i].data.lat,resultantMarkers[i].data.lon),
						new google.maps.LatLng(resultantMarkers[i].children[j].data.lat,resultantMarkers[i].children[j].data.lon)
					];
				} else {
					var lat = resultantMarkers[i].data.lat;
					var lon = resultantMarkers[i].data.lon;
					var rad = resultantMarkers[i].children[j].data.radius;
					var azimuth = resultantMarkers[i].children[j].data.azimuth_angle;
					var beam_width = resultantMarkers[i].children[j].data.beam_width;
					var sector_color = resultantMarkers[i].children[j].data.sector_color;
					var sectorDataset = resultantMarkers[i].children[j].data.param.sector_info;
					/*Call create sector function to plot the section.*/
					that.createSector(lat,lon,rad,azimuth,beam_width,sector_color,sectorDataset,function(sectorObj) {

						var halfPt = Math.floor(sectorObj.length / (+2));
						/*Create object for Link Line Between Master & Slave*/
						pathDataObject = [
							new google.maps.LatLng(sectorObj[halfPt].k,sectorObj[halfPt].A),
							new google.maps.LatLng(resultantMarkers[i].children[j].data.lat,resultantMarkers[i].children[j].data.lon)
						];
					});
				}

				if(resultantMarkers[i].children[j].data.show_link == 1) {

					var linkObject = {};

					linkObject = {
						path 				: pathDataObject,
						strokeColor			: resultantMarkers[i].children[j].data.link_color,
						strokeOpacity		: 1.0,
						strokeWeight		: 2,
						pointType 			: "path",
						geodesic			: true,
						ss_info				: resultantMarkers[i].children[j].data.param.sub_station,
						ss_lat 				: resultantMarkers[i].children[j].data.lat,
						ss_lon 				: resultantMarkers[i].children[j].data.lon,						
						ss_perf 			: resultantMarkers[i].children[j].data.perf,
						ss_height 			: resultantMarkers[i].children[j].data.antena_height,
						bs_lat 				: resultantMarkers[i].data.lat,
						bs_lon 				: resultantMarkers[i].data.lon,
						bs_perf 			: resultantMarkers[i].data.perf,
						bs_height 			: resultantMarkers[i].data.antena_height
					};

					if($.trim(resultantMarkers[i].type) == "P2P") {
						linkObject["bs_info"] = resultantMarkers[i].data.param.base_station;
					} else {
						linkObject["bs_info"] = resultantMarkers[i].children[j].data.param.sector_info;
					}

					pathConnector = new google.maps.Polyline(linkObject);
					/*Plot the link line between master & slave*/
					pathConnector.setMap(mapInstance);

					pathLineArray.push(pathConnector);

					/*Bind Click Event on Link Path Between Master & Slave*/
					google.maps.event.addListener(pathConnector, 'click', function(e) {

						/*Call the function to create info window content*/
						var content = that.makeWindowContent(this);
						/*Set the content for infowindow*/
						infowindow.setContent(content);
						/*Set The Position for InfoWindow*/
						infowindow.setPosition(e.latLng);
						/*Open the info window*/
						infowindow.open(mapInstance);
					});
				}/*SHOW_LINK condition ends*/
			}
		}
		
		var bsLatArray = [],
			bsLonArray = [],
			ssLatArray = [],
			ssLonArray = [];

		/*Get All BS Lat & Lon*/
		$.grep(masterMarkersObj,function(bs) {
			bsLatArray.push(bs.position.A);
			bsLonArray.push(bs.position.k);
		});

		/*Get All SS Lat & Lon*/
		$.grep(slaveMarkersObj,function(ss) {
			ssLatArray.push(ss.position.A);
			ssLonArray.push(ss.position.k);
		});

		/*Loop to change the icon for same location markers(to cluster icon)*/
		for(var k=0;k<masterMarkersObj.length;k++) {
			
			/*if two BS on same position*/
			var bsLatOccurence = $.grep(bsLatArray, function (elem) {return elem === masterMarkersObj[k].position.A;}).length;
			var bsLonOccurence = $.grep(bsLonArray, function (elem) {return elem === masterMarkersObj[k].position.k;}).length;
			if(bsLatOccurence > 1 && bsLonOccurence > 1) {
				masterMarkersObj[k].setOptions({"icon" : clusterIcon});
			}

			for(var l=0;l<slaveMarkersObj.length;l++) {
				
				/*if two BS on same position*/
				var ssLatOccurence = $.grep(ssLatArray, function (elem) {return elem === slaveMarkersObj[l].position.A;}).length;
				var ssLonOccurence = $.grep(ssLonArray, function (elem) {return elem === slaveMarkersObj[l].position.k;}).length;
				if(ssLatOccurence > 1 && ssLonOccurence > 1) {
					slaveMarkersObj[l].setOptions({"icon" : clusterIcon});
				}

				/*if some BS & SS are on same position*/
				var BS_SS_location = masterMarkersObj[k].position.A == slaveMarkersObj[l].position.A && masterMarkersObj[k].position.k == slaveMarkersObj[l].position.k;
				if(BS_SS_location) {
					slaveMarkersObj[l].setOptions({"icon" : clusterIcon});	
					masterMarkersObj[k].setOptions({"icon" : clusterIcon});
				}
			}
		}

		/*Cluster options object*/
		var clusterOptions = {gridSize: 70, maxZoom: 8};
		/*Add the master markers to the cluster MarkerCluster object*/
		masterClusterInstance = new MarkerClusterer(mapInstance, masterMarkersObj, clusterOptions);
		/*Add the slave markers to the cluster MarkerCluster object*/
		slaveClusterInstance = new MarkerClusterer(mapInstance, slaveMarkersObj, clusterOptions);
	};


	/**
	 * This function creates sectors on google maps.
	 * @class networkMapClass.
	 * @method createSector.
	 * @param Lat "Number", It contains lattitude of any point.
	 * @param Lng "Number", It contains longitude of any point.
	 * @param radius "Number", It contains radius for sector.
	 * @param azimuth "Number", It contains azimuth angle for sector.
	 * @param beamwidth "Number", It contains width for the sector.
	 * @param sectorData {JSON Object}, It contains sector info json object.
	 */
	this.createSector = function(lat,lng,radius,azimuth,beamWidth,bgColor,sectorData,callback) {

		// Degrees to radians
        var d2r = Math.PI / 180;
        //  Radians to degrees
        var r2d = 180 / Math.PI;
		
        var centerPoint = new google.maps.LatLng((+lat),(+lng));

        var PRlat = (radius/3963) * r2d; // using 3963 miles as earth's radius
        var PRlng = PRlat/Math.cos(lat*d2r);

        var PGpoints = [];
        // PGpoints.push(centerPoint);
        with(Math) {

			lat1 = (+lat) + (PRlat * cos( d2r * (azimuth - beamWidth/2 )));
			lon1 = (+lng) + (PRlng * sin( d2r * (azimuth - beamWidth/2 )));
			
			PGpoints.push( new google.maps.LatLng(lat1,lon1));

			lat2 = (+lat) + (PRlat * cos( d2r * (azimuth + beamWidth/2 )));
			lon2 = (+lng) + (PRlng * sin( d2r * (azimuth + beamWidth/2 )));
			
			var theta = 0;
			var gamma = d2r * (azimuth + beamWidth/2 );

			for (var a = 1; theta < gamma ; a++ ) {
				theta = d2r * (azimuth - beamWidth/2 +a);
				PGlon = (+lng) + (PRlng * sin( theta ));
				PGlat = (+lat) + (PRlat * cos( theta ));				
				PGpoints.push(new google.maps.LatLng($.trim(PGlat),$.trim(PGlon)));				
			}

			PGpoints.push( new google.maps.LatLng(lat2,lon2));
			PGpoints.push(centerPoint);
		}
		var poly = new google.maps.Polygon({
			map 		  : mapInstance,
			path 		  : PGpoints,
			strokeColor   : bgColor,
			fillColor 	  : bgColor,
			pointType	  : "sector",
			strokeOpacity : 0.5,
			strokeWeight  : 1,
			dataset 	  : sectorData
        });
        /*Push polygon to an array*/
		sectorArray.push(poly);

        poly.setMap(mapInstance);

        /*listener for click event of sector*/
		google.maps.event.addListener(poly,'click',function(p) {
			
			var windowPosition = new google.maps.LatLng(lat,lng);
			/*Call the function to create info window content*/
			var content = that.makeWindowContent(poly);
			/*Set the content for infowindow*/
			infowindow.setContent(content);
			/*Set The Position for InfoWindow*/
			infowindow.setPosition(windowPosition);
			/*Open the info window*/
			infowindow.open(mapInstance);
		});

        callback(PGpoints);
	};

	/**
	 * This function creates circle on the given lat lon of given radius
	 * @class networkMapClass.
	 * @method createCircle.
	 * @param Lat "Number", It contains lattitude of any point.
	 * @param Lng "Number", It contains longitude of any point.
	 * @param radius "Number", It contains radius for sector.
	 * @param bgColor "String", It contains bg color for circle.
	 * @param pType "String", It contains info about circle is plot for BH or frequency.
	 * @param dType "String", It contains info about circle is plot for SS or BS.
	 * @param bhData {JSON Object}, It contains JSON object of BH info data.
	 */
	this.createCircle = function(lat,lng,radius,bgColor,pType,dType,bhData) {

		var rad = 0,
			fOpacity = 0,
			sColor = "";
		if($.trim(pType) == "frequency") {
			rad = radius * 2;
			fOpacity = 0.7;
			sColor = bgColor;
		} else if($.trim(dType) == "ss") {
			rad = radius;
			fOpacity = 0.95;
			sColor = '000000';
		} else {
			rad = radius;
			fOpacity = 0.7;
			sColor = bgColor;
		}
		/*Make circle data object for devices*/
		var devicesCircleOptions = {
			strokeColor		: "#"+sColor,
			strokeOpacity	: 1.0,
			clickable		: true,
			strokeWeight	: 1,
			fillColor		: "#"+bgColor,
			fillOpacity		: fOpacity,
			pointType		: pType,
			map 			: mapInstance,
			center 			: new google.maps.LatLng(lat,lng),
			radius 			: rad,
			dataset 		: bhData
		};

		/*Make the circle on the device marker*/
		var deviceCircle = new google.maps.Circle(devicesCircleOptions);

		/*Add circle object to an array*/
		circleArray.push(deviceCircle);
		rad = 0;
		fOpacity = 0;
		sColor = "";
		if($.trim(pType) == "backhual") {
			/*listener for click event of circle*/
			google.maps.event.addListener(deviceCircle,'click',function(e) {
				
				var windowPosition = new google.maps.LatLng(lat,lng);
				/*Call the function to create info window content*/
				var content = that.makeWindowContent(deviceCircle);
				/*Set the content for infowindow*/
				infowindow.setContent(content);
				/*Set The Position for InfoWindow*/
				infowindow.setPosition(windowPosition);
				/*Open the info window*/
				infowindow.open(mapInstance);
			});
		}
	};

	/**
	 * This function creates the info window content for BS,SS & link path 
	 * @class networkMap
	 * @method makeWindowContent
	 * @param contentObject {JSON Object} It contains current pointer(this) information
	 * @return windowContent "String" It contains content to be shown on info window
	 */
	this.makeWindowContent = function(contentObject) {

		/*Store the reference of current pointer in a global variable*/
		that = this;

		var windowContent = "",
			infoTable =  "",
			perfContent = "",
			clickedType = $.trim(contentObject.pointType);

		/*True,if clicked on the link line*/
		if(clickedType == "path") {

			infoTable += "<table class='table table-bordered'><thead><th>BS-Sector Info</th><th>BS-Sector Perf</th><th>SS Info</th><th>SS Perf</th></thead><tbody>";
			infoTable += "<tr>";
			/*BS-Sector Info Start*/
			infoTable += "<td>";	
			infoTable += "<table class='table table-hover innerTable'><tbody>";
			/*Loop for ss info object array*/
			for(var i=0;i<contentObject.ss_info.length;i++) {

				if(contentObject.ss_info[i].show == 1) {
					infoTable += "<tr><td>"+contentObject.ss_info[i].title+"</td><td>"+contentObject.ss_info[i].value+"</td></tr>";
				}
			}

			infoTable += "<tr><td>Lat, Long</td><td>"+contentObject.bs_lat+", "+contentObject.bs_lon+"</td></tr>";
			infoTable += "</tbody></table>";			
			infoTable += "</td>";
			/*BS-Sector Info End*/
			/*BS-Sector Performance Start*/
			infoTable += "<td style='vertical-align:middle;text-align: center;'><h1><i class='fa fa-signal'></i>  "+contentObject.bs_perf+"</h1></td>";
			/*BS-Sector Performance End*/
			/*SS Info Start*/
			infoTable += "<td>";			
			infoTable += "<table class='table table-hover innerTable'><tbody>";
			/*Loop for BS or Sector info object array*/
			for(var i=0;i<contentObject.bs_info.length;i++) {

				if(contentObject.bs_info[i].show == 1) {
					infoTable += "<tr><td>"+contentObject.bs_info[i].title+"</td><td>"+contentObject.bs_info[i].value+"</td></tr>";
				}
			}

			infoTable += "<tr><td>Lat, Long</td><td>"+contentObject.ss_lat+", "+contentObject.ss_lon+"</td></tr>";
			infoTable += "</tbody></table>";		
			infoTable += "</td>";
			/*SS Info End*/
			/*SS Performance Start*/
			infoTable += "<td style='vertical-align:middle;text-align: center;'><h1><i class='fa fa-signal'></i>  "+contentObject.ss_perf+"</h1></td>";
			/*SS Performance End*/
			infoTable += "</tr>";
			infoTable += "</tbody></table>";
			
			/*Concat infowindow content*/
			windowContent += "<div class='windowContainer'><div class='box border'><div class='box-title'><h4><i class='fa fa-map-marker'></i> BS-SS</h4></div><div class='box-body'>"+infoTable+"<div class='clearfix'></div><ul class='list-unstyled list-inline'><li><button class='btn btn-sm btn-info' onClick='that.claculateFresnelZone("+contentObject.bs_lat+","+contentObject.bs_lon+","+contentObject.ss_lat+","+contentObject.ss_lon+","+contentObject.bs_height+","+contentObject.ss_height+");'>Fresnel Zone</button></li></ul></div></div></div>";

		} else {

			infoTable += "<table class='table table-bordered'><tbody>";

			for(var i=0;i<contentObject.dataset.length;i++) {

				if(contentObject.dataset[i].show == 1) {
					infoTable += "<tr><td>"+contentObject.dataset[i].title+"</td><td>"+contentObject.dataset[i].value+"</td></tr>";
				}
			}
			
			if(contentObject.position != undefined) {
				infoTable += "<tr><td>Lat, Long</td><td>"+contentObject.position.k+", "+contentObject.position.A+"</td></tr>";
			} else if(contentObject.center != undefined) {
				infoTable += "<tr><td>Lat, Long</td><td>"+contentObject.center.k+", "+contentObject.center.A+"</td></tr>";
			}

			infoTable += "</tbody></table>";

			if(contentObject.perf != undefined) {
				perfContent += "<h1><i class='fa fa-signal'></i>  "+contentObject.perf+"</h1>";
			}			
			/*Final infowindow content string*/
			windowContent += "<div class='windowContainer'><div class='box border'><div class='box-title'><h4><i class='fa fa-map-marker'></i>  "+contentObject.pointType.toUpperCase()+"</h4></div><div class='box-body'><div class='windowInfo' align='center'>"+infoTable+"</div><div class='perf'>"+perfContent+"</div><div class='clearfix'></div></div></div></div>";
		}
		/*Return the info window content*/
		return windowContent;
	};

	/**
	 * This function calculates the fresnel zone
	 * @class networkMap
	 * @method claculateFresnelZone
	 * @param lat1 "Int", It contains lattitude of first point
	 * @param lon1 "Int", It contains longitude of first point
	 * @param lat2 "Int", It contains lattitude of second point
	 * @param lon2 "Int", It contains longitude of second point
	 * @param height1 "Int", It contains antina height of first point
	 * @param height2 "Int", It contains antina height of second point
	 */
	this.claculateFresnelZone = function(lat1,lon1,lat2,lon2,height1,height2) {

		/** Converts numeric degrees to radians */
		Number.prototype.toRad = function() {
		   return this * Math.PI / 180;
		}
		/** Converts numeric radians to degrees */
		Number.prototype.toDeg = function() {
		   return this * 180 / Math.PI;
		}

		/*Set the antina height to the available heights*/
		if(height1 == 0 || height1 == undefined) {
			antenaHight1 = antenaHight1;			
		} else {
			antenaHight1 = height1;
		}

		if(height2 == 0 || height2 == undefined) {
			antenaHight2 = antenaHight2;			
		} else {
			antenaHight2 = height2;
		}

		/*Reset global variables*/
		latLongArray = [];
		arrayCounter = 0;

		/*Google maps elevation object*/
		var elevator = new google.maps.ElevationService();

	    /*Two points distance calculation*/
	    /*earth's mean radius in km*/
	    var earthRadius = 6371;
	    var radian_lat1 = lat1.toRad();
	    var radian_lat2 = lat2.toRad();
	    var decimal_Lat = (lat2 - lat1).toRad();
	    var decimal_Lon = (lon2 - lon1).toRad();
	    /*Distance params calculation*/
	    var distance_param1 = Math.sin(decimal_Lat / 2) * Math.sin(decimal_Lat / 2) + Math.cos(radian_lat1) * Math.cos(radian_lat2) * Math.sin(decimal_Lon / 2) * Math.sin(decimal_Lon / 2);
	    var distance_param2 = 2 * Math.atan2(Math.sqrt(distance_param1), Math.sqrt(1 - distance_param1));
	    /*Distance between two points*/
	    var distance_between_sites = earthRadius * distance_param2;
	    
	    /*Stores one end or BS lat lon info to latLongArray*/
	    latLongArray[arrayCounter] = new Array();
	    latLongArray[arrayCounter][0] = lat1;
	    latLongArray[arrayCounter++][1] = lon1;
	    /*Call the getFresnelPath function to generate the data for */
	    that.getFresnelPath(lat1.toRad(), lon1.toRad(), lat2.toRad(), lon2.toRad(), depthStep);

	    /* ----  It stores the destination BTS cordinaties ------*/
	    latLongArray[arrayCounter] = new Array();
	    latLongArray[arrayCounter][0] = lat2;
	    latLongArray[arrayCounter++][1] = lon2;

	    var locations = [];
	    for (var abc = 0; abc < arrayCounter; abc++) {
	        locations.push(new google.maps.LatLng(latLongArray[abc][0], latLongArray[abc][1]));
	    }
	    var positionalRequest = { 'locations': locations };
	    var elevationArray = [];

	    elevator.getElevationForLocations(positionalRequest, function (results, status) {
	        if (status == google.maps.ElevationStatus.OK) {
	            for (var x = 0; x < results.length; x++) {
	                elevationArray.push(results[x].elevation);
	            }
	            that.getFresnelChartData(elevationArray, distance_between_sites);
	        }
	    });
	};

	/**
	 * This function generate fresnel point data.
	 * @class networkMap
	 * @method getFresnelPath
	 * @param lat1 "Int", It contains lattitude of first point
	 * @param lon1 "Int", It contains longitude of first point
	 * @param lat2 "Int", It contains lattitude of second point
	 * @param lon2 "Int", It contains longitude of second point
	 * @param depth "Int", It contains accuracy or depth value for which lat-lons path has to be calculated
	 */
	this.getFresnelPath = function(lat1, lon1, lat2, lon2, depth) {

	    var mlat = that.getMidPT_Lat(lat1, lon1, lat2, lon2);
	    var mlon = that.getMidPT_Lon(lat1, lon1, lat2, lon2);
	    
	    if (depth > 0) {
	        that.getFresnelPath(lat1, lon1, mlat, mlon, depth - 1);
	        latLongArray[arrayCounter] = new Array();
	        latLongArray[arrayCounter][0] = mlat.toDeg();
	        latLongArray[arrayCounter++][1] = mlon.toDeg();

	        that.getFresnelPath(mlat, mlon, lat2, lon2, depth - 1);
	    }
	    else {
	        latLongArray[arrayCounter] = new Array();
	        latLongArray[arrayCounter][0] = mlat.toDeg();
	        latLongArray[arrayCounter++][1] = mlon.toDeg();
	    }
	};

	/**
	 * This function calculates mid lattitude point for given lat-lons
	 * @class networkMap
	 * @method getMidPT_Lat
	 * @param lat1 "Int", It contains lattitude of first point
	 * @param lon1 "Int", It contains longitude of first point
	 * @param lat2 "Int", It contains lattitude of second point
	 * @param lon2 "Int", It contains longitude of second point
	 * @return lat3 "Int", It contains mid pt lat value
	 */
	this.getMidPT_Lat = function(lat1, lon1, lat2, lon2) {
	    var decimal_Lon = (lon2.toDeg() - lon1.toDeg()).toRad();
	    var Bx = Math.cos(lat2) * Math.cos(decimal_Lon);
	    var By = Math.cos(lat2) * Math.sin(decimal_Lon);
	    var lat3 = Math.atan2(Math.sin(lat1) + Math.sin(lat2), Math.sqrt((Math.cos(lat1) + Bx) * (Math.cos(lat1) + Bx) + By * By));

	    return lat3;
	};

	/**
	 * This function calculates mid longitude point for given lat-lons
	 * @class networkMap
	 * @method getMidPT_Lon
	 * @param lat1 "Int", It contains lattitude of first point
	 * @param lon1 "Int", It contains longitude of first point
	 * @param lat2 "Int", It contains lattitude of second point
	 * @param lon2 "Int", It contains longitude of second point
	 * @return lon3 "Int", It contains mid pt lon value
	 */
	this.getMidPT_Lon = function(lat1, lon1, lat2, lon2) {
	    var decimal_Lon = (lon2.toDeg() - lon1.toDeg()).toRad();
	    var Bx = Math.cos(lat2) * Math.cos(decimal_Lon);
	    var By = Math.cos(lat2) * Math.sin(decimal_Lon);

	    var lon3 = lon1 + Math.atan2(By, Math.cos(lat1) + Bx);

	    return lon3;
	};

	/**
	 * This function generates the data for fresnel zone
	 * @class networkMap
	 * @method getFresnelChartData
	 * @param elevationArray [Int Array], It contains elevation values array
	 * @param pt_distance "Int", It contains distance between two points
	 */
	this.getFresnelChartData = function(elevationArray, pt_distance) {

	    var segSize = pt_distance / (arrayCounter - 1);

	    for (var i = 0; i < arrayCounter; i++) {
	        latLongArray[i][2] = parseFloat(elevationArray[i]);
	        latLongArray[i][3] = i * segSize;
	    }
		
		minYChart=latLongArray[0][2];
		maxYChart=latLongArray[0][2];

		for(var j=1;j<arrayCounter;j++){
			if(minYChart>latLongArray[j][2]){
				minYChart=latLongArray[j][2];
			}
			if(maxYChart<latLongArray[j][2]){
				maxYChart=latLongArray[j][2];
			}
			
		}
			
		minYChart=Math.round(minYChart);
		minYChart=(minYChart>20)? (minYChart-20):minYChart;
		mod=minYChart%10;
		minYChart=minYChart-mod;

	    latLongArray[0][2] += parseFloat(antenaHight1);
	    latLongArray[arrayCounter - 1][2] += parseFloat(antenaHight2);
		
		var startHeight = parseFloat(latLongArray[0][2]);
	    var endHeight = parseFloat(latLongArray[arrayCounter - 1][2]);
	    var theta = Math.atan((endHeight - startHeight) / pt_distance);
		var slant_d = pt_distance / Math.cos(theta);
		var fr_ghz = fr / 1000;
		var clr_coff = clear_factor / 100;

	    for (var k = 0; k < arrayCounter; k++) {
	        latLongArray[k][4] = startHeight + (((endHeight - startHeight) / pt_distance) * latLongArray[k][3]);

	        var vS0 = parseFloat(latLongArray[k][3]);
			var slant_vS0 = vS0 / Math.cos(theta);
			var vS1 = parseFloat(latLongArray[k][4]);
			var v1 = 17.314 * Math.sqrt((slant_vS0 * (slant_d - slant_vS0)) / (slant_d * fr_ghz));
			var v2 = v1 * Math.cos(theta) * clr_coff;
			
	        latLongArray[k][5] = (vS1) + v2;
	        latLongArray[k][7] = (vS1) - v2;
			
			/*If height changes -------- For future use, if we add sliders for height variation*/
			if(!HEIGHT_CHANGED){
				latLongArray[k][9] = latLongArray[k][2]; // pin points
			}
			else{
				latLongArray[k][9] = latLongArrayCopy[k][9];
				if(k == (arrayCounter-1)){
					HEIGHT_CHANGED = false;
				}
			}
	    }

		for(var l=0;l<arrayCounter;l++){
				
			if(maxYChart<latLongArray[l][5]){
				maxYChart=latLongArray[l][5];
			}
		}

		maxYChart=Math.round(maxYChart);
		maxYChart=maxYChart+30;
		mod=maxYChart%10;
		maxYChart=maxYChart-mod;

		/*Call 'drawFresnelChart' function to plot Fresnel Chart*/
	    that.drawFresnelChart();
	};

	/**
	 * This function creates the fresnal zone chart with elevation points using jquery.flot.js
	 * @class networkMap
	 * @method drawFresnelChart
	 * @user jquery.flot.js
	 * @user bootbox.js
	 */
	this.drawFresnelChart = function() {

		/* init points arrays for the chart */
		var dataPinpoints = [],
			dataAltitude = [],
			dataLOS = [],
			dataFresnel1 = [],
			dataFresnel2 = [];

		/* filling points arrays for the chart */
		for(i = 0; i < arrayCounter; i++) {
			dataAltitude.push([parseFloat(latLongArray[i][3]), parseFloat(latLongArray[i][2])]);
			dataLOS.push([parseFloat(latLongArray[i][3]), parseFloat(latLongArray[i][4])]);
			dataFresnel1.push([parseFloat(latLongArray[i][3]), parseFloat(latLongArray[i][5])]);
			dataFresnel2.push([parseFloat(latLongArray[i][3]), parseFloat(latLongArray[i][7])]);
			dataPinpoints.push([parseFloat(latLongArray[i][3]), parseFloat(latLongArray[i][9])]);
		}

		/*Fresnel template String*/
		var fresnelTemplate = '<div class="fresnelContainer row" style="height:310px;overflow-y:auto;"><div class="col-md-2" align="center"><div class="col-md-8 col-md-offset-2"><input type="text" id="antinaVal1" class="form-control" value="'+antenaHight1+'"></div><div class="clearfix"></div><div id="antina_height1" style="height:290px;" class="slider slider-blue"></div></div><div class="col-md-8"><div id="chart_div" style="width:600px;max-width:100%;height:320px;"></div></div><div class="col-md-2" align="center"><div class="col-md-8 col-md-offset-2"><input type="text" id="antinaVal2" class="form-control" value="'+antenaHight2+'"></div><div class="clearfix"></div><div id="antina_height2" class="slider slider-blue" style="height:290px;"></div></div></div>';

		/*Call the bootbox to show the popup with Fresnel Zone Graph*/
		bootbox.dialog({
			message: fresnelTemplate,
			title: '<i class="fa fa-dot-circle-o">&nbsp;</i> Fresnel Zone'
		});

		$("#antina_height1").slider({
	    	range:"min",
	    	value:antenaHight1,
	    	min:1,
	    	max:100,
	    	animate:true,
	    	orientation:"vertical",
	    	slide:function(a,b){
    			$("#antinaVal1").val(b.value);
	    	}
	    });
	    $("#antina_height2").slider({
	    	range:"min",
	    	value:antenaHight2,
	    	min:1,
	    	max:100,
	    	animate:true,
	    	orientation:"vertical",
	    	slide:function(a,b){
    			$("#antinaVal2").val(b.value);
	    	}
	    });

		$(".modal-dialog").css("width","75%");

		/*Plotting chart with points array using jquery.flot.js*/
		var fresnelChart = $.plot(
			$("#chart_div"),
			[ 
				{ data: dataPinpoints, label: "Pin Points", lines: { show: false}, points: { show: true ,fill: true, radius: 1}, bars: {show:true, lineWidth:1, fill:false, barWidth:0}},
				{ data: dataAltitude, label: "Altitude",lines: { show: true ,fill: 0.8, fillColor: altitudeColor}},
				{ data: dataLOS, label: "LOS", lines: { show: true}},
				{ data: dataFresnel1, label: "Fresnel-1"},
				{ data: dataFresnel2, label: "Fresnel-2"}
			],
			{
				series: {
					lines: { show: true},
					points: { show: false },
					colors: [{ opacity: 0.8 }, { brightness: 0.6, opacity: 0.8 } ]
				},
				grid: { hoverable: true, clickable: true, autoHighlight: true, backgroundColor: { colors: ["#ccc", "#fff"] }},
				yaxis: { min:minYChart, max:  maxYChart },
				xaxis: { min: 0, max:  latLongArray[arrayCounter - 1][3]},
				colors: [pinPointsColor,altitudeColor,losColor,fresnel1Color,fresnel2Color]
			}
		);
	};

	/**
	 * This function filters the markers for the given filters
	 * @class networkMap
	 * @method applyFilter
	 * @param filtersArray [JSON Array] It is an object array of filters with keys
	 */
	this.applyFilter = function(filtersArray) {

		/*Store the reference of current pointer in a global variable*/
		that = this;

		var filterKey = [],
			filteredData = [],
			masterIds = [],
			slaveIds = [];

		/*Fetch the keys from the filter array*/
		$.each(filtersArray, function(key, value) {

		    filterKey.push(key);
		});
		
	 	if(devices.length > 0) {

	 		filteredData = [];
	 		for(var i=0;i<devices.length;i++) {

	 			/*Total Slaves Count*/
	 			var slaveLength = devices[i].children.length;
	 			/*Loop For Slaves*/
	 			for(var j=0;j<slaveLength;j++) {

	 				var master = devices[i];
		 			var slave = devices[i].children[j];
		 				
		 			/*Conditions as per the number of filters*/
		 			if(filterKey.length == 1) {

	 					if(master.data[filterKey[0]] == filtersArray[filterKey[0]] || slave.data[filterKey[0]] == filtersArray[filterKey[0]]) {

		 					/*Check For The Duplicacy*/
		 					if(masterIds.indexOf(master.id) == -1 && slaveIds.indexOf(slave.id) == -1) {

		 						/*Save the master & slave ids to array to remove duplicacy*/
		 						masterIds.push(master.id);
		 						slaveIds.push(slave.id);

		 						filteredData.push(devices[i]);
		 					}
		 				}

		 			} else if(filterKey.length == 2) {

	 					if((master.data[filterKey[0]] == filtersArray[filterKey[0]] || slave.data[filterKey[0]] == filtersArray[filterKey[0]]) && (master.data[filterKey[1]] == filtersArray[filterKey[1]] || slave.data[filterKey[1]] == filtersArray[filterKey[1]])) {

		 					/*Check For The Duplicacy*/
		 					if(masterIds.indexOf(master.id) == -1 && slaveIds.indexOf(slave.id) == -1) {

		 						/*Save the master & slave ids to array to remove duplicacy*/
		 						masterIds.push(master.id);
		 						slaveIds.push(slave.id);

		 						filteredData.push(devices[i]);
		 					}
		 				}
		 			} else if(filterKey.length == 3) {

		 				if((master.data[filterKey[0]] == filtersArray[filterKey[0]] || slave.data[filterKey[0]] == filtersArray[filterKey[0]]) && (master.data[filterKey[1]] == filtersArray[filterKey[1]] || slave.data[filterKey[1]] == filtersArray[filterKey[1]]) && (master.data[filterKey[2]] == filtersArray[filterKey[2]] || slave.data[filterKey[2]] == filtersArray[filterKey[2]])) {

		 					/*Check For The Duplicacy*/
		 					if(masterIds.indexOf(master.id) == -1 && slaveIds.indexOf(slave.id) == -1) {

		 						/*Save the master & slave ids to array to remove duplicacy*/
		 						masterIds.push(master.id);
		 						slaveIds.push(slave.id);

		 						filteredData.push(devices[i]);
		 					}
		 				}
		 			} else if(filterKey.length == 4) {

		 				if((master.data[filterKey[0]] == filtersArray[filterKey[0]] || slave.data[filterKey[0]] == filtersArray[filterKey[0]]) && (master.data[filterKey[1]] == filtersArray[filterKey[1]] || slave.data[filterKey[1]] == filtersArray[filterKey[1]]) && (master.data[filterKey[2]] == filtersArray[filterKey[2]] || slave.data[filterKey[2]] == filtersArray[filterKey[2]]) && (master.data[filterKey[3]] == filtersArray[filterKey[3]] || slave.data[filterKey[3]] == filtersArray[filterKey[3]])) {

		 					/*Check For The Duplicacy*/
		 					if(masterIds.indexOf(master.id) == -1 && slaveIds.indexOf(slave.id) == -1) {

		 						/*Save the master & slave ids to array to remove duplicacy*/
		 						masterIds.push(master.id);
		 						slaveIds.push(slave.id);

		 						filteredData.push(devices[i]);
		 					}
		 				}
		 			}
	 			}
	 		}
	 		/*Check that after applying filters any data exist or not*/
	 		if(filteredData.length === 0) {

	 			bootbox.alert("User Don't Have Any Devies For Selected Filters");

	 		} else {

				/*Reset the markers, polyline & filters*/
	 			that.clearMapElements();

				masterMarkersObj = [];
				slaveMarkersObj = [];

				/*Populate the map with the filtered markers*/
	 			that.populateNetwork(filteredData);
	 		}	 		
	 	}	
	};

	/**
	 * This function calls the populateNetwork function to load the fetched devices in case of no filters
	 * @class devicePlottingLib
	 * @method loadExistingDevices
	 */
	this.loadExistingDevices = function() {

		/*Store the reference of current pointer in a global variable*/
		that = this;

		that.populateNetwork(devices);
	};

	/**
     * This function makes an array from the selected filters
     * @function makeFiltersArray
     * @return selectedArray [JSON Array] It is an object array of the selected filters with the keys
     */
    this.makeFiltersArray = function() {

    	/*Store the reference of current pointer in a global variable*/
		that = this;

        var selectedTechnology = $("#technology").val(),
            selectedvendor = $("#vendor").val(),
            selectedState = $("#state").val(),
            selectedCity = $("#city").val(),
            selectedArray = {};

        if(selectedTechnology != "") {

            selectedArray["technology"] = selectedTechnology;
        }

        if(selectedvendor != "") {

            selectedArray["vendor"] = selectedvendor;
        }

        if(selectedState != "") {

            selectedArray["state"] = selectedState;
        }

        if(selectedCity != "") {

            selectedArray["city"] = selectedCity;
        }
        /*Get The Length Of Filter Array*/
        var filtersLength = Object.keys(selectedArray).length;

        /*If any filter is applied then filter the data*/
        if(filtersLength > 0) {

            that.applyFilter(selectedArray);
        }
        /*If no filter is applied the load all the devices*/
        else {

            that.loadExistingDevices();
        }
    };

	/**
	 * This function creates enable the polygon drawing tool & draw the polygon
	 * @class devicePlottingLib
	 * @method createPolygon
	 */
	this.createPolygon = function() {

		/*Store the reference of current pointer in a global variable*/
    	that = this;
    	
    	selectedCount = polygonSelectedDevices.length;

    	if(selectedCount == 0) {

    		drawingManager = new google.maps.drawing.DrawingManager({
				drawingMode: google.maps.drawing.OverlayType.POLYGON,
				drawingControl: false,
				drawingControlOptions: {
					position: google.maps.ControlPosition.TOP_CENTER,
					drawingModes: [
						google.maps.drawing.OverlayType.POLYGON,
					]
				},
				map : mapInstance
			});
			
			drawingManager.setMap(mapInstance);

			google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {

				pathArray = e.overlay.getPath().getArray();
				polygon = new google.maps.Polygon({"path" : pathArray});
				bs_ss_array = masterMarkersObj.concat(slaveMarkersObj);
				currentPolygon = e.overlay;
				currentPolygon.type = e.type;
				
				for(var k=0;k<bs_ss_array.length;k++) {
					
					var point = bs_ss_array[k].position;

					if (google.maps.geometry.poly.containsLocation(point, polygon)) {
						polygonSelectedDevices.push(bs_ss_array[k]);
					}
				}
				selectedCount = polygonSelectedDevices.length;
				if(selectedCount == 0) {
					
					bootbox.alert("No devices are under the selected area.Please re-select");
					/*Remove current polygon from map*/
					that.clearPolygon();

				} else if(selectedCount > 200) {
					
					bootbox.alert("Max. limit for selecting devices is 200.Please re-select");
					/*Remove current polygon from map*/
					that.clearPolygon();

				} else {
					// var datasetArray = [];
					// $.each(polygonSelectedDevices,function(key,val) {
					// 	datasetArray.push(val.dataset);
					// });
					// $.each(datasetArray,function(key2,dataval) {
					// 	if(dataval.name == "title" || dataval.name == "ip") {
							
					// 	}
					// });
					
					var devicesTemplate = "<div class='deviceWellContainer'>";
					for(var i=0;i<selectedCount;i++) {
						devicesTemplate += '<div class="well well-sm"><h5>'+polygonSelectedDevices[i].title+'('+polygonSelectedDevices[i].pointIp+')</h5><ul class="list-unstyled list-inline">';
						devicesTemplate += '<li><button id="play_'+i+'" onClick="that.startMonitoring('+i+')" class="btn btn-default btn-xs"><i class="fa fa-play"></i></button></li>';
						devicesTemplate += '<li><button id="pause_'+i+'" onClick="that.pauseMonitoring('+i+')" class="btn btn-default btn-xs"><i class="fa fa-pause"></i></button></li>';
						devicesTemplate += '<li><button id="stop_'+i+'" onClick="that.stopMonitoring('+i+')" class="btn btn-default btn-xs"><i class="fa fa-stop"></i></button></li>';
						devicesTemplate += '</ul><div class="sparklineContainer"><span class="sparkline" id="sparkline_'+i+'">Loading...</span></div></div>';
					}
					devicesTemplate += "</div>";
					

					$("#sideInfo > .panel-body").html(devicesTemplate);					

					if($("#sideInfoContainer").hasClass("hide")) {
						$("#sideInfoContainer").removeClass("hide");
					}
					if(!$("#createPolygonBtn").hasClass("hide")) {
						$("#createPolygonBtn").addClass("hide");
					}

					if($("#clearPolygonBtn").hasClass("hide")) {
						$("#clearPolygonBtn").removeClass("hide");
					}

					drawingManager.setDrawingMode(null);
				}

				$("#createPolygonBtn").button("complete");
				$("#advFilterBtn").button("complete");
				$("#resetFilters").button("complete");
			});
    	} else {

    		bootbox.alert("Please clear the current selection.");
    		$("#clearPolygonBtn").removeClass("hide");
    		$("#createPolygonBtn").button("complete");
			$("#advFilterBtn").button("complete");
			$("#resetFilters").button("complete");
    	}
	};

	/**
	 * This function clear the polygon selection from the map
	 * @class devicePlottingLib
	 * @method clearPolygon
	 */
	this.clearPolygon = function() {

		/*Update the html of accordian body*/
		$("#sideInfo > .panel-body").html("No device selected.");
		/*Collapse the selected devices accordian*/
		if(!$("#sideInfoContainer").hasClass("hide")) {
			$("#sideInfoContainer").addClass("hide");
		}		
		/*Show Select Devices button*/
		if($("#createPolygonBtn").hasClass("hide")) {
			$("#createPolygonBtn").removeClass("hide");
		}
		/*Hide the clear selection button*/
		if(!$("#clearPolygonBtn").hasClass("hide")) {
			$("#clearPolygonBtn").addClass("hide");
		}
		/*Remove the current polygon from the map*/
		currentPolygon.setMap(null);
		/*Reset the variables*/
		polygonSelectedDevices = [];		
		pathArray = [];
		polygon = "";
		pointsArray = [];
		// currentPolygon = {};
	};

	/**
	 * This function creates the line chart for the monitoring of selected devices
	 * @class devicePlottingLib
	 * @method makeMonitoringChart
	 * @param id 'Integer'
	 */
	this.makeMonitoringChart = function(id) {

		var startClassNames = $("#play_"+id)[0].className;
		var stopClassNames = $("#stop_"+id)[0].className;

		if(startClassNames.indexOf("active") != -1) {
			
			var num = Math.floor((Math.random() * 20) + 1)
			var oldLength = dataArray.length;
			for(var i=0;i<num;i++) {

				dataArray.push(Math.floor(Math.random() * 80));
			}

			var margin = oldLength * 5;
			
			$("#sparkline_"+id).sparkline(dataArray, {
		        type: "line",
		        lineColor: "blue",
		        spotColor : "orange",
		        defaultPixelsPerValue : 5
		    });

		    setTimeout(function() {
				$("#sparkline_"+id).css("margin-left","-"+leftMargin+"px");
				/*Decrement the margin-left value*/
				leftMargin = margin;
				/*Recursive calling*/
				that.makeMonitoringChart(id);
			},1500);

		} else if(stopClassNames.indexOf("active") != -1) {

				$("#sparkline_"+id).sparkline("", {
			        type: "line",
			        lineColor: "blue",
			        spotColor : "orange",
			        zeroAxis: false
			    });
		}
	};

	this.startMonitoring = function(id) {

		$("#play_"+id).addClass("active");
        if($("#pause_"+id).hasClass("active")) {
            $("#pause_"+id).removeClass("active");
        }
        if($("#stop_"+id).hasClass("active")) {
            $("#stop_"+id).removeClass("active");
        }

        that.makeMonitoringChart(id);
	};

	this.pauseMonitoring = function(id) {
		
		$("#pause_"+id).addClass("active");
        if($("#play_"+id).hasClass("active")) {
            $("#play_"+id).removeClass("active");
        }
        if($("#stop_"+id).hasClass("active")) {
            $("#stop_"+id).removeClass("active");
        }
        that.makeMonitoringChart(id);
	};

	this.stopMonitoring = function(id) {
		
		$("#stop_"+id).addClass("active");
        if($("#play_"+id).hasClass("active")) {
            $("#play_"+id).removeClass("active");
        }
        if($("#pause_"+id).hasClass("active")) {
            $("#pause_"+id).removeClass("active");
        }
        that.makeMonitoringChart(id);
	};
	
    /**
     * This function resets the global variables & again call the api calling function after given timeout
     * @class devicePlottingLib
     * @method recallServer
     */
    this.recallServer = function() {

    	/*Store the reference of current pointer in a global variable*/
    	that = this;

    	/*Hide The loading Icon*/
		$("#loadingIcon").hide();

		/*Enable the refresh button*/
		$("#resetFilters").button("complete");
		

    	setTimeout(function() {
			
			/*Hide The loading Icon*/
			$("#loadingIcon").show();

			/*Enable the refresh button*/
			$("#resetFilters").button("loading");

			/*Reset markers & polyline*/
			that.clearMapElements();

			/*Reset Global Variables & Filters*/
			that.resetVariables();	
			
			/*Recall the API*/
			that.getDevicesData(username);

		},120000);
    };

    /**
	 * This function removes all the elements from the map
	 * @class devicePlottingLib
	 * @method clearMapElements
	 */
	this.clearMapElements = function() {

		/*Store the reference of current pointer in a global variable*/
		that = this;

		/*Clear the marker array of OverlappingMarkerSpiderfier*/
		oms.clearMarkers();

		/*Clear master marker cluster objects*/
		if(masterClusterInstance != "") {
			masterClusterInstance.clearMarkers();
		}
		
		/*Clear slave marker cluster objects*/
		if(slaveClusterInstance != "") {
			slaveClusterInstance.clearMarkers();
		}

		/*Hide The loading Icon*/
		$("#loadingIcon").hide();

		/*Enable the refresh button*/
		$("#resetFilters").button("complete");		

		/*If any master devices exists*/
		if(masterMarkersObj.length > 0) {
			/*Remove All Master Markers*/
			for(var i=0;i<masterMarkersObj.length;i++) {

				masterMarkersObj[i].setMap(null);
			}
		}

		/*If any slave devices exists*/
		if(slaveMarkersObj.length > 0) {
			/*Remove All Slave Markers*/
			for(var j=0;j<slaveMarkersObj.length;j++) {

				slaveMarkersObj[j].setMap(null);
			}
		}

		/*If any link between devices exists*/
		if(pathLineArray.length > 0) {
			/*Remove all link line between devices*/
			for(var j=0;j<pathLineArray.length;j++) {

				pathLineArray[j].setMap(null);
			}
		}

		/*If any sector exists*/
		if(sectorArray.length > 0) {
			/*Clear the sectors from map*/
			for(var j=0;j<sectorArray.length;j++) {

				sectorArray[j].setMap(null);
			}
		}

		/*If any circle exists*/
		if(circleArray.length > 0) {
			/*Clear the sectors from map*/
			for(var j=0;j<circleArray.length;j++) {

				circleArray[j].setMap(null);
			}
		}
	};

	/**
	 * This function reset all global variable used in the process
	 * @class devicePlottingLib
	 * @method resetVariables
	 */
	this.resetVariables = function() {

		/*Reset All The Variables*/
		hitCounter = 1;
		showLimit = 0;
		remainingDevices = 0;
		counter = -999;
		totalCalls = 1;
		devicesObject = {};
		devices = [];
		masterMarkersObj = [];
		slaveMarkersObj = [];
		clusterIcon = "";
		sectorArray = [];
		circleArray = [];
	};
}