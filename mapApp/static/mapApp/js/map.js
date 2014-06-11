// Leaflet map code and functions

/* GLOBAL VARIABLES */

// Global map object
var map;

// Dynamically clustered point data layer
var accidentPoints = new L.MarkerClusterGroup({
		maxClusterRadius: 50
	}); //, disableClusteringAtZoom: 16});

// Heatmap layer corresponding to all accident data
var heatMap = L.heatLayer([], {
	radius: 50,
	blur: 20,
	opacity: 1
});

// Custom icons (Using Maki icon symbols)
var bikeRedIcon = L.MakiMarkers.icon({
	icon: "bicycle",
	color: "#d9534f",
	size: "m"
});
var bikeYellowIcon = L.MakiMarkers.icon({
	icon: "bicycle",
	color: "#f0ad4e",
	size: "m"
});
var policeIcon = L.MakiMarkers.icon({
	icon: "police",
	color: "#428bca",
	size: "m"
});

var policePoints = new L.geoJson(policeData, {
	pointToLayer: function(feature, latlng) {
		heatMap.addLatLng(latlng);
		
		return L.marker(latlng, {
			icon: policeIcon
		});
	},
	onEachFeature: function(feature, layer) {
		layer.bindPopup('<strong>' + feature.properties.ACC_DATE + '</strong><br>' + feature.properties.ACC_TYPE);
	}
});
policePoints.addTo(accidentPoints);

var bikeLanes = new L.geoJson(bikeRoutes, {
	style: function(feature) {
		switch (feature.properties.Descriptio) {
			case 'Buffered Bike Lane':
				return {
					color: '#007f16', // Dark green
				};
			case 'Cycle Track*':
				return {
					color: '#259238', // Faded dark green
					opacity: 0.8
				};
			case 'Multi-Use Trail':
				return {
					color: '#87a000', // Dark Yellow
					opacity: 0.8
				};
			case 'Conventional Bike Lane':
				return {
					color: '#00c322', // Green
					opacity: 0.8
				};
			case 'Priority Transit and Cycling Lanes*':
				return {
					color: '#05326d', // Dark blue
					opacity: 0.8
				};
			case 'Signed Bike Route':
				return {
					color: '#0e51a7', // blue
					opacity: 0.8
				};
			case 'Proposed Bicycle Network':
				return {
					color: '#ff9e00', // Faded green
					opacity: 0.3
				};
		}
	}
});

var drawnItems = new L.FeatureGroup();



/* Create the map with a tile layer and set global variable map */
function initialize() {
	var openCycleMap = L.tileLayer(
		'http://tile.opencyclemap.org/cycle/{z}/{x}/{y}.png', {
			attribution: '&copy <a href=http://openstreetmap.org>OpenStreetMap</a> contributors, CC-BY-SA',
			maxZoom: 18,
		});

	var mapbox = L.tileLayer('http://{s}.tiles.mapbox.com/v3/tayden.ibi2aoib/{z}/{x}/{y}.png', {
		attribution: 'Tiles courtesy of <a href=https://www.mapbox.com/>Mapbox</a>, \
	    	map data &copy <a href=http://openstreetmap.org>OpenStreetMap</a> contributors',
		maxZoom: 18
	});

	var mapboxSat = L.tileLayer('http://{s}.tiles.mapbox.com/v3/openstreetmap.map-4wvf9l0l/{z}/{x}/{y}.png', {
		attribution: 'Tiles courtesy of <a href=https://www.mapbox.com/>Mapbox</a>, \
	    	map data &copy <a href=http://openstreetmap.org>OpenStreetMap</a> contributors',
		maxZoom: 18
	});

	var stravaHM5 = L.tileLayer('http://gometry.strava.com/tiles/cycling/color5/{z}/{x}/{y}.png', {
		attribution: 'ridership data &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>',
		minZoom: 3,
		maxZoom: 17,
		opacity: 0.5
	});

	/* Define which map tiles are basemaps */
	var baseMaps = {
		"Map": mapbox,
		"Open Cycle Map": openCycleMap,
		"Satellite": mapboxSat,
	};

	/* Define which map tiles are overlays */
	var overlayMaps = {
		"Accident points": accidentPoints,
		"Bike lanes": bikeLanes,
		"Accident heat map": heatMap,
		"Ridership heat map": stravaHM5,
	}

	/* DEFAULTS AND PANEL */
	/* Set map center, zoom, default layers and render */
	map = L.map('map', {
		drawControl: true,
		center: [48.5, -123.3],
		zoom: 11,
		layers: [mapbox, accidentPoints, bikeLanes],
		/* Layers to display on load */
	});

	/* Create the control panel */
	L.control.layers(baseMaps, overlayMaps).addTo(map);
}


/* Create a popup when map is clicked with button to add a new point  */
function setPoint(layer) {
	var popup = L.popup({
		'closeOnClick': true,
	});
	popup
		.setLatLng(layer.getLatLng())
		.setContent('<button class="btn btn-primary btn-lg" data-toggle="modal" \
        	data-target="#incidentForm"><span class="glyphicon glyphicon-pushpin"></span></button>')
		.openOn(map);

	//Set point field in form to click location
	document.getElementById("point").value = ('Point(' + layer.getLatLng().lng + ' ' + layer.getLatLng().lat + ')');
}


function getPoint(latlng, msg, type) {
	heatMap.addLatLng(latlng);

	var icon;
	if (type == "police") {
		icon = policeIcon;
	} else if (type == "Collision") {
		icon = bikeRedIcon;
	} else {
		icon = bikeYellowIcon;
	}
	marker = L.marker(latlng, {
		icon: icon
	});
	marker.bindPopup(msg);

	accidentPoints.addLayer(marker);
}

function toggleICBC() {
	return
}

function toggleBikeRacks() {
	return
}

function locateUser() {
	this.map.locate({
		setView: true
	});
}