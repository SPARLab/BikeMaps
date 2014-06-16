// Leaflet map code and functions

/* GLOBAL VARIABLES */
var map, //global map object

	// Dynamically clustered point data layer
	accidentPoints = new L.MarkerClusterGroup({
		// maxClusterRadius: 50,
		// disableClusteringAtZoom: 16});
	}),

	userRoutes = new L.LayerGroup([]);

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

		stravaHM5 = L.tileLayer('http://gometry.strava.com/tiles/cycling/color5/{z}/{x}/{y}.png', {
			attribution: 'Ridership data &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>',
			minZoom: 3,
			maxZoom: 17,
			opacity: 0.8
		});

		mapquest = L.tileLayer('http://otile2.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
			attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">, \
	    	map data &copy <a href=http://openstreetmap.org>OpenStreetMap</a> contributors',
			maxZoom: 18
		}),

		skobbler = L.tileLayer('http://tiles1-b586b1453a9d82677351c34485e59108.skobblermaps.com/TileService/tiles/2.0/1112113120/10/{z}/{x}/{y}.png@2x', {
			attribution: '© Tiles: <a href="http://maps.skobbler.com/">skobbler</a>, Map data: <a href=http://openstreetmap.org>OpenStreetMap</a> contributors, CC-BY-SA',
		}),

		skobblerNight = L.tileLayer('http://tiles1-b586b1453a9d82677351c34485e59108.skobblermaps.com/TileService/tiles/2.0/1112113120/2/{z}/{x}/{y}.png@2x', {
			attribution: '© Tiles: <a href="http://maps.skobbler.com/">skobbler</a>, Map data: <a href=http://openstreetmap.org>OpenStreetMap</a> contributors, CC-BY-SA',
		}),
	
	/* MAP INIT AND DEFAULT LAYERS */
	map = L.map('map', {
		center: [48.5, -123.3],
		zoom: 11,
		layers: [skobbler, accidentPoints, userRoutes],
	});

	/* LAYER CONTROL */
	var baseMaps = {
			"Day": skobbler,
			"Night": skobblerNight,
			// "Open Cycle Map": openCycleMap,
		},
		overlayMaps = {
			"Accident points": accidentPoints,
			"Accident heat map": heatMap,
			"User route heat map": userRoutes,
			"Strava heat map": stravaHM5,
			"Bike Racks": racksCluster,
			"Bike lanes": bikeLanes,
		};
	L.control.layers(baseMaps, overlayMaps).addTo(map);


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


function getPolyline(latlng, freq) {
	userRoutes.addLayer(L.polyline(latlng, {
		color: 'red',
		width: 40,
		opacity: 0.1,
		lineCap: 'round',
		clickable: false,
	}));
}


function locateUser() {
	this.map.locate({
		setView: true
	});
}