Number.prototype.toRad = function() {
    return this * Math.PI / 180;
}

Number.prototype.toDeg = function() {
    return this * 180 / Math.PI;
}

/*This function gets the Points Lat lng at specific angle and radius */
function getAtXYDirection(brng, dist, lon, lat) {
    dist = dist/10;
    dist = dist / 6371;
    brng = brng.toRad();

    var lat1 = Number(lat).toRad(),
        lon1 = Number(lon).toRad();

    var lat2 = Math.asin(Math.sin(lat1) * Math.cos(dist) + Math.cos(lat1) * Math.sin(dist) * Math.cos(brng));
    var lon2 = lon1 + Math.atan2(Math.sin(brng) * Math.sin(dist) * Math.cos(lat1), Math.cos(dist) - Math.sin(lat1) * Math.sin(lat2));

    if (isNaN(lat2) || isNaN(lon2)) return null;

    return {lat: Number(lat2).toDeg(), lon: Number(lon2).toDeg()};
}

/*This function converts dms lat lon to decimal degree lat lon*/
function dmsToDegree(latLng) {

    var new_pt = NaN,degrees,minutes,seconds,hemisphere;

    degrees = Number(latLng[1]);
    minutes = typeof (latLng[2]) !== "undefined" ? Number(latLng[2]) / 60 : 0;
    seconds = typeof (latLng[3]) !== "undefined" ? Number(latLng[3]) / 3600 : 0;
    hemisphere = latLng[4] || null;
    if (hemisphere !== null && /[SW]/i.test(hemisphere)) {
        degrees = Math.abs(degrees) * -1;
    }
    if(degrees < 0) {
        new_pt = degrees - minutes - seconds;
    } else {
        new_pt = degrees + minutes + seconds;
    }

    return new_pt;
}

/*
Function to show Error Message
 */
function showErrorMessage(errormsg, response) {
    // console.log(errormsg, response);
}

/*
OpenLayer KML extension to show KML on Openlayer
 */
OpenLayers.Format.KML = OpenLayers.Class(OpenLayers.Format.KML, {
    CLASS_NAME: "OpenLayers.Format.KML",
    parseStyle: function(node) {
        var baseURI = node.baseURI.split("?")[0]; // remove query, if any
        if (baseURI.lastIndexOf("/") != baseURI.length - 1) {
            baseURI = baseURI.substr(0, baseURI.lastIndexOf("/") + 1);
        }
        var style = OpenLayers.Format.KML.prototype.parseStyle.call(this, node);
        if (typeof style.externalGraphic != "undefined" && style.externalGraphic.match(new RegExp("(^/)|(://)")) == null) {
            style.externalGraphic = baseURI + style.externalGraphic;
        }
        return style;
    }
});

function displayBounds(feature, lon, lat){
    var bounds = feature.geometry.getBounds();
    var lonlat = new OpenLayers.LonLat(lon, lat);

    if ((lonlat.lon < bounds.left) || (lonlat.lat > bounds.top) || (lonlat.lat < bounds.bottom) ||(lonlat.lon > bounds.right) ) {
        return 'out';
    }
    return 'in';
}

