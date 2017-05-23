var map; // google map object
var poly; // google map polyline
var positions = new Array()
var altitudeInfo;
var planeMarker;
var label;



function initialize() {

	var mapOptions = {
		zoom: 8,
		center: new google.maps.LatLng(0, -180),
		mapTypeId: google.maps.MapTypeId.TERRAIN
	};

	document.getElementById("map-canvas").innerHTML = "Sample";

	map = new google.maps.Map(document.getElementById("map-canvas"),
	  mapOptions);

	var polyOptions = {
	    geodesic: true,
	    strokeColor: '#FF0000',
	    strokeOpacity: 1.0,
	    strokeWeight: 2
	};

	poly = new google.maps.Polyline(polyOptions);
	poly.setMap(map);


	var iconBase = '/images/';
	planeMarker = new google.maps.Marker({
	  map: map,
	  title: 'Altitude',
	  icon: iconBase + 'plane.png'
	});

	altitudeInfo = new google.maps.InfoWindow({
    });
    altitudeInfo.open(map, planeMarker);


    google.maps.event.addListener(planeMarker, 'click', function() {
		altitudeInfo.open(map, planeMarker);
	});

}





function AddPath(position) {

  var location = new google.maps.LatLng(position.lat, position.lng);
  var path = poly.getPath();

  // Because path is an MVCArray, we can simply append a new coordinate
  // and it will automatically appear.
  path.push(location);
  map.setCenter(location);
  planeMarker.setPosition(location)
}


function PositionExists(pos) {

	var rtnValue=false;
	for( var i in positions) {
		if(positions[i].lat == pos.lat && positions[i].lng == pos.lng) {
			rtnValue=true;
			break;
		}		
	}
	return rtnValue;
}


function GetCurrentLatLng() {

	// download and parse the json file
	$.getJSON("../mapData/latlng.json", function( data ) {

		// loop through all the items in the list
		$.each(data, function(i, item) {
			var t_pos = {lat:item[0], lng: item[1]}

			if(PositionExists(t_pos) != true) {	
				AddPath(t_pos);
		 		positions.push(t_pos);
		 	}
		});
	});

	// download and parse the json file
	$.getJSON("../mapData/alt.json", function( data ) {
		altitudeInfo.setContent("ALT: " + data.toString());
	});	
}


// load the google maps
google.maps.event.addDomListener(window, 'load', initialize);



$(document).ready(function(){

	$.ajaxSetup({ cache: false });
	setInterval(GetCurrentLatLng,1000);
}); 
