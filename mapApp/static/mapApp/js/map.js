// Leaflet map code and functions

/* GLOBAL VARIABLES */
var map, //global map object

	// Dynamically clustered point data layer
	accidentPoints = new L.MarkerClusterGroup({
		// maxClusterRadius: 50,
		// disableClusteringAtZoom: 16});
	}),

	// Heatmap layer corresponding to all accident data
	heatMap = L.heatLayer([], {
		radius: 40,
		blur: 20,
	});

/* ICON DEFINITIONS */
var bikeRedIcon = L.MakiMarkers.icon({
		icon: "bicycle",
		color: "#d9534f",
		size: "m"
	}),
	bikeYellowIcon = L.MakiMarkers.icon({
		icon: "bicycle",
		color: "#f0ad4e",
		size: "m"
	}),
	bikeGreyIcon = L.MakiMarkers.icon({
		icon: "bicycle",
		color: "#999",
		size: "m"
	}),
	policeIcon = L.MakiMarkers.icon({
		icon: "police",
		color: "#004",
		size: "m"
	}),
	icbcIcon = L.MakiMarkers.icon({
		icon: "car",
		color: "#20a5de",
		size: "m"
	}),
	bikeRackIcon = L.MakiMarkers.icon({
		icon: "parking",
		color: "#111",
		size: "s"
	}),
	bikeRackIconAlt = L.MakiMarkers.icon({
		icon: bikeRackIcon.options.icon,
		color: "#333",
		size: "m"
	});

/* Create the map with a tile layer and set global variable map */
function initialize() {
	/* STATIC VECTOR DEFINITIONS */
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
		}).addTo(accidentPoints),


		icbcPoints = new L.geoJson(icbcData, {
			pointToLayer: function(feature, latlng) {
				heatMap.addLatLng(latlng);

				return L.marker(latlng, {
					icon: icbcIcon
				});
			},
			onEachFeature: function(feature, layer) {
				layer.bindPopup('<strong>' + feature.properties.Month + ' ' + feature.properties.Year + '</strong><br>');
			}
		}).addTo(accidentPoints),


		racksCluster = new L.MarkerClusterGroup({
			maxClusterRadius: 20,
			disableClusteringAtZoom: 18,
			iconCreateFunction: function(cluster) {
				if (cluster.getChildCount() != 1) {
					return bikeRackIconAlt;
				}
				return bikeRackIcon;
			},
		}),
		bikeRacksVictoria = new L.geoJson(bikeRacks, {
			pointToLayer: function(feature, latlng) {
				heatMap.addLatLng(latlng);

				return L.marker(latlng, {
					icon: bikeRackIcon
				});
			},
			onEachFeature: function(feature, layer) {
				layer.bindPopup('Bike rack');
			}
		}).addTo(racksCluster),


		bikeLanes = new L.geoJson(bikeRoutes, {
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

	/* TILE LAYER DEFINITIONS */
	var openCycleMap = L.tileLayer(
			'http://tile.opencyclemap.org/cycle/{z}/{x}/{y}.png', {
				attribution: '&copy <a href=http://openstreetmap.org>OpenStreetMap</a> contributors, CC-BY-SA',
				maxZoom: 18,
			}),

		mapbox = L.tileLayer('http://{s}.tiles.mapbox.com/v3/tayden.ibi2aoib/{z}/{x}/{y}.png', {
			attribution: 'Tiles courtesy of <a href=https://www.mapbox.com/>Mapbox</a>, \
	    	map data &copy <a href=http://openstreetmap.org>OpenStreetMap</a> contributors',
			maxZoom: 18
		}),

		mapboxSat = L.tileLayer('http://{s}.tiles.mapbox.com/v3/openstreetmap.map-4wvf9l0l/{z}/{x}/{y}.png', {
			attribution: 'Tiles courtesy of <a href=https://www.mapbox.com/>Mapbox</a>, \
	    	map data &copy <a href=http://openstreetmap.org>OpenStreetMap</a> contributors',
			maxZoom: 18
		}),

		stravaHM5 = L.tileLayer('http://gometry.strava.com/tiles/cycling/color5/{z}/{x}/{y}.png', {
			attribution: 'ridership data &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>',
			minZoom: 3,
			maxZoom: 17,
			opacity: 0.5
		});

	
	/* MAP INIT AND DEFAULT LAYERS */
	map = L.map('map', {
		center: [48.5, -123.3],
		zoom: 11,
		layers: [mapbox, accidentPoints],
	});

	/* LAYER CONTROL */
	var baseMaps = {
			"Map": mapbox,
			"Open Cycle Map": openCycleMap,
			"Satellite": mapboxSat,
		},
		overlayMaps = {
			"Accident points": accidentPoints,
			"Bike lanes": bikeLanes,
			"Accident heat map": heatMap,
			"Ridership heat map": stravaHM5,
			"Bike Racks": racksCluster,
		};
	L.control.layers(baseMaps, overlayMaps, {collapsed:false}).addTo(map);


	/* DRAWING CONTROL */
	L.drawLocal.draw.toolbar.buttons.marker = 'Add an incident marker';
	L.drawLocal.draw.handlers.marker.tooltip.start = 'Place me where the incident occurred';
	L.drawLocal.draw.toolbar.buttons.polyline = 'Add your cycling route';

	map.addControl(new L.Control.Draw({
		draw: {
			polyline: {
				shapeOptions: {
					color: '#f357a1',
					weight: 5
				}
			},
			polygon: false,
			rectangle: false,
			circle: false,
			marker: {
				icon: bikeGreyIcon,
			}
		},
		edit: false,
	}));

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