OpenLayers.Strategy.Cluster = OpenLayers.Class(OpenLayers.Strategy, {

    /**
     * APIProperty: distance
     * {Integer} Pixel distance between features that should be considered a
     *     single cluster.  Default is 20 pixels.
     */
    distance: 20,

    /**
     * APIProperty: threshold
     * {Integer} Optional threshold below which original features will be
     *     added to the layer instead of clusters.  For example, a threshold
     *     of 3 would mean that any time there are 2 or fewer features in
     *     a cluster, those features will be added directly to the layer instead
     *     of a cluster representing those features.  Default is null (which is
     *     equivalent to 1 - meaning that clusters may contain just one feature).
     */
    threshold: null,

    /**
     * Property: features
     * {Array(<OpenLayers.Feature.Vector>)} Cached features.
     */
    features: null,

    /**
     * Property: clusters
     * {Array(<OpenLayers.Feature.Vector>)} Calculated clusters.
     */
    clusters: null,

    /**
     * Property: clustering
     * {Boolean} The strategy is currently clustering features.
     */
    clustering: false,

    /**
     * Property: resolution
     * {Float} The resolution (map units per pixel) of the current cluster set.
     */
    resolution: null,

    /**
     * Constructor: OpenLayers.Strategy.Cluster
     * Create a new clustering strategy.
     *
     * Parameters:
     * options - {Object} Optional object whose properties will be set on the
     *     instance.
     */

    /**
     * APIMethod: activate
     * Activate the strategy.  Register any listeners, do appropriate setup.
     * 
     * Returns:
     * {Boolean} The strategy was successfully activated.
     */
    activate: function() {
        var activated = OpenLayers.Strategy.prototype.activate.call(this);
        if(activated) {
            this.layer.events.on({
                "beforefeaturesadded": this.cacheFeatures,
                "moveend": this.cluster,
                scope: this
            });
        }
        return activated;
    },

    /**
     * APIMethod: deactivate
     * Deactivate the strategy.  Unregister any listeners, do appropriate
     *     tear-down.
     * 
     * Returns:
     * {Boolean} The strategy was successfully deactivated.
     */
    deactivate: function() {
        var deactivated = OpenLayers.Strategy.prototype.deactivate.call(this);
        if(deactivated) {
            this.clearCache();
            this.layer.events.un({
                "beforefeaturesadded": this.cacheFeatures,
                "moveend": this.cluster,
                scope: this
            });
        }
        return deactivated;
    },

    /**
     * Method: cacheFeatures
     * Cache features before they are added to the layer.
     *
     * Parameters:
     * event - {Object} The event that this was listening for.  This will come
     *     with a batch of features to be clustered.
     *     
     * Returns:
     * {Boolean} False to stop features from being added to the layer.
     */
    cacheFeatures: function(event) {
        var propagate = true;
        if(!this.clustering) {
            this.clearCache();
            this.features = event.features;
            this.cluster();
            propagate = false;
        }
        return propagate;
    },

    /**
     * Method: clearCache
     * Clear out the cached features.
     */
    clearCache: function() {
        this.features = null;
    },

    /**
     * Method: cluster
     * Cluster features based on some threshold distance.
     *
     * Parameters:
     * event - {Object} The event received when cluster is called as a
     *     result of a moveend event.
     */
    cluster: function(event) {
        if((!event || event.zoomChanged || (event && event.recluster)) && this.features) {
            var resolution = this.layer.map.getResolution();
            if(resolution != this.resolution || !this.clustersExist() || (event && event.recluster)) {
                this.resolution = resolution;
                var clusters = [];
                var feature, clustered, cluster;
                for(var i=0; i<this.features.length; ++i) {
                    feature = this.features[i];
                    if(feature && feature.geometry) {
                        clustered = false;
                        for(var j=clusters.length-1; j>=0; --j) {
                            cluster = clusters[j];
                            if(this.shouldCluster(cluster, feature)) {
                                this.addToCluster(cluster, feature);
                                clustered = true;
                                break;
                            }
                        }
                        if(!clustered) {
                            clusters.push(this.createCluster(this.features[i]));
                        }
                    }
                }
                this.layer.removeAllFeatures();
                if(clusters.length > 0) {
                    if(this.threshold > 1) {
                        var clone = clusters.slice();
                        clusters = [];
                        var candidate;
                        for(var i=0, len=clone.length; i<len; ++i) {
                            candidate = clone[i];
                            if(candidate.attributes.count < this.threshold) {
                                Array.prototype.push.apply(clusters, candidate.cluster);
                            } else {
                                clusters.push(candidate);
                            }
                        }
                    }
                    this.clustering = true;
                    // A legitimate feature addition could occur during this
                    // addFeatures call.  For clustering to behave well, features
                    // should be removed from a layer before requesting a new batch.
                    this.layer.addFeatures(clusters);
                    this.clustering = false;
                }
                this.clusters = clusters;
            }
        }
    },

    /**
     * Method: recluster
     * User-callable function to recluster features
     * Useful for instances where a clustering attribute (distance, threshold, ...)
     *     has changed
     */
    recluster: function(){
        var event={"recluster":true};
        this.cluster(event);
    },

    /**
     * Method: clustersExist
     * Determine whether calculated clusters are already on the layer.
     *
     * Returns:
     * {Boolean} The calculated clusters are already on the layer.
     */
    clustersExist: function() {
        var exist = false;
        if(this.clusters && this.clusters.length > 0 &&
           this.clusters.length == this.layer.features.length) {
            exist = true;
            for(var i=0; i<this.clusters.length; ++i) {
                if(this.clusters[i] != this.layer.features[i]) {
                    exist = false;
                    break;
                }
            }
        }
        return exist;
    },

    /**
     * Method: shouldCluster
     * Determine whether to include a feature in a given cluster.
     *
     * Parameters:
     * cluster - {<OpenLayers.Feature.Vector>} A cluster.
     * feature - {<OpenLayers.Feature.Vector>} A feature.
     *
     * Returns:
     * {Boolean} The feature should be included in the cluster.
     */
    shouldCluster: function(cluster, feature) {
        var cc = cluster.geometry.getBounds().getCenterLonLat();
        var fc = feature.geometry.getBounds().getCenterLonLat();
        var distance = (
            Math.sqrt(
                Math.pow((cc.lon - fc.lon), 2) + Math.pow((cc.lat - fc.lat), 2)
            ) / this.resolution
        );
        return (distance <= this.distance);
    },

    /**
     * Method: addToCluster
     * Add a feature to a cluster.
     *
     * Parameters:
     * cluster - {<OpenLayers.Feature.Vector>} A cluster.
     * feature - {<OpenLayers.Feature.Vector>} A feature.
     */
    addToCluster: function(cluster, feature) {
        cluster.cluster.push(feature);
        cluster.attributes.count += 1;
    },

    /**
     * Method: createCluster
     * Given a feature, create a cluster.
     *
     * Parameters:
     * feature - {<OpenLayers.Feature.Vector>}
     *
     * Returns:
     * {<OpenLayers.Feature.Vector>} A cluster.
     */
    createCluster: function(feature) {
        var center = feature.geometry.getBounds().getCenterLonLat();
        var cluster = new OpenLayers.Feature.Vector(
            new OpenLayers.Geometry.Point(center.lon, center.lat),
            {count: 1}
        );
        cluster.cluster = [feature];
        return cluster;
    },

    CLASS_NAME: "OpenLayers.Strategy.Cluster" 
});

