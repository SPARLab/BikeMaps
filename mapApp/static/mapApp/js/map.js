// Leaflet map code and functions

// Global map object
var map;


/* Create the map with a tile layer and set global variable map */
function initialize(){


	/* Used <http://josm.openstreetmap.de/wiki/Maps> for map tiles */

/* BASEMAPS */
	/* We don't need all of these. Just for visualization so we can pick a few */
	/* OSM Cycle Map basemap tile layer */	
	var openCycleMap = L.tileLayer(
	    'http://tile.opencyclemap.org/cycle/{z}/{x}/{y}.png', {
	    attribution: '&copy <a href=http://openstreetmap.org>OpenStreetMap</a> contributors, CC-BY-SA',
	    maxZoom: 18,
	    });
	

	var mapbox = L.tileLayer('http://{s}.tiles.mapbox.com/v3/tayden.ibi2aoib/{z}/{x}/{y}.png', {
	    attribution: 'Tiles Courtesy of <a href=https://www.mapbox.com/>Mapboxt</a>, \
	    	map data &copy <a href=http://openstreetmap.org>OpenStreetMap</a> contributors',
	    maxZoom: 18
	});

    var humanitarianOSM = L.tileLayer('http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
	    attribution: '&copy <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, tiles courtesy of <a href=http://hot.openstreetmap.org/>Humanitarian OpenStreetMap Team</a>',
	    maxZoom: 20
	});

    var mapboxSat = L.tileLayer('http://{s}.tiles.mapbox.com/v3/openstreetmap.map-4wvf9l0l/{z}/{x}/{y}.png', {
    	attribution: 'Tiles Courtesy of <a href=https://www.mapbox.com/>Mapboxt</a>, \
	    	map data &copy <a href=http://openstreetmap.org>OpenStreetMap</a> contributors',
	    maxZoom: 18
	});

    var mapQuest = L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
	    attribution: 'Tiles Courtesy of <a href=https://open.mapquest.com/>MapQuest</a>, \
	    	map data &copy <a href=http://openstreetmap.org>OpenStreetMap</a> contributors',
	    maxZoom: 18,
	    subdomains: '1234' // Switch between subdomains {s} 1,2,3,4 instead of a,b,c
	});


	var osmMapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	    attribution: '&copy <a href=https://openstreetmap.org/>OpenStreetMap</a> contributors, CC-BY-SA',
	    maxZoom: 19,
	});


	var osmMapnikBW = L.tileLayer('http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png', {
	    attribution: '&copy <a href=https://openstreetmap.org/>OpenStreetMap</a> contributors, CC-BY-SA',
	    maxZoom: 18,
	});


	/* Define which map tiles are basemaps */
	var baseMaps = {
		"Open Street Map": osmMapnik,
		"Open Street Map B&W": osmMapnikBW,
		"Open Cycle Map": openCycleMap,
		"Humanitarian OSM": humanitarianOSM,
		"Mapbox": mapbox,
		"Mapbox Satellite": mapboxSat,
		"MapQuest OSM": mapQuest,

	};



/* OVERLAY MAPS */
	
	/* OSM Strava heatmap tile layer */
	var stravaHM1 = L.tileLayer('http://gometry.strava.com/tiles/cycling/color1/{z}/{x}/{y}.png', {
	    attribution: 'Heatmap &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>',
	    minZoom: 3,
	    maxZoom: 17,
	    opacity: 0.5
	});

	var stravaHM2 = L.tileLayer('http://gometry.strava.com/tiles/cycling/color2/{z}/{x}/{y}.png', {
	    attribution: 'Heatmap &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>',
	    minZoom: 3,
	    maxZoom: 17,
	    opacity: 0.5
	});

	var stravaHM3 = L.tileLayer('http://gometry.strava.com/tiles/cycling/color3/{z}/{x}/{y}.png', {
	    attribution: 'Heatmap &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>',
	    minZoom: 3,
	    maxZoom: 17,
	    opacity: 0.5
	});

	var stravaHM4 = L.tileLayer('http://gometry.strava.com/tiles/cycling/color4/{z}/{x}/{y}.png', {
	    attribution: 'Heatmap &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>',
	    minZoom: 3,
	    maxZoom: 17,
	    opacity: 0.5
	});

	var stravaHM5 = L.tileLayer('http://gometry.strava.com/tiles/cycling/color5/{z}/{x}/{y}.png', {
	    attribution: 'Heatmap &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>',
	    minZoom: 3,
	    maxZoom: 17,
	    opacity: 0.5
	});

	var stravaHM6 = L.tileLayer('http://gometry.strava.com/tiles/cycling/color6/{z}/{x}/{y}.png', {
	    attribution: 'Heatmap &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>',
	    minZoom: 3,
	    maxZoom: 17,
	    opacity: 0.5
	});


	/* Define which map tiles are overlays */
	var overlayMaps = {
		"Strava heatmap 1": stravaHM1,
		"Strava heatmap 2": stravaHM2,
		"Strava heatmap 3": stravaHM3,
		"Strava heatmap 4": stravaHM4,
		"Strava heatmap 5": stravaHM5,
		"Strava heatmap 6": stravaHM6,
	}
/* DEFAULTS AND PANEL */	
	/* Set map center, zoom, and default layers */
	map = L.map('map', {
		center: [48.455, -123.3],
		zoom: 13,
		layers: [humanitarianOSM, stravaHM5]
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