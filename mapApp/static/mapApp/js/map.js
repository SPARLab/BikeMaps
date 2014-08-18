var DISABLE_GEOFENCES = false;

/* GLOBAL VARIABLES */
var map;

// Icon definitions
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
	bikeOrangeIcon = L.MakiMarkers.icon({
		icon: bikeRedIcon.options.icon,
		color: "#d9844f",
		size: "m"
	}),
	bikeGreyIcon = L.MakiMarkers.icon({
		icon: "bicycle",
		color: "#999999",
		size: "m"
	}),
	hazardIcon = L.MakiMarkers.icon({
		icon: "triangle-stroked",
		color: "#3eab45",
		size: "m"
	}),
	theftIcon = L.MakiMarkers.icon({
		icon: "bicycle",
		color: "#000000",
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
	}),
	geocodeIcon = L.MakiMarkers.icon({
		icon: "embassy",
		color: "#CC2A01",
		size: "l"
	}),
	locationIcon = L.MakiMarkers.icon({
		icon: "star",
		color: "#CC2A01",
		size: "s"
	});

// Layer datasets
// Cluster group for all accident data
var accidentPoints = new L.MarkerClusterGroup({
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

	// Tile layers
	// Skobbler settings flag reference at http://developer.skobbler.com/getting-started/web#sec0
	skobbler = L.tileLayer('http://tiles1-b586b1453a9d82677351c34485e59108.skobblermaps.com/TileService/tiles/2.0/0111113120/10/{z}/{x}/{y}.png@2x', {
		minZoom: 2,
		attribution: '© Tiles: <a href="http://maps.skobbler.com/">skobbler</a>, Map data: <a href=http://openstreetmap.org>OpenStreetMap</a> contributors, CC-BY-SA'
	}),

	skobblerNight = L.tileLayer('http://tiles1-b586b1453a9d82677351c34485e59108.skobblermaps.com/TileService/tiles/2.0/0111113120/2/{z}/{x}/{y}.png@2x', {
		minZoom: 2,
		attribution: '© Tiles: <a href="http://maps.skobbler.com/">skobbler</a>, Map data: <a href=http://openstreetmap.org>OpenStreetMap</a> contributors, CC-BY-SA'
	}),

	stravaHM = L.tileLayer('http://gometry.strava.com/tiles/cycling/color5/{z}/{x}/{y}.png', {
		minZoom: 3,
		maxZoom: 17,
		opacity: 0.8,
		attribution: 'Ridership data &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>'
	}),
	
	infrastructure = new L.FeatureGroup([]);

/* Create the map with a tile layer and set global variable map */
function initialize(mobile) {
	mobile = typeof mobile !== 'undefined' ? mobile : false; //default value of mobile is false

	// Static vector definitions 
	initializeDatasets();

	// Map init and default layers 
	map = L.map('map', {
		center: [48, -100],
		zoom: 4,
		layers: [skobbler, stravaHM, accidentPoints, alertAreas],
	});

	// Add all controls to the map
	addControls(mobile);

	$(document).ready(mapListen);

	function initializeDatasets() {
		// Police data
		L.geoJson(policeData, {
			pointToLayer: function(feature, latlng) {
				heatMap.addLatLng(latlng);

				return L.marker(latlng, {
					icon: policeIcon
				});
			},
			onEachFeature: function(feature, layer) {
				var date = feature.properties.ACC_DATE.split("/");
				date = getMonthFromInt(parseInt(date[1])) + ' ' + date[2] + ', ' + date[0]; // Month dd, YYYY
				layer.bindPopup('<strong>Source:</strong> Victoria Police Dept.<br><strong>Date:</strong> ' + date);
			}
		}).addTo(accidentPoints);

		// ICBC Data
		L.geoJson(icbcData, {
			pointToLayer: function(feature, latlng) {
				heatMap.addLatLng(latlng);

				return L.marker(latlng, {
					icon: icbcIcon
				});
			},
			onEachFeature: function(feature, layer) {
				var date = toTitleCase(feature.properties.Month) + ", " + feature.properties.Year;
				layer.bindPopup('<strong>Source:</strong> ICBC<br><strong>Date: </strong>' + date);
			}
		}).addTo(accidentPoints);

		L.tileLayer.wms("https://bikemaps.org/WMS", {
			layers: 'bikemaps_infrastructure',
			format: 'image/png',
			transparent: true,
			version: '1.3.0'
		}).addTo(infrastructure);
	};

	function addControls(mobile) {
		/* LAYER CONTROL */
		layerControl = L.control.layers([], [], {
			collapsed: mobile
		});

		// Add layers
		// Basemaps
		// layerControl.addBaseLayer(skobbler, '<i class="fa fa-sun-o"></i> Light map');
		// layerControl.addBaseLayer(skobblerNight, '<i class="fa fa-moon-o"></i> Dark map');
		
		layerControl.addOverlay(stravaHM, 'Rider volume<br>' +
			'<div id=strava-legend class="legend-subtext collapse in">' +
			'<small class="strava-gradient gradient-bar">less <div class="pull-right">more</div></small>' + 
			'</div>');
		
		layerControl.addOverlay(accidentPoints,
			'Incident points<br>'
			+'<div id=incident-legend class="marker-group legend-subtext collapse in">' 
			+	'<img src="https://api.tiles.mapbox.com/v3/marker/pin-s' + '-' + bikeRedIcon.options.icon + '+' + bikeRedIcon.options.color + '.png">'
			+		' <small>Citizen collision report</small><br>' 
			
			+	'<img src="https://api.tiles.mapbox.com/v3/marker/pin-s' + '-' + bikeOrangeIcon.options.icon + '+' + bikeOrangeIcon.options.color + '.png">'
			+		' <small>Citizen near miss report</small><br>' 
			
			+	'<img src="https://api.tiles.mapbox.com/v3/marker/pin-s' + '-' + bikeYellowIcon.options.icon + '+' + bikeYellowIcon.options.color + '.png">'
			+		' <small>Citizen fall report</small><br>' 
			
			+	'<img src="https://api.tiles.mapbox.com/v3/marker/pin-s' + '-' + hazardIcon.options.icon + '+' + hazardIcon.options.color + '.png">'
			+		' <small>Cyclist hazard</small><br>' 
			
			+	'<img src="https://api.tiles.mapbox.com/v3/marker/pin-s' + '-' + icbcIcon.options.icon + '+' + icbcIcon.options.color + '.png">'
			+		' <small>Insurance report</small><br>' 
			
			+	'<img src="https://api.tiles.mapbox.com/v3/marker/pin-s' + '-' + policeIcon.options.icon + '+' + policeIcon.options.color + '.png">'
			+		' <small>Police report</small><br>' 
			
			+	'<img src="https://api.tiles.mapbox.com/v3/marker/pin-s' + '-' + theftIcon.options.icon + '+' + theftIcon.options.color + '.png">'
			+		' <small>Bike Theft</small>' 
			+'</div>'
		);
		
		if (!DISABLE_GEOFENCES) {
			layerControl.addOverlay(alertAreas, 'Alert Areas' +
				'   <a data-target="#about-alert-areas" data-toggle="modal" href="#"><i class="fa fa-question-circle fa-1x"></i></a><br>' +
				'<div id="alert-areas-legend" class="legend-subtext collapse in">' +
				'<small class="alert-area-box"></small>' +
				'</div>'
			);
		}

		infrastructureLegendHTML = "Infrastructure<br>" +
			'<div id="infrastructure-legend" class="legend-subtext collapse">' +
			'<small> Bike rack</small><br>' +
			'<small> Separated lane</small><br>' +
			'<small> Shared lane</small></div>';

		layerControl.addOverlay(infrastructure, infrastructureLegendHTML);
		
		layerControl.addOverlay(heatMap, 'Incident heatmap<br>' +
			'<div id="hm-legend" class="legend-subtext collapse">' +
			'<small class="rainbow-gradient gradient-bar">less <div class="pull-right">more</div></small>' +
			'</div>');

		layerControl.addTo(map);

		/* GEOCODING SEARCH BAR CONTROL */
		var geocoder = L.Control.geocoder({
			position: "topleft"
		}).addTo(map);

		var geocodeMarker;
		geocoder.markGeocode = function(result) {
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

		/* ADD SCALE BAR */
		L.control.scale({
			position: 'bottomright'
		}).addTo(map);

		/* ADD CUSTOM HELP BUTTON */
		L.easyButton('bottomright', 'fa-question-circle',
			function() {
				toggleTooltips("show")
			},
			'Get Help'
		);
	};

	function mapListen(){
		// Listener events for locating the user
		map.on('locationerror', onLocationError);
		map.on('locationfound', onLocationFound);
		
		function onLocationError(e) {
			alert(e.message);
		};

		function onLocationFound(e) {
			// console.log('location found');
			// if(locationGroup) layerControl.removeLayer(locationGroup);
			var radius = Math.round((((e.accuracy / 2)+0.00001)*100)/100), //Round accuracy to two decimal places

				marker = L.marker(e.latlng, {
					icon: locationIcon
				})
				.bindPopup("You are within " + radius + " meters of this point"),
				circle = L.circle(e.latlng, radius, {
					color: "#" + locationIcon.options.color,
					weight: 1,
					opacity: 0.3,
					clickable: false,
					fillOpacity: 0.05
				});

			locationGroup = L.layerGroup([marker, circle]);
			layerControl.addOverlay(locationGroup, 'Detected location<br>' +
				'<div id="location-legend" class="marker-group legend-subtext collapse">' +
				'<img src="https://api.tiles.mapbox.com/v3/marker/pin-s' + '-' + locationIcon.options.icon + '+' + locationIcon.options.color + '.png"> <small>You are here</small></div>' +
				'</div>');
			locationGroup.addTo(map);
		};


		//Listener events for toggling legend items
		map.on('overlayremove', collapseLegendItem);
		map.on('overlayadd', showLegendItem);

		function collapseLegendItem(e){
			if(e.name.match('Incident points.')){
				$('#incident-legend').collapse('hide');
			}
			else if(e.name.match('Rider volume.')){
				$('#strava-legend').collapse('hide');
			}
			else if(e.name.match('Infrastructure.')){
				$('#infrastructure-legend').collapse('hide');
			}
			else if(e.name.match('Incident heatmap.')){
				$('#hm-legend').collapse('hide');
			}
			else if(e.name.match('Detected location.')){
				$('#location-legend').collapse('hide');
			}		
			else if(e.name.match('Alert Areas.')){
				$('#alert-areas-legend').collapse('hide');
			}
		};

		function showLegendItem(e){
			if(e.name.match('Incident points.')){
				$('#incident-legend').collapse('show');
			}
			else if(e.name.match('Rider volume.')){
				$('#strava-legend').collapse('show');
			}
			else if(e.name.match('Infrastructure.')){
				$('#infrastructure-legend').collapse('show');
			}
			else if(e.name.match('Incident heatmap.')){
				$('#hm-legend').collapse('show');
			}	
			else if(e.name.match('Detected location.')){
				$('#location-legend').collapse('show');
			}			
			else if(e.name.match('Alert Areas.')){
				$('#alert-areas-legend').collapse('show');
			}
		};
	};
};

// Purpose: Locate the user and add their location to the map. 
// 		Given lat, lng, and zoom, go to that point, else to user location
function setView(lat, lng, zoom) {
	if (zoom) {
		this.map.setView(L.latLng(lat, lng), zoom);
		locateUser(setView = false);
	} else {
		locateUser(setView = true);
	}

	/* FIND AND RETURN THE USER'S LOCATION */
	function locateUser(setView) {
		this.map.locate({
			setView: setView,
			maxZoom: 16,
			// watch: true,
			enableHighAccuracy: true
		});
	};
};

// Purpose: Add a given latlng poing with the given information to the map. 
// 		Add pk for easy lookup of marker for admin tasks
function getPoint(latlng, date, type, pk) {
	heatMap.addLatLng(latlng);

	var icon;
	if (type === "Collision") {
		icon = bikeRedIcon;
		dataset = "incident"
	} else if (type === "Near miss") {
		icon = bikeOrangeIcon;
		dataset = "incident"
	} else if (type === "Fall") {
		icon = bikeYellowIcon;
		dataset = "incident"
	} else if (type === "Hazard") {
		icon = hazardIcon;
		dataset = "hazard"
	} else if (type === "Theft") {
		icon = theftIcon;
		dataset = "theft"
	} else {
		return;
	}

	marker = L.marker(latlng, {
		icon: icon,
		pk: pk,
		objType: dataset
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
		weight: 2,
		opacity: 0.6,
		fillOpacity: 0.1,
		pk: pk, /*Mark the polygon with it's database id*/
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
		nBikeO = 0,
		nBikeY = 0,
		nHazard = 0,
		nTheft = 0,
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
		} else if (marker.icon === bikeOrangeIcon.options.icon && marker.color === bikeOrangeIcon.options.color) {
			nBikeO++;
		} else if (marker.icon === bikeYellowIcon.options.icon && marker.color === bikeYellowIcon.options.color) {
			nBikeY++;
		} else if (marker.icon === hazardIcon.options.icon && marker.color === hazardIcon.options.color) {
			nHazard++;
		} else if (marker.icon === theftIcon.options.icon && marker.color === theftIcon.options.color) {
			nTheft++;
		} else {
			nUnknown++;
		}
	});

	// if(nUnknown > 0){
	// 	console.log("Unknown cluster points found");
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
		"type": 'BikeO',
		"count": nBikeO,
		"color": bikeOrangeIcon.options.color
		}, {
		"type": 'BikeY',
		"count": nBikeY,
		"color": bikeYellowIcon.options.color
		}, {
		"type": 'Hazard',
		"count": nHazard,
		"color": hazardIcon.options.color
		}, {
		"type": 'Theft',
		"count": nTheft,
		"color": theftIcon.options.color
		}, {
		"type": 'Unknown',
		"count": nUnknown,
		"color": bikeGreyIcon.options.color
	}];

	// Build the svg layer
	return pieChart(data, outerR, innerR, n);
	

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
		

		// Purpose: Helper function to convert xmlNode to a string
		function serializeXmlNode(xmlNode) {
		    if (typeof window.XMLSerializer != "undefined") {
		        return (new window.XMLSerializer()).serializeToString(xmlNode);
		    } else if (typeof xmlNode.xml != "undefined") {
		        return xmlNode.xml;
		    }
		    return "";
		};
	};
};


function getMonthFromInt(num) {
	months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	return months[num - 1];
};


function toTitleCase(s) {
	return s.replace(/\w\S*/g, function(txt) {
		return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
	});
};