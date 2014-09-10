/*Global Variables*/
var advJustSearch_self = "",
	gmapJustInstance = "",
	setJustFilterApiUrl = "",
	earthJustInstance = "",
    filtersJustInfoArray = [],
    templateJustData = "",
    formJustElements = "",
    elementsJustArray = [],
    resultantJustObject = {},
    appliedJustAdvFilter = [],
    appliedJustAdvSearch_Active = [],
    searchJustParameters = "",
    lastJustSelectedValues = [];
    searchJustquery_data=[];
    result_Just_plot_devices=[], maxZoomLevel= 15, statusText= "Advance Search Applied";

var advanceSearchMasterObj= {};
advanceSearchMasterObj.previouslySearchedMarkersList= [];
advanceSearchMasterObj.searchedIconUrl= 'http://www.iconsdb.com/icons/preview/color/FF1C33/arrow-211-xl.png';
advanceSearchMasterObj.searchedLinesByCircuitIDs= [];
advanceSearchMasterObj.searchedLinesIconUrl= 'http://www.iconsdb.com/icons/preview/color/FF1C33/arrow-211-xl.png';
advanceSearchMasterObj.maxSearchLevelNumber= 20;
advanceSearchMasterObj.searchNumberLimitMessage= 'Too many Searched Results. Please filter again. No Markers drawn'

var ipStationFound= 0;
var ipStation= [];
/**
 * This class is used to Advance Search.
 * @class advanceSearchLibrary
 * @uses jQuery
 * @uses Select2
 * Coded By :- Rahul Garg
 */
