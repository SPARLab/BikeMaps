// Leaflet map code and functions

// Global map object
var map;


/* Create the map with a tile layer and set global variable map */
function initialize(){

	/* OSM Cycle Map basemap tile layer */
	mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
	ocmlink = '<a href="http://thunderforest.com/">Thunderforest</a>';
	var OCM = L.tileLayer(
	    'http://{s}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png', {
	    attribution: '&copy; '+mapLink+' Contributors & '+ocmlink,
	    maxZoom: 18,
	    });

	/* Mapbox basemap tile layer */
	var mapBox = L.tileLayer('http://{s}.tiles.mapbox.com/v3/tayden.ibi2aoib/{z}/{x}/{y}.png', {
	    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> \
	    	contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, \
	    	Imagery © <a href="http://mapbox.com">Mapbox</a>',
	    maxZoom: 18
	});
	
	/* OSM Strava heatmap tile layer */
	var stravaHM = L.tileLayer('http://gometry.strava.com/tiles/cycling/color1/{z}/{x}/{y}.png', {
	    attribution: 'Heatmap &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>',
	    minZoom: 3,
	    maxZoom: 17,
	    opacity: 0.5
	});


	/* Define which map tiles are basemaps */
	var baseMaps = {
		"MapBox": mapBox,
		"Open Cycle Map": OCM
	};

	/* Define which map tiles are overlays */
	var overlayMaps = {
		"Strava heatmap": stravaHM
	};
	
	/* Set map center, zoom, and default layers */
	map = L.map('map', {
		center: [48.455, -123.3],
		zoom: 13,
		layers: [mapBox, stravaHM]
	});
	
	/* Create the control panel and render the map */
	L.control.layers(baseMaps, overlayMaps).addTo(map);

}




/* Create a popup when map is clicked with button to  */
function addNewPoint(e) {
	var popup = L.popup();
    popup
        .setLatLng(e.latlng)
        // How to move this to index.html and pass as parameter?
        .setContent('<button class="btn btn-primary btn-lg" data-toggle="modal" \
        	data-target="#incidentForm">Add an incident</button>')
        .openOn(map);

    //Set point field in form to click location
    document.getElementById("point").value = ('Point('+e.latlng.lng+' '+e.latlng.lat+')');
}


function addPoint(latlng, blurb) {
	marker = L.marker(latlng).addTo(map);
    marker.bindPopup(blurb);
}


function toggleUserData() {
	return
}
function toggleHeatmap() {
	return
} 

function toggleICBC() {
	return
}
function toggleICBCHM() {
	return
}

function toggleBikeRacks() {
	return
}

function toggleUserData() {
	return
}