/**
* This function creates data to plot sectors on google maps.
* @method createSectorData.
* @param Lat {Number}, It contains lattitude of any point.
* @param Lng {Number}, It contains longitude of any point.
* @param radius {Number}, It contains radius for sector.
 @param azimuth {Number}, It contains azimuth angle for sector.
* @param beamwidth {Number}, It contains width for the sector.
* @param sectorData {Object}, It contains sector info json object.
* @param orientation {String}, It contains the orientation type of antena i.e. vertical or horizontal
* @return {Object Array} sectorDataArray, It is the polygon points lat-lon object array
*/
function createSectorData(lat, lng, radius, azimuth, beamWidth, orientation, callback) {
    var triangle = [], sectorDataArray = [];
    // Degrees to radians
    var d2r = Math.PI / 180;
    //  Radians to degrees
    var r2d = 180 / Math.PI;

    var PRlat = (radius / 6371) * r2d; // using 3959 miles or 6371 KM as earth's radius
    var PRlng = PRlat / Math.cos(lat * d2r);

    var PGpoints = [],
         pointObj = {};

    with(Math) {
        lat1 = (+lat) + (PRlat * cos(d2r * (azimuth - beamWidth / 2)));
        lon1 = (+lng) + (PRlng * sin(d2r * (azimuth - beamWidth / 2)));

        /*Create lat-lon point object*/
        /*Reset Pt Object*/
        pointObj = {};
        pointObj["lat"] = lat1;
        pointObj["lon"] = lon1;
        /*Add point object to array*/
        PGpoints.push(pointObj);

        lat2 = (+lat) + (PRlat * cos(d2r * (azimuth + beamWidth / 2)));
        lon2 = (+lng) + (PRlng * sin(d2r * (azimuth + beamWidth / 2)));

        var theta = 0;
        var gamma = d2r * (azimuth + beamWidth / 2);

        for (var a = 1; theta < gamma; a++) {
            theta = d2r * (azimuth - beamWidth / 2 + a);
            PGlon = (+lng) + (PRlng * sin(theta));
            PGlat = (+lat) + (PRlat * cos(theta));
            /*Reset Pt Object*/
            pointObj = {};
            pointObj["lat"] = PGlat;
            pointObj["lon"] = PGlon;
            /*Add point object to array*/
            PGpoints.push(pointObj);
        }
        /*Reset Pt Object*/
        pointObj = {};
        pointObj["lat"] = lat2;
        pointObj["lon"] = lon2;
        /*Add point object to array*/
        PGpoints.push(pointObj);

        var centerPtObj = {};
        centerPtObj["lat"] = lat;
        centerPtObj["lon"] = lng;
        /*Add center point object to array*/
        PGpoints.push(centerPtObj);
    }

    /*Condition for the orientation of sector antina*/
    if (orientation == "horizontal") {
        var len = Math.floor(PGpoints.length / 3);
        triangle.push(PGpoints[0]);
        triangle.push(PGpoints[(len * 2) - 1]);
        triangle.push(PGpoints[PGpoints.length - 1]);
        /*Assign the triangle object array to sectorDataArray for plotting the polygon*/
        sectorDataArray = triangle;
    } else {
        /*Assign the PGpoints object array to sectorDataArray for plotting the polygon*/
        sectorDataArray = PGpoints;
    }
    /*Callback with lat-lon object array.*/
    callback(sectorDataArray);
};

