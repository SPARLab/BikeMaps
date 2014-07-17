// Leaflet map code and functions

/* GLOBAL VARIABLES */
var map; //global map object
	// Dynamically clustered point data layer
	// accidentPoints = new L.LayerGroup({

/* ICON DEFINITIONS */
var bikeRedIcon = L.MakiMarkers.icon({
		icon: "bicycle",
		color: "#d9534f",
		size: "m"
	}),
	bikeYellowIcon = L.MakiMarkers.icon({
		icon: bikeRedIcon.options.icon,
		color: "#f0ad4e",
		size: "m"
	}),
	bikeGreyIcon = L.MakiMarkers.icon({
		icon: "bicycle",
		color: "#999999",
		size: "m"
	}),
	policeIcon = L.MakiMarkers.icon({
		icon: "police",
		color: "#000044",
		size: "m"
	}),
	icbcIcon = L.MakiMarkers.icon({
		icon: "car",
		color: "#20a5de",
		size: "m"
	});
	geocodeIcon = L.MakiMarkers.icon({
		icon: "embassy",
		color: "#CC2A01",
		size: "l"
	});

/* DATASETS */
	// Cluster group for all accident data
var	accidentPoints = new L.MarkerClusterGroup({
		maxClusterRadius: 70,
		polygonOptions: {
			color: '#2c3e50',
			weight: 3
		},
		iconCreateFunction: createPieCluster
	}),

	alertAreas = new L.FeatureGroup([]),

	// Heatmap layer corresponding to all accident data
	heatMap = L.heatLayer([], {
		radius: 40,
		blur: 20,
	}),

	// Bike rack cluster
	racksCluster = new L.MarkerClusterGroup({
		showCoverageOnHover: false,
		// spiderfyOnMaxZoom: false,
		maxClusterRadius: 20,
		singleMarkerMode: true,
		iconCreateFunction: function(cluster) {
			var c = ' rack-cluster-'
			if (cluster.getChildCount() > 1) {
				c += 'medium';
				size = new L.Point(10,10);
			} else {
				c += 'small';
				size = new L.Point(5,5);
			}

			return new L.DivIcon({ className: 'rack-cluster' + c, iconSize: size});
		},
	});


