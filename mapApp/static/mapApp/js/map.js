// Leaflet map code and functions

// Global map object
var map;


/* Create the map with a tile layer and set global variable map */
function initialize(){
	map = L.map('map').setView([48.455, -123.3], 13);

	/* Render OSM Cycle Map */
	// mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
	// ocmlink = '<a href="http://thunderforest.com/">Thunderforest</a>';
	// L.tileLayer(
	//     'http://{s}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png', {
	//     attribution: '&copy; '+mapLink+' Contributors & '+ocmlink,
	//     maxZoom: 18,
	//     }).addTo(map)

	/* Render Mapbox tiles */
	L.tileLayer('http://{s}.tiles.mapbox.com/v3/tayden.ibi2aoib/{z}/{x}/{y}.png', {
	    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> \
	    	contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, \
	    	Imagery © <a href="http://mapbox.com">Mapbox</a>',
	    maxZoom: 18
	}).addTo(map);
}


function addPoint(latlng, blurb) {
	marker = L.marker(latlng).addTo(map);
    marker.bindPopup(blurb);
}

/* Create a popup when map is clicked with button to  */
function addNewPoint(e) {
	var popup = L.popup();
    popup
        .setLatLng(e.latlng)
        .setContent('<button class="btn btn-primary btn-lg" data-toggle="modal" \
        	data-target="#incidentForm">Add an incident</button>')
        // .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);

    //Set point field in form to click location
    document.getElementById("point").value = ('Point('+e.latlng.lng+' '+e.latlng.lat+')');
}