/**
 * @method  showWmapFilteredData
 * @param  {[type]} dataArray [description]
 * @return {[type]}           [description]
 */
function showWmapFilteredData(dataArray) {

    var filtered_bs_ss_data = [],
        filtered_sector_data = [],
        filtered_devices_data = [],
        filtered_line_data = [];

    var bsDeviceObj_Filtered = {};

    filtered_devices_array= [];

    for(var i=0;i<dataArray.length;i++) {        
        var sectorsArray = dataArray[i].data.param.sector;
        var bsName = dataArray[i].name ? $.trim(dataArray[i].name) : "";
        var bs_marker = bs_marker = wm_obj['features'][bsName];

        if(bs_marker) {
            filtered_bs_ss_data.push(bs_marker);
        }
        for(var j=0;j<sectorsArray.length;j++) {
            /*Check that the current sector name is present in filtered data or not*/
            var subStationsArray = sectorsArray[j].sub_station,
                sectorName = sectorsArray[j].sector_configured_on ? $.trim(sectorsArray[j].sector_configured_on) : "",
                radius = sectorsArray[j].radius,
                azimuth = sectorsArray[j].azimuth_angle,
                beamWidth = sectorsArray[j].beam_width,
                bsName = dataArray[i].name ? $.trim(dataArray[i].name) : "",
                bs_marker = wm_obj['features'][bsName],
                sector_device = wm_obj['devices']["sector_"+sectorName],
                sector_polygon = wm_obj['sectors']["poly_"+sectorName+"_"+radius+"_"+azimuth+"_"+beamWidth];

            for(var k=0;k<subStationsArray.length;k++) {
                /*BS, SS & Sectors from filtered data array*/
                var ssName = subStationsArray[k].name ? $.trim(subStationsArray[k].name) : "",
                    ss_marker = wm_obj['features'][ssName],
                    line_marker = wm_obj['lines']["line_"+ssName];

                if(ss_marker) {
                    filtered_bs_ss_data.push(ss_marker);
                }
                if(line_marker) {
                    filtered_line_data.push(line_marker);
                }
            }

            if(!bsDeviceObj_Filtered[bsName]) {
                bsDeviceObj_Filtered[bsName] = [];
            }

            if(sector_device) {
                filtered_devices_data.push(sector_device);
                bsDeviceObj_Filtered[bsName].push(sector_device);
                filtered_devices_array.push(sector_device);
            }

            if(sector_polygon) {
                filtered_sector_data.push(sector_polygon);
            }
        }
    }
    whiteMapClass.applyAdvanceFilter({data_for_filters: dataArray, filtered_Devices: bsDeviceObj_Filtered, filtered_Features: filtered_bs_ss_data, line_Features: filtered_line_data, sector_Features: filtered_sector_data});
}



/*
This function returns Size of the Markers to show accroding to the value selected in tools option
 */