function advanceJustSearchClass() {

	/*Store the reference of current pointer in a global variable*/
	advJustSearch_self = this; // Name of current pointer referencing element in all files should be different otherwise conflicts occurs


    this.getFilterInfofrompagedata = function(domElemet, windowTitle, buttonId){
    	//Get filter Data
        filtersJustInfoArray= getDataForAdvanceSearch();

        if(appliedJustAdvSearch_Active.length != 0) {
			lastJustSelectedValues = appliedJustAdvSearch_Active;
		}

        var templateData = "", elementsArray = [];
        templateData += '<div class="iframe-container"><div class="content-container"><div id="'+domElemet+'" class="advanceSearchContainer">';
        templateData += '<form id="'+domElemet+'_form"><div class="form-group form-horizontal">';

        formElements = "";
        /*Reset the appliedJustAdvFilter*/
        appliedJustAdvFilter = [];
        appliedJustAdvSearch_Active = [];
        for(var i=0;i<filtersJustInfoArray.length;i++) {

            if(filtersJustInfoArray[i] != null) {

                formElements += '<div class="form-group"><label for="'+filtersJustInfoArray[i].key+'" class="col-sm-4 control-label">';
                formElements += filtersJustInfoArray[i].title;
                formElements += '</label><div class="col-sm-8">';

                var currentKey = $.trim(filtersJustInfoArray[i].key);
                var elementType = $.trim(filtersJustInfoArray[i].element_type);
                /*Check Element Type*/
                if(elementType == "multiselect") {

                    var filterValues = filtersJustInfoArray[i].values;
                    if(filterValues.length > 0) {

                                                formElements += '<select multiple class="multiSelectBox col-md-12" id="search_'+filtersJustInfoArray[i].key+'">';

                        /*Condition for mapped tables to pass the ID in the values else pass the value*/
                        if(currentKey == "device_group" || currentKey == "device_type" || currentKey == "device_technology" || currentKey == "device_vendor") {

                            for(var j=0;j<filterValues.length;j++) {

                                if(($.trim(filterValues[j].id) != null && $.trim(filterValues[j].value) != null) && ($.trim(filterValues[j].id) != "" && $.trim(filterValues[j].value) != "")) {

                                    formElements += '<option value="'+filterValues[j].value+'">'+filterValues[j].value+'</option>';
                                }
                            }
                        } else {

                            for(var j=0;j<filterValues.length;j++) {

                                if(($.trim(filterValues[j].id) != null && $.trim(filterValues[j].value) != null) && ($.trim(filterValues[j].id) != "" && $.trim(filterValues[j].value) != "")) {
                                    if(currentKey=== "sector_configured_on") {
                                        var s= filterValues[j].value;
                                        s= s.substring(s.lastIndexOf("(")+1,s.lastIndexOf(")"));
                                        formElements += '<option value="'+filterValues[j].value+'">'+s+'</option>';
                                    } else {
                                        formElements += '<option value="'+filterValues[j].value+'">'+filterValues[j].value+'</option>';    
                                    }

                                    
                                }
                            }
                        }
//Add Sub Station IPs too
                        if(currentKey== "sector_configured_on") {
                            var a= markersMasterObj['SS'];
                            var tempArray= [];
                            for(var key in a) {
                                formElements += '<option value="'+a[key]['dataset'][12]['value']+'">'+a[key]['dataset'][12]['value']+'</option>';
                            }
                        }

                        formElements += '</select>';
                    } else {

                        formElements += '<input type="text" id="search_'+filtersJustInfoArray[i].key+'" name="'+filtersJustInfoArray[i].key+'"  class="form-control"/>';
                    }
                } else if(elementType == "select") {

                    var filterValues = filtersJustInfoArray[i].values;
                    if(filterValues.length > 0) {

                        formElements += '<select class="multiSelectBox col-md-12" id="search_'+filtersJustInfoArray[i].key+'">';

                        for(var j=0;j<filterValues.length;j++) {

                            formElements += '<option value="'+filterValues[j].id+'">'+filterValues[j].value+'</option>';
                        }

                        formElements += '</select>';
                    } else {

                        formElements += '<input type="text" id="search_'+filtersJustInfoArray[i].key+'" name="'+filtersJustInfoArray[i].key+'"  class="form-control"/>';
                    }
                }
                else if(elementType == "radio") {

                    var filterValues = filtersJustInfoArray[i].values;
                    if(filterValues.length > 0) {

                        for(var j=0;j<filterValues.length;j++) {

                            formElements += '<label class="radio-inline"><input type="radio" id="radio_'+filterValues[j].id+'" class="radioField" value="'+filterValues[j].id+'" name="'+filtersJustInfoArray[i].key+'"> '+filterValues[j].value+'</label>';
                        }
                    } else {

                        formElements += '<input type="text" id="search_'+filtersJustInfoArray[i].key+'" name="'+filtersJustInfoArray[i].key+'"  class="form-control"/>';
                    }
                } else if(elementType == "checkbox") {

                    var filterValues = filtersJustInfoArray[i].values;
                    if(filterValues.length > 0) {

                        for(var j=0;j<filterValues.length;j++) {

                            formElements += '<label class="checkbox-inline"><input type="checkbox" class="checkboxField" id="checkbox_'+filterValues[j].id+'" value="'+filterValues[j].id+'" name="'+filterValues[j].id+'"> '+filterValues[j].value+'</label>';
                        }
                    } else {

                        formElements += '<input type="text" id="search_'+filtersJustInfoArray[i].key+'" name="'+filtersJustInfoArray[i].key+'"  class="form-control"/>';
                    }
                } else {

                    formElements += '<input type="text" id="search_'+filtersJustInfoArray[i].key+'" name="'+filtersJustInfoArray[i].key+'"  class="form-control"/>';
                }

                formElements += '</div></div>';
                elementsArray.push(formElements);
                formElements = "";
            }
        }

        templateData += elementsArray.join('');
        templateData += '<div class="clearfix"></div></div><div class="clearfix"></div></form>';
        templateData += '<div class="clearfix"></div></div></div><iframe class="iframeshim" frameborder="0" scrolling="no"></iframe></div><div class="clearfix"></div>';

        $("#advSearchFormContainer").html(templateData);

        if($("#advSearchContainerBlock").hasClass("hide")) {
            $("#advSearchContainerBlock").removeClass("hide");
        }

        /*Initialize the select2*/
        $(".advanceSearchContainer select").select2();
        /*loop to show the last selected values*/
        for(var k=0;k<lastJustSelectedValues.length;k++) {
        	
        	$("#search_"+lastJustSelectedValues[k].field).select2("val", lastJustSelectedValues[k].value);
        }
	    /*Hide the spinner*/
	    hideSpinner();

    };

    this.showNotification= function() {
    	if(!$("span#gis_search_status_txt").length) {
    		$("<br /><span id='gis_search_status_txt'>Advance Search Applied</span><button class='btn btn-sm pull-right' onclick='resetAdvanceSearch();'>Reset</button>").insertAfter("#gis_status_txt");
    	}
    }

    this.hideNotification= function() {
    	if($("span#gis_search_status_txt").length) {
    		$("span#gis_search_status_txt").prev().remove();
            $("span#gis_search_status_txt").next().remove();
    		$("span#gis_search_status_txt").remove();
    	}
    }

    //We will remove all Setted Search Markers here in the Array from the map and then clear the Array.
    this.resetPreviousSearchedMarkers= function() {
    	var previousSearchedMarkers= advanceSearchMasterObj.previouslySearchedMarkersList;
    	for(var i=0; i< previousSearchedMarkers.length; i++) {
    		previousSearchedMarkers[i].setMap(null);
    	}
    	previousSearchedMarkers= [];
    }

    //Here we create a new Marker based on the lat, long and show it on the map. Also push the marker to the previouslySeachedMarkersList array
    this.applyIconToSearchedResult= function(lat, long, iconUrl) {
        //create a new lat long
        var searchedMarkerLatLong= new google.maps.LatLng(lat, long);
//sub station visibility check
        if(iconUrl) {
            var ssMarker= markersMasterObj['SS'][String(lat)+long];
            if(ssMarker && !ssMarker.getVisible()) {
                return;
            }
        } else {
            var bsMarker= markersMasterObj['BS'][String(lat)+long];
            if(bsMarker && !bsMarker.getVisible()) {
                return ;
            }
        }

        //create a new marker
        var showSearchedResultMarker= new google.maps.Marker({position: searchedMarkerLatLong, zIndex: 100})
        //push marker in the previouslySearchedMarkersList array
        advanceSearchMasterObj.previouslySearchedMarkersList.push(showSearchedResultMarker);

//IF NOT FILTER APPLIED IS IN CITY OR STATE, THEN WE WILL NOT CHANGE ANY ICONS
    
        var selectedInputs= advJustSearch_self.getInputArray();
        var isOnlyStateorCityIsApplied= false;
        if(selectedInputs['BS Name'].length || /*selectedInputs['BS Latitude'].length || selectedInputs['BS Longitude'].length || */selectedInputs['Circuit Id'].length || selectedInputs['IP'].length || selectedInputs['Technology'].length) {
            isOnlyStateorCityIsApplied= false;
        }
        if(!isOnlyStateorCityIsApplied) {
                if(iconUrl) {
                    //set icon from global object
                    showSearchedResultMarker.setIcon(iconUrl);  
                } else {
                    //set icon from global object
                    showSearchedResultMarker.setIcon(advanceSearchMasterObj.searchedIconUrl);
                }
                //set animation to bounce
                // showSearchedResultMarker.setAnimation(null);
                if(showSearchedResultMarker.getAnimation() != null) {
                    showSearchedResultMarker.setAnimation(null);
                } else {
                    showSearchedResultMarker.setAnimation(google.maps.Animation.DROP);
                }
                //show the marker on map.
                showSearchedResultMarker.setMap(mapInstance);
        }

        google.maps.event.addListener(showSearchedResultMarker, 'click', function() {
            if(iconUrl) {
                google.maps.event.trigger(markersMasterObj['SS'][String(lat)+long], 'click');
            } else {
                google.maps.event.trigger(markersMasterObj['BS'][String(lat)+long], 'click');
                
            }
            
        });
    	return ;
    }

    this.resetPreviousSearchedLines= function() {
    	advanceSearchMasterObj.searchedLinesByCircuitIDs= [];
    }

    this.findTheLineToUpdate= function(device,searchedText) {
        for(var i=0; i< device['data']['param']['sector'].length; i++) {
            for(var j=0; j< searchedText.length; j++) {
                if((String(searchedText[j]).toLowerCase())== (String(device['data']['param']['sector'][i]['circuit_id']).toLowerCase())) {
                    advJustSearch_self.applyIconToSearchedResult(device['data']['param']['sector'][i]['sub_station'][0]['data']['lat'], device['data']['param']['sector'][i]['sub_station'][0]['data']['lon'], advanceSearchMasterObj.searchedLinesIconUrl);
                    advanceSearchMasterObj.searchedLinesByCircuitIDs.push(new google.maps.LatLng(device['data']['param']['sector'][i]['sub_station'][0]['data']['lat'], device['data']['param']['sector'][i]['sub_station'][0]['data']['lon']));
                }    
            }
        }
    }


    this.getInputArray= function() {
    	var ob= {};
    	$("form#searchInfoModal_form > div.form-group .form-group").each(function(i , formEl) {
    		var key= $(formEl).find('label.control-label').html();

    		var selectedValues= [];

    		$(formEl).find('ul.select2-choices li.select2-search-choice').each(function(i, selectedli) {
    			selectedValues.push($(selectedli).find('div').html());
    		});

    		ob[key]= selectedValues;

    		var selectedSelectId= $(formEl).find('select').select2('val');

    		var forAttr= $(formEl).find('label.control-label').attr('for');
    		appliedJustAdvSearch_Active.push({field: forAttr, value: selectedSelectId});
    	});

    	
    	return ob;
    }

    /**
	 * This method generates get parameter for setfilter API & call setFilter function
	 * @method callSetFilter
	 */
	this.searchAndCenterData = function(main_devices_data_gmaps) {
        ipStationFound= 0;
        ipStation= [];

		var selectedInputs= advJustSearch_self.getInputArray();


		function checkIfValid(deviceJson) {
			for(var key in selectedInputs) {
				if(selectedInputs.hasOwnProperty(key)) {
					if(selectedInputs[key].length) {

						//Check BS NAME
						if(key==='BS Name') {
							if(((String(deviceJson.name)).toLowerCase() !== "") && (String(selectedInputs[key]).toLowerCase()).indexOf((String(deviceJson.name)).toLowerCase()) != -1) {
							} else {
								return false;
							}
						}

						// // Check BS Technology
						// if(key==='Technology') {
						// 	var deviceTechnology= deviceJson.sector_ss_technology;
						// 	var deviceTechnologyArray= deviceTechnology.split(" ");
						// 	var isTechnologyPresent= false;
						// 	for(var z=0; z< deviceTechnologyArray.length; z++) {
						// 		if(((String(deviceTechnologyArray[z])).toLowerCase() !== "") && (String(selectedInputs[key]).toLowerCase()).indexOf((String(deviceTechnologyArray[z])).toLowerCase()) != -1) {
						// 			isTechnologyPresent= true;
						// 		}	
						// 	}

						// 	if(!isTechnologyPresent) {
						// 		return false;
						// 	}
						// }

						// Check BS Vendor
						// if(key==='Vendor') {
						// 	var deviceVendor= deviceJson.sector_ss_vendor;
						// 	var deviceVendorArray= deviceVendor.split(" ");
						// 	var isVendorPresent= false;
						// 	for(var z=0; z< deviceVendorArray.length; z++) {
						// 		if(((String(deviceVendorArray[z])).toLowerCase() !== "") && (String(selectedInputs[key]).toLowerCase()).indexOf((String(deviceVendorArray[z])).toLowerCase()) != -1) {
						// 			isVendorPresent= true;
						// 		}	
						// 	}

						// 	if(!isVendorPresent) {
						// 		return false;
						// 	}
						// }

						// Check BS State
						// if(key === 'BS State') {
						// 	if(((String(deviceJson.data.state)).toLowerCase() !== "") && (String(selectedInputs[key]).toLowerCase()).indexOf((String(deviceJson.data.state)).toLowerCase()) != -1) {
						// 	} else {
						// 		return false;
						// 	}							
						// }

						// Check BS City
						if(key === 'BS City') {
                            console.log(selectedInputs[key]);
							if(((String(deviceJson.data.city)).toLowerCase() !== "") && (String(selectedInputs[key]).toLowerCase()).indexOf((String(deviceJson.data.city)).toLowerCase()) != -1) {
							} else {
								return false;
							}	
						}

						// // Check BS Latitude
						// if(key === 'BS Latitude') {
						// 	if(((String(deviceJson.data.lat)).toLowerCase() !== "") && (String(selectedInputs[key]).toLowerCase()).indexOf((String(deviceJson.data.lat)).toLowerCase()) != -1) {
						// 	} else {
						// 		return false;
						// 	}	
						// }

						// // Check BS Longitude
						// if(key === 'BS Longitude') {
						// 	if(((String(deviceJson.data.lon)).toLowerCase() !== "") && (String(selectedInputs[key]).toLowerCase()).indexOf((String(deviceJson.data.lon)).toLowerCase()) != -1) {
						// 	} else {
						// 		return false;
						// 	}	
						// }

						//Check BS Sector Configured On
						if(key === 'IP') {
							var isSectorIsConfigured= false;
                            var deivceConfiguredOn= deviceJson["sector_configured_on_devices"];
                            var deivceConfiguredOnArray= deivceConfiguredOn.split(" ");

                            for(var z=0; z< deivceConfiguredOnArray.length; z++) {
                                if(deivceConfiguredOnArray[z] && ((String(deivceConfiguredOnArray[z])).toLowerCase() !== "")) {
                                    var s= (String(deivceConfiguredOnArray[z])).toLowerCase();
                                    s= s.substring(s.lastIndexOf("(")+1,s.lastIndexOf(")"));
                                    if((String(selectedInputs[key]).toLowerCase()).indexOf(s) != -1) {
                                        isSectorIsConfigured= true;
                                    }
                                }
                            }

//Check for SUbStations
                            for(var i=0; i< deviceJson['data']['param']['sector'].length; i++) {
                                for(var j=0; j< deviceJson['data']['param']['sector'][i]['sub_station'].length; j++) {
                                    var ip= deviceJson['data']['param']['sector'][i]['sub_station'][j]['data']['param']['sub_station'][12]['value'];
                                    if((String(selectedInputs[key]).toLowerCase()).indexOf(ip) != -1) {
                                        ipStationFound= 1;
                                        ipStation.push(deviceJson['data']['param']['sector'][i]['sub_station'][j]['data']['lat'], deviceJson['data']['param']['sector'][i]['sub_station'][j]['data']['lon']);
                                        advJustSearch_self.applyIconToSearchedResult(deviceJson['data']['param']['sector'][i]['sub_station'][j]['data']['lat'], deviceJson['data']['param']['sector'][i]['sub_station'][j]['data']['lon']);
                                        isSectorIsConfigured= true;
                                    }
                                }
                            }

                            if(!isSectorIsConfigured) {
								return false;
							}
						}

						if(key === 'Circuit Id') {
							var deviceCircuitIDs= deviceJson.circuit_ids;
                            var deviceCircuitIDSArray= deviceCircuitIDs.split(" ");
                            var isCircuitPresent= false;
							for(var z=0; z< deviceCircuitIDSArray.length; z++) {
								if(deviceCircuitIDSArray[z] && ((String(deviceCircuitIDSArray[z])).toLowerCase() !== "") && (String(selectedInputs[key]).toLowerCase()).indexOf((String(deviceCircuitIDSArray[z])).toLowerCase()) != -1) {
									advJustSearch_self.findTheLineToUpdate(deviceJson, selectedInputs[key]);
									isCircuitPresent= true;
								}	
							}

							if(!isCircuitPresent) {
								return false;
							}
						}
					}
				}
			}
			return true;
		}

		var searchedStations= [];

		//reset previous markers
		advJustSearch_self.resetPreviousSearchedMarkers();

		//Reset Lines
		advJustSearch_self.resetPreviousSearchedLines();
		var bounds= new google.maps.LatLngBounds();
		for(var i=0; i< main_devices_data_gmaps.length; i++) {
			if(checkIfValid(main_devices_data_gmaps[i])) {
				searchedStations.push(main_devices_data_gmaps[i]);
				bounds.extend(new google.maps.LatLng(main_devices_data_gmaps[i]['data']['lat'], main_devices_data_gmaps[i]['data']['lon']));
				advJustSearch_self.applyIconToSearchedResult(main_devices_data_gmaps[i]['data']['lat'], main_devices_data_gmaps[i]['data']['lon']);
			}

            if(ipStationFound) {
                bounds.extend(new google.maps.LatLng(ipStation[0], ipStation[1]));
            }
		}


        if(advanceSearchMasterObj.searchedLinesByCircuitIDs.length) {
            for(var i=0; i< advanceSearchMasterObj.searchedLinesByCircuitIDs.length; i++) {
                bounds.extend(advanceSearchMasterObj.searchedLinesByCircuitIDs[i]);
            }
        }

		if(searchedStations.length) {
			if(searchedStations.length > advanceSearchMasterObj.maxSearchLevelNumber) {
   //              // $.gritter.add({
   //              //     // (string | mandatory) the heading of the notification
   //              //     title: 'GIS : Search',
   //              //     // (string | mandatory) the text inside the notification
   //              //     text: advanceSearchMasterObj.searchNumberLimitMessage,
   //              //     // (bool | optional) if you want it to fade out on its own or just sit there
   //              //     sticky: false
   //              // });
                advanceSearchMasterObj.searchedLinesByCircuitIDs= [];
                advJustSearch_self.resetPreviousSearchedMarkers();
            }

            mapInstance.fitBounds(bounds);
            if(mapInstance.getZoom() >= maxZoomLevel) {
                mapInstance.setZoom(maxZoomLevel);
            }
            advJustSearch_self.showNotification();
        } else {
			$.gritter.add({
				// (string | mandatory) the heading of the notification
				title: 'GIS : Search',
				// (string | mandatory) the text inside the notification
				text: 'No data found for the given Searchterm.',
				// (bool | optional) if you want it to fade out on its own or just sit there
				sticky: false
			});

			mapInstance.setCenter(new google.maps.LatLng(21.1500,79.0900));
			mapInstance.setZoom(5);
			advJustSearch_self.hideNotification();
		}

		hideSpinner();
		$("#advSearchFormContainer").html("");
		if(!($("#advSearchContainerBlock").hasClass("hide"))) {
			$("#advSearchContainerBlock").addClass("hide");
		}
	}

	/**
	 * This function reset all variable used in the process
	 * @class advanceSearchLib
	 * @method resetVariables
	 */
	this.resetVariables = function() {

		/*Reset the variable*/
		filtersJustInfoArray = [];
		templateJustData = "";
		formJustElements = "";
		elementsJustArray = [];
		resultantJustObject = {};
		searchJustParameters = "";
		appliedJustAdvSearch_Active= [];
        advanceSearchMasterObj.searchedLinesByCircuitIDs= [];
        filtersJustInfoArray = [],
        resultantJustObject = {},
        appliedJustAdvFilter = [],
        appliedJustAdvSearch_Active = [],
        searchJustParameters = "",
        lastJustSelectedValues = [];
        searchJustquery_data=[];
        result_Just_plot_devices=[]
	};
}