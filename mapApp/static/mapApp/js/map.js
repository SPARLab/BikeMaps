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

/* DATASETS */
var	userRoutes = new L.LayerGroup([]),

	bikeLanes,

	// Heatmap layer corresponding to all accident data
	heatMap = L.heatLayer([], {
		radius: 40,
		blur: 20,
	}),

	// Cluster group for all accident data
	accidentPoints = new L.MarkerClusterGroup({
		maxClusterRadius: 70,
		polygonOptions: {
			color: '#2c3e50',
			weight: 3
		},
		iconCreateFunction: createPieCluster
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
function initialize() {
	/* STATIC VECTOR DEFINITIONS */
	initializeGeoJsonLayers();

	/* TILE LAYER DEFINITIONS */
	var stravaHM5 = L.tileLayer('http://gometry.strava.com/tiles/cycling/color5/{z}/{x}/{y}.png', {
			attribution: 'Ridership data &copy <a href=http://labs.strava.com/heatmap/>Strava labs</a>',
			minZoom: 3,
			maxZoom: 17,
			opacity: 0.8
		});

		// Based on OSM data
		skobbler = L.tileLayer('http://tiles1-b586b1453a9d82677351c34485e59108.skobblermaps.com/TileService/tiles/2.0/1111113120/10/{z}/{x}/{y}.png@2x', {
			attribution: '© Tiles: <a href="http://maps.skobbler.com/">skobbler</a>, Map data: <a href=http://openstreetmap.org>OpenStreetMap</a> contributors, CC-BY-SA',
		}),

		skobblerNight = L.tileLayer('http://tiles1-b586b1453a9d82677351c34485e59108.skobblermaps.com/TileService/tiles/2.0/1111113120/2/{z}/{x}/{y}.png@2x', {
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


	/* DRAWING CONTROLS */
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

	/* LEAFLET-ROUTING */
/*
	// Snapping Layer
    snapping = new L.geoJson(null, {
      style: {
        opacity:0
        ,clickable:false
      }
    }).addTo(map);
    map.on('moveend', function() {
      if (map.getZoom() > 12) {
        var proxy = 'http://www2.turistforeningen.no/routing.php?url=';
        var route = 'http://www.openstreetmap.org/api/0.6/map';
        var params = '&bbox=' + map.getBounds().toBBoxString() + '&1=2';
        $.get(proxy + route + params).always(function(osm, status) {
          if (status === 'success' && typeof osm === 'object') {
            var geojson = osmtogeojson(osm);

            snapping.clearLayers();
            for (var i = 0; i < geojson.features.length; i++) {
              var feat = geojson.features[i];
              if (feat.geometry.type === 'LineString' && feat.properties.tags.highway) {
                snapping.addData(geojson.features[i]);
              }
            }
          } else {
            console.log('Could not load snapping data');
          }
        });
      } else {
        snapping.clearLayers();
      }
    });
    map.fire('moveend');

    // OSM Router
    router = function(m1, m2, cb) {
      var proxy = 'http://www2.turistforeningen.no/routing.php?url=';
      var route = 'http://www.yournavigation.org/api/1.0/gosmore.php&format=geojson&v=foot&fast=1&layer=mapnik';
      var params = '&flat=' + m1.lat + '&flon=' + m1.lng + '&tlat=' + m2.lat + '&tlon=' + m2.lng;
      $.getJSON(proxy + route + params, function(geojson, status) {
        if (!geojson || !geojson.coordinates || geojson.coordinates.length === 0) {
          if (typeof console.log === 'function') {
            console.log('OSM router failed', geojson);
          }
          return cb(new Error());
        }
        return cb(null, L.GeoJSON.geometryToLayer(geojson));
      });
    }

    routing = new L.Routing({
      position: 'topleft'
      ,routing: {
        router: router
      }
      ,snapping: {
        layers: []
      }
      ,snapping: {
        layers: [snapping]
        ,sensitivity: 15
        ,vertexonly: false
      }
    });
    map.addControl(routing);
    routing.draw()
*/

}

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

	// Initialize global bikeLanes layer
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
}


function getPoint(latlng, date, type) {
	heatMap.addLatLng(latlng);

	var icon;
	if (type == "Collision") {
		icon = bikeRedIcon;
	} else {
		icon = bikeYellowIcon;
	}
	marker = L.marker(latlng, {
		icon: icon
	});

	date = date.split(",");
	date = date[0] + ',' + date[1]
	marker.bindPopup('<strong>Source:</strong> User submitted<br><strong>Date:</strong> ' + date + '<br><strong>Type:</strong> ' + type);

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
}


function toTitleCase(s){
    return s.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

// Purpose: Initializes the Pie chart cluster icons by getting the needed attributes from each cluster
//		and passing them to the pieChart function
function createPieCluster(cluster) {
	var children = cluster.getAllChildMarkers();

	//Count the number of markers in each cluster
	var	n = children.length,
		nPolice = 0,
		nIcbc = 0,
		nBikeR = 0,
		nBikeY = 0,
		nUnknown = 0,
		marker;
	
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

	// Build the svg layer
	return pieChart([{
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
	}], 
	
	outerR, 
	innerR,
	n
	);
};


// pieChart
// 	Purpose: Builds the svg DivIcons
// 	inputs: data as list of objects containing "type", "count", "color", outer chart radius, inner chart radius, and total points for cluster
// 	output: L.DivIcon donut chart where each "type" is mapped to the corresponding "color" with a proportional section corresponding to "count"
function pieChart(data, outerR, innerR, total){
	var types = [],
		counts = [],
		colors = [];

	data.forEach(function(d){
		types.push(d.type);
		counts.push(d.count);
		colors.push(d.color);
	});

	var color = d3.scale.ordinal()
		.domain(types)
		.range(colors)

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
		.style("fill", function(d) { return color(d.data.type); });

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

// Purpose: Helper function to convert xmlNode into a string
function serializeXmlNode(xmlNode) {
    if (typeof window.XMLSerializer != "undefined") {
        return (new window.XMLSerializer()).serializeToString(xmlNode);
    } else if (typeof xmlNode.xml != "undefined") {
        return xmlNode.xml;
    }
    return "";
}