var previousIconValue = "small";
var newGraphicHeight = 0, newGraphicWidth = 0, newGraphicXOffset = 0, newGraphicYOffset = 0, bs_newGraphicHeight = 0, bs_newGraphicWidth = 0, bs_newGraphicXOffset = 0, bs_newGraphicYOffset = 0;
function getIconSize() {
    var iconSize = $("#icon_Size_Select_In_Tools").val();
    if(previousIconValue !== iconSize) {
        var largeur= 32, hauteur= 37,largeur_bs = 32, hauteur_bs= 37, divideBy;
        var anchorX, i;
        if(iconSize=== 'small') {
            divideBy= 1.4;
            anchorX= 0.4;
        } else if(iconSize=== 'medium') {
            divideBy= 1;
            anchorX= 0;
        } else {
            divideBy= 0.8;
            anchorX= -0.2;
        }

        
        newGraphicWidth = Math.ceil(largeur/divideBy);
        newGraphicHeight = Math.ceil(hauteur/divideBy);
        newGraphicXOffset = Math.ceil(16-(16*anchorX));
        newGraphicYOffset = Math.ceil(hauteur/divideBy);

        bs_newGraphicHeight= Math.ceil(hauteur_bs/divideBy)+5;
        bs_newGraphicWidth = Math.ceil(largeur_bs/divideBy)-5;
        bs_newGraphicXOffset = Math.ceil(16-(16*anchorX));
        bs_newGraphicYOffset = Math.ceil(hauteur_bs/divideBy);        
        previousIconValue = iconSize;
    }

    return {
        'ss_devices_size': {
            'graphicWidth': newGraphicWidth,
            'graphicHeight': newGraphicHeight,
            'graphicXOffset': newGraphicXOffset,
            'graphicYOffset': newGraphicYOffset
        },
        'bs_devices_size': {
            'graphicWidth': bs_newGraphicWidth,
            'graphicHeight': bs_newGraphicHeight,
            'graphicXOffset': bs_newGraphicXOffset,
            'graphicYOffset': bs_newGraphicYOffset  
        }
    }
}

/**
 * This function shows a Feature
 * @param  {OpenLayer Feature} feature Feature which is to be shown
 * @return {[type]}         [description]
 */
function showOpenLayerFeature(feature) {
    if(feature && feature.style) {
        var featureLayer = feature.layer ? feature.layer : feature.layerReference;
        feature.style.display = '';
        if(featureLayer) {
            // featureLayer.redraw();
        }
    }
}

/**
 * This function hide a Feature
 * @param  {OpenLayer Feature} feature Feature which is to be shown
 * @return {[type]}         [description]
 */
function hideOpenLayerFeature(feature) {
    if(feature && feature.style) {
        var featureLayer = feature.layer ? feature.layer : feature.layerReference;
        feature.style.display = 'none';
        if(featureLayer) {
            // featureLayer.redraw();
            
        }
    }
}


/**
 * This function removes all items from white map
 * @method removeAllOpenLayerFeature
 */
function removeAllOpenLayerFeature() {

    // Hide perf info label
    for (var x = 0; x < labelsArray.length; x++) {
        ccpl_map.removePopup(labelsArray[x]);
    }

    // Hide tooltip info label
    for (key in tooltipInfoLabel) {
        ccpl_map.removePopup(tooltipInfoLabel[key]);
    }

    // Hide loader label
    for (key in loader_icon_dict) {
        ccpl_map.removePopup(loader_icon_dict[key]);
    }

    // Reset labels array 
    labelsArray = [];
    tooltipInfoLabel = {};
    loader_icon_dict = {};


    /*Clear master marker cluster objects*/
    // Deactivate Marker Clustering Strategy
    ccpl_map.getLayersByName('Markers')[0].strategies[0].deactivate();

    ccpl_map.getLayersByName('Markers')[0].destroyFeatures(ccpl_map.getLayersByName('Markers')[0].features);
    ccpl_map.getLayersByName('Markers')[0].redraw();

    ccpl_map.getLayersByName('Lines')[0].destroyFeatures(ccpl_map.getLayersByName('Lines')[0].features);
    ccpl_map.getLayersByName('Lines')[0].redraw();

    ccpl_map.getLayersByName('RedCross')[0].destroyFeatures(ccpl_map.getLayersByName('RedCross')[0].features);
    ccpl_map.getLayersByName('RedCross')[0].redraw();

    ccpl_map.getLayersByName('Sectors')[0].destroyFeatures(ccpl_map.getLayersByName('Sectors')[0].features);
    ccpl_map.getLayersByName('Sectors')[0].redraw();

    ccpl_map.getLayersByName('Devices')[0].destroyFeatures(ccpl_map.getLayersByName('Devices')[0].features);
    ccpl_map.getLayersByName('Devices')[0].redraw();

    // Reset Variables
    bs_ss_markers= [];
    main_devices_data_wmap = [];
    plottedBsIds = [];
    pollableDevices = [];
    deviceIDArray = [];
    sectorMarkerConfiguredOn = [];
    sectorMarkersMasterObj = {};
    sector_MarkersArray = [];
    currentlyPlottedDevices = [];
    allMarkersObject_wmap= {
        'base_station': {},
        'path': {},
        'sub_station': {},
        'sector_device': {},
        'sector_polygon': {},
        'backhaul': {}
    };
    cross_label_array = {};
}