/* Create the map with a tile layer and set global variable map */
function initialize(lat, lng, zoom) {
	/* STATIC VECTOR DEFINITIONS */
	initializeGeoJsonLayers();

	/* TILE LAYER DEFINITIONS */
	var stravaUrl = 'http://gometry.strava.com/tiles/cycling/color5/{z}/{x}/{y}.png',
		stravaAttrib = 'Ridership data &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>',
		stravaHM = L.tileLayer(stravaUrl, {minZoom: 3, maxZoom: 17, opacity: 0.8, attribution: stravaAttrib}),

		// Based on OSM data
		skobblerUrl = 'http://tiles1-b586b1453a9d82677351c34485e59108.skobblermaps.com/TileService/tiles/2.0/1111113120/10/{z}/{x}/{y}.png@2x',
		skobblerAttrib = '© Tiles: <a href="http://maps.skobbler.com/">skobbler</a>, Map data: <a href=http://openstreetmap.org>OpenStreetMap</a> contributors, CC-BY-SA',
		skobbler = L.tileLayer(skobblerUrl, {minZoom: 2, attribution: skobblerAttrib}),

		skobblerNightUrl = 'http://tiles1-b586b1453a9d82677351c34485e59108.skobblermaps.com/TileService/tiles/2.0/1111113120/2/{z}/{x}/{y}.png@2x',
		skobblerNightAttrib = '© Tiles: <a href="http://maps.skobbler.com/">skobbler</a>, Map data: <a href=http://openstreetmap.org>OpenStreetMap</a> contributors, CC-BY-SA',
		skobblerNight = L.tileLayer(skobblerNightUrl, {minZoom: 2, attribution: skobblerNightAttrib});
	
	/* MAP INIT AND DEFAULT LAYERS */
	map = L.map('map', {
		center: [48, -100],
		zoom: 4,
		layers: [skobbler, accidentPoints, stravaHM, alertAreas],
	});
	if(zoom){
		this.map.setView(L.latLng(lat,lng), zoom);
	}
	else{
		locateUser();
	}

	/* LAYER CONTROL */
	var baseMaps = {
			"Day": skobbler,
			"Night": skobblerNight,
		},
		overlayMaps = {
			"Accident points": accidentPoints,
			"Accident heat map": heatMap,
			"Strava heat map": stravaHM,
			"Bike Racks": racksCluster,
			"Alert Areas": alertAreas,
		};
	L.control.layers(baseMaps, overlayMaps).addTo(map);

	/* GEOCODING SEARCH BAR CONTROL */
	var geocoder = L.Control.geocoder({
		position: "bottomright"
	}).addTo(map);

	var geocodeMarker;
	geocoder.markGeocode = function(result){
		map.fitBounds(result.bbox);

		if (geocodeMarker) {
			map.removeLayer(geocodeMarker);
		}

		geocodeMarker = new L.Marker(result.center, {
			icon: geocodeIcon
		})
			.bindPopup(result.name)
			.addTo(map)
			.openPopup();
	};
	
	/* GET GEOJSON STATIC LAYERS AND STORE AS LEAFLET FEATURE */
	function initializeGeoJsonLayers(){
		var policePoints = new L.geoJson(policeData, {
			pointToLayer: function(feature, latlng) {
				heatMap.addLatLng(latlng);

				return L.marker(latlng, {
					icon: policeIcon
				});
			},
			onEachFeature: function(feature, layer) {
				var date = feature.properties.ACC_DATE.split("/");
				date = getMonthFromInt(parseInt(date[1])) + ' ' + date[2] + ', ' + date[0]; 	// Month dd, YYYY
				layer.bindPopup('<strong>Source:</strong> Victoria Police Dept.<br><strong>Date:</strong> ' + date);
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
				var date = toTitleCase(feature.properties.Month) + " " + feature.properties.Year;
				layer.bindPopup('<strong>Source:</strong> ICBC<br><strong>Date: </strong>' + date);
			}
		}).addTo(accidentPoints),

		bikeRacksVictoria = new L.geoJson(bikeRacks, {
			pointToLayer: function(feature, latlng) {
				return L.marker(latlng);
			},
			onEachFeature: function(feature, layer) {
				layer.bindPopup('Bike rack');
			}
		}).addTo(racksCluster);
	};
	
	/* FIND AND RETURN THE USER'S LOCATION */
	function locateUser() {
		this.map.locate({
			setView: true,
			maxZoom: 16
		});
	};
}

// Purpose: Add a given latlng poing with the given information to the map. 
// 		Add pk for easy lookup of marker for admin tasks
function getPoint(latlng, date, type, pk) {
	heatMap.addLatLng(latlng);

	var icon;
	if (type == "Collision") {
		icon = bikeRedIcon;
	} else {
		icon = bikeYellowIcon;
	}
	marker = L.marker(latlng, {
		icon: icon,
		pk:pk,
		objType: 'point'
	});

	date = date.split(",");
	date = date[0] + ',' + date[1]
	marker.bindPopup('<strong>Source:</strong> User submitted<br><strong>Date:</strong> ' + date + '<br><strong>Type:</strong> ' + type);

	accidentPoints.addLayer(marker);
};

// Purpose: Add a given latlng list to the map as a polygon. Add pk attribute so polygon can be deleted by user.
function getPolygon(latlng, pk) {
	alertAreas.addLayer(L.polygon(latlng, {
		color: '#3b9972',
		weight: 3,
		opacity: 1,
		pk: pk,	/*Mark the polygon with it's database id*/
		objType: 'polygon'
	}));
};


