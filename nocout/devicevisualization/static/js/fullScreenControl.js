function FullScreenControl(map) {
	var controlDiv = document.createElement('div');
	controlDiv.className = "fullScreen";
	controlDiv.index = 1;
	controlDiv.style.padding = '5px';

	// Set CSS for the control border.
	var controlUI = document.createElement('div');
	controlUI.style.backgroundColor = 'white';
	controlUI.style.borderStyle = 'solid';
	controlUI.style.borderWidth = '1px';
	controlUI.style.borderColor = '#717b87';
	controlUI.style.cursor = 'pointer';
	controlUI.style.textAlign = 'center';
	controlUI.style.boxShadow = 'rgba(0, 0, 0, 0.298039) 0px 1px 4px -1px';
	controlDiv.appendChild(controlUI);

	// Set CSS for the control interior.
	var controlText = document.createElement('div');
	controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
	controlText.style.fontSize = '11px';
	controlText.style.fontWeight = '400';
	controlText.style.paddingTop = '1px';
	controlText.style.paddingBottom = '1px';
	controlText.style.paddingLeft = '6px';
	controlText.style.paddingRight = '6px';
	controlText.innerHTML = '<strong>Full Screen(Only Map)</strong>';
	controlUI.appendChild(controlText);

	// set print CSS so the control is hidden
	var head = document.getElementsByTagName('head')[0];
	var newStyle = document.createElement('style');
	newStyle.setAttribute('type', 'text/css');
	newStyle.setAttribute('media', 'print');
	try{newStyle.appendChild(document.createTextNode('.fullScreen { display: none;}'));}catch(err){}
	try{head.appendChild(newStyle);}catch(err){}	
	
	var fullScreen = false;
	var interval;
	var mapDiv = map.getDiv();
	var divStyle = mapDiv.style;
	if (mapDiv.runtimeStyle)
		divStyle = mapDiv.runtimeStyle;
	var originalPos = divStyle.position;
	var originalWidth = divStyle.width;
	var originalHeight = divStyle.height;
	
	// IE8 hack
	if (originalWidth == "")
		originalWidth = mapDiv.style.width;
	if (originalHeight == "")
		originalHeight = mapDiv.style.height;
	
	var originalTop = divStyle.top;
	var originalLeft = divStyle.left;
	var originalZIndex = divStyle.zIndex;

	var bodyStyle = document.body.style;
	if (document.body.runtimeStyle)
		bodyStyle = document.body.runtimeStyle;
	var originalOverflow = bodyStyle.overflow;
	
	var goFullScreen = function() {
		// Update the position prop from 'absolute' to 'fixed'
		$(".sideInfoContainer").css("position","fixed");

		if(mapDiv.style.height) {
			originalHeight = mapDiv.style.height;
		}
		
		var center = map.getCenter();
		mapDiv.style.position = "fixed";
		mapDiv.style.width = "100%";
		mapDiv.style.height = "100%";
		mapDiv.style.top = "0";
		mapDiv.style.left = "0";
		mapDiv.style.zIndex = "100";
		document.body.style.overflow = "hidden";
		controlText.innerHTML = '<strong>Exit full screen(Only Map)</strong>';
		fullScreen = true;
		google.maps.event.trigger(map, 'resize');
		map.setCenter(center);
		// this works around street view causing the map to disappear, which is caused by Google Maps setting the 
		// CSS position back to relative. There is no event triggered when Street View is shown hence the use of setInterval
		interval = setInterval(function() { 
				if (mapDiv.style.position != "fixed") {
					mapDiv.style.position = "fixed";
					google.maps.event.trigger(map, 'resize');
				}
			}, 100);
	};
	
	var exitFullScreen = function() {
		// Revert the position prop to absolute
		$(".sideInfoContainer").css("position","absolute");

		var center = map.getCenter();
		if (originalPos == "")
			mapDiv.style.position = "relative";
		else
			mapDiv.style.position = originalPos;
		mapDiv.style.width = originalWidth;
		mapDiv.style.height = originalHeight;
		mapDiv.style.top = originalTop;
		mapDiv.style.left = originalLeft;
		mapDiv.style.zIndex = originalZIndex;
		document.body.style.overflow = originalOverflow;
		controlText.innerHTML = '<strong>Full Screen(Only Map)</strong>';
		fullScreen = false;
		google.maps.event.trigger(map, 'resize');
		map.setCenter(center);
		clearInterval(interval);
	}
	
	// Setup the click event listener
	google.maps.event.addDomListener(controlUI, 'click', function() {
		if (!fullScreen) {
			if(mapInstance.controls[google.maps.ControlPosition.TOP_RIGHT].length) {
                $(mapInstance.controls[google.maps.ControlPosition.TOP_RIGHT].b[0]).addClass('hide');
                if(mapInstance.controls[google.maps.ControlPosition.TOP_RIGHT].length == 3) {
                	$(mapInstance.controls[google.maps.ControlPosition.TOP_RIGHT].b[2]).addClass('hide');
                }
            }
			goFullScreen();
		}
		else {
			if(mapInstance.controls[google.maps.ControlPosition.TOP_RIGHT].length) {
                $(mapInstance.controls[google.maps.ControlPosition.TOP_RIGHT].b[0]).removeClass('hide');
                if(mapInstance.controls[google.maps.ControlPosition.TOP_RIGHT].length == 3) {
                	$(mapInstance.controls[google.maps.ControlPosition.TOP_RIGHT].b[2]).removeClass('hide');
                }
            }
			exitFullScreen();
		}
	});
	
	return controlDiv;
}