/**
 * This function checks if given feature lies in bound of polygon if polygon is provided else, in map bounds.
 * @param  {Object} point   Point which is to be check. It contains Lat Lng keys.
 * @param  {OpenLayer Polygon Feature} polygon Optional Param. If passed, check inside of polygon else use mapextend
 * @return {[type]}         [description]
 */
WhiteMapClass.prototype.checkIfPointLiesInside = function(point, polygon) {
    var mapBounds = [];
    //get map extent
    var mapBoundsArray = ccpl_map.getExtent().toArray();

    for(var i=0; i< mapBoundsArray.length; i++) {
        var pointObj= {};
        if(i=== 0) {
            pointObj.lat = mapBoundsArray[1];
            pointObj.lon = mapBoundsArray[0];
        } else if (i=== 1) {
            pointObj.lat = mapBoundsArray[3];
            pointObj.lon = mapBoundsArray[0];
        } else if (i=== 2) {
            pointObj.lat = mapBoundsArray[3];
            pointObj.lon = mapBoundsArray[2];
        } else {
            pointObj.lon = mapBoundsArray[2];
            pointObj.lat = mapBoundsArray[1];
        }
        mapBounds.push(pointObj);
    }
    //check if point lies inside extend
    if(isPointInPoly(mapBounds, point)) {
        //return true if it does
        return true;
    }
    //else return false
    return false;
}

/**
 * This function creates PL-RTA labels on SS & sectors(PTP) when right clicked on them for "White Map"
 * @method createPLRtaLabel
 * @param clicked_feature {Object}, It contains the right clicked openlayers feature(Sector or SS).
 */
function createPLRtaLabel(clicked_feature) {

    var condition1 = (clicked_feature.pl || clicked_feature.pl == 0) && $.trim(clicked_feature.pl) != 'N/A',
        condition2 = (clicked_feature.rta || clicked_feature.rta == 0) && $.trim(clicked_feature.rta) != 'N/A',
        condition3 = clicked_feature.pl_timestamp && $.trim(clicked_feature.pl_timestamp) != 'N/A';

    if(condition1 || condition2 || condition3) {
        var pl = (clicked_feature.pl || clicked_feature.pl == 0) ? clicked_feature.pl : "N/A",
            rta = (clicked_feature.rta || clicked_feature.rta == 0) ? clicked_feature.rta : "N/A",
            pl_timestamp = clicked_feature.pl_timestamp ? clicked_feature.pl_timestamp : "N/A",
            info_html = '';

        // Create hover infowindow html content
        info_html += '<table class="table table-responsive table-bordered table-hover">\
                      <tr><td>Packet Drop</td><td>'+pl+'</td></tr>\
                      <tr><td>Latency</td><td>'+rta+'</td></tr>\
                      <tr><td>Timestamp</td><td>'+pl_timestamp+'</td></tr>\
                      </table>';

        var open_location_lat = clicked_feature.ptLat,
            open_location_lon = clicked_feature.ptLon;

        if(clicked_feature.pointType == 'sector_Marker') {
            open_location_lat = clicked_feature.new_lat ? clicked_feature.new_lat : open_location_lat;
            open_location_lon = clicked_feature.new_lon ? clicked_feature.new_lon : open_location_lon;
        }

        pl_rta_popup = new OpenLayers.Popup('ss_perf_'+clicked_feature.name,
            new OpenLayers.LonLat(open_location_lon,open_location_lat),
            new OpenLayers.Size(135,75),
            info_html,
            false
        );

        ccpl_map.addPopup(pl_rta_popup);

        // Remove height prop from div's
        $('.olPopupContent').css('height','');
        $('.olPopup').css('height','');
    }
}