// Purpose: Initializes the Pie chart cluster icons by getting the needed attributes from each cluster
//		and passing them to the pieChart function
function createPieCluster(cluster) {
	var children = cluster.getAllChildMarkers();

	var	n = children.length,
		nPolice = 0,
		nIcbc = 0,
		nBikeR = 0,
		nBikeY = 0,
		nUnknown = 0,
		marker;
	
	//Count the number of markers in each cluster
	children.forEach( function(c) {
		marker = c.options.icon.options; // options for each point in clusters icon, used here to differentiate the points in each cluster
		if (marker.icon === policeIcon.options.icon) {
			nPolice++;
		} else if (marker.icon === icbcIcon.options.icon) {
			nIcbc++;
		} else if (marker.icon === bikeRedIcon.options.icon && marker.color === bikeRedIcon.options.color) {
			nBikeR++;
		} else if (marker.icon === bikeYellowIcon.options.icon && marker.color === bikeYellowIcon.options.color) {
			nBikeY++;
		} else {
			nUnknown++;
		}
	});

	// if(nUnknown > 0){
	// 	console.log("error");
	// }
	var outerR = 20, 
		innerR = 10;
	if(n>=50){
		outerR += 5;
		innerR += 3; 
	}else if(n<10){
		outerR -= 5;
		innerR -= 3;
	}

	var data = [{
		"type": 'Police',
		"count": nPolice,
		"color": policeIcon.options.color
		}, {
		"type": 'ICBC',
		"count": nIcbc,
		"color": icbcIcon.options.color
		}, {
		"type": 'BikeR',
		"count": nBikeR,
		"color": bikeRedIcon.options.color
		}, {
		"type": 'BikeY',
		"count": nBikeY,
		"color": bikeYellowIcon.options.color
		}, {
		"type": 'Unknown',
		"count": nUnknown,
		"color": bikeGreyIcon.options.color
	}];

	// Build the svg layer
	return pieChart(data, outerR, innerR, n);
};


// pieChart
// 	Purpose: Builds the svg DivIcons
// 	inputs: data as list of objects containing "type", "count", "color", outer chart radius, inner chart radius, and total points for cluster
// 	output: L.DivIcon donut chart where each "type" is mapped to the corresponding "color" with a proportional section corresponding to "count"
function pieChart(data, outerR, innerR, total){
	var arc = d3.svg.arc()
		.outerRadius(outerR)
		.innerRadius(innerR);

	var pie = d3.layout.pie()
		.sort(null)
		.value(function(d) { return d.count; });

	// Define the svg layer
	var width = 50, 
		height = 50;
	var svg = document.createElementNS(d3.ns.prefix.svg, 'svg');	
	var vis = d3.select(svg)
		.data(data)
		.attr('class', 'marker-cluster-pie')
		.attr('width', width)
		.attr('height', height)
		.append("g")
		.attr('transform', 'translate(' + width/2 + ',' + height/2 + ')');

	var g = vis.selectAll(".arc")
		.data(pie(data))
		.enter().append("g")
		.attr('class', 'arc');

	g.append('path')
		.attr("d", arc)
		.style("fill", function(d) { return '#' + d.data.color; });

	// Add center fill
	vis.append("circle")
		.attr("cx", 0)
		.attr("cy", 0)
		.attr("r", innerR)
		.attr('class', 'center')
		.attr("fill", "#f1f1f1");

	// Add count text
	vis.append('text')
		.attr('class', 'pieLabel')
		.attr('text-anchor', 'middle')
		.attr('dy','.3em')
		.text(total)

	var html = serializeXmlNode(svg);

	return new L.DivIcon({
		html: html,
		className: 'marker-cluster',
		iconSize: new L.Point(40,40)
	});
};

// Purpose: Helper function to convert xmlNode to a string
function serializeXmlNode(xmlNode) {
    if (typeof window.XMLSerializer != "undefined") {
        return (new window.XMLSerializer()).serializeToString(xmlNode);
    } else if (typeof xmlNode.xml != "undefined") {
        return xmlNode.xml;
    }
    return "";
};


function getMonthFromInt(num){
	switch(num) {
		case 1:
			return "January";
		case 2:
			return "February";
		case 3:
			return "March";
		case 4:
			return "April";
		case 5:
			return "May";
		case 6:
			return "June";
		case 7:
			return "July";
		case 8:
			return "August";
		case 9:
			return "September";
		case 10:
			return "October";
		case 11:
			return "November";
		case 12:
			return "December";
	}
};


function toTitleCase(s){
    return s.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};
