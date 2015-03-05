// Create data feature groups
var incidentData = new L.MarkerClusterGroup({
      maxClusterRadius: 70,
      polygonOptions: {
        color: '#2c3e50',
        weight: 3
      },
      iconCreateFunction: function(cluster){
        var data = serializeClusterData(cluster);
        return pieChart(data);
      },
    }),
    heatMap = L.heatLayer([], {
      radius: 40,
      blur: 20,
    }),
    alertAreas = new L.FeatureGroup([]);

// Define popup getter function
incidentData.on('click', function(e){
  var layer = e.layer;
  layer.bindPopup(getPopup(layer)).openPopup();
});

// Initialize the map
var map = L.map('map', {
  center: [48, -100],
  zoom: 4,
  layers: [MapQuestOpen_OSM, stravaHM, incidentData, alertAreas],
  worldCopyJump: true,
});

// Set map view
var userMark;
map.on("locationfound", function(location) {
  if (!userMark) {
    userMark = L.userMarker(location.latlng, {smallIcon:true, circleOpts:{weight: 1, opacity: 0.3, fillOpacity: 0.05}}).addTo(map);
    userMark.setAccuracy(location.accuracy);
  }
});

if (typeof zoom !== 'undefined') {
  map.setView(L.latLng(lat, lng), zoom);
  locateUser(setView = false, watch = false);
} else {
  locateUser(setView = true, watch = false);
}

// Add geocoder control
var geocoder = L.Control.geocoder({
  position: "topleft"
}).addTo(map);
var geocodeMarker;
geocoder.markGeocode = function(result) {
  map.fitBounds(result.bbox);
  geocodeMarker && map.removeLayer(geocodeMarker); //remove old marker if it exists

  geocodeMarker = new L.Marker(result.center, {
    icon: icons["geocodeIcon"]
  })
  .bindPopup(result.name)
  .addTo(map)
  .openPopup();
};

// Add scalebar
L.control.scale({
  position: 'bottomright'
}).addTo(map);

// Add all points to map
var collisions = geojsonMarker(collisions, "collision").addTo(incidentData).getLayers(),
    nearmisses = geojsonMarker(nearmisses, "nearmiss").addTo(incidentData).getLayers(),
    hazards = geojsonMarker(hazards, "hazard").addTo(incidentData).getLayers(),
    thefts = geojsonMarker(thefts, "theft").addTo(incidentData).getLayers(),
    officials = geojsonMarker(officials, "official").addTo(incidentData).getLayers();

// Add geofence alert areas to map
var geofences = L.geoJson(geofences, {
  style: function(feature) {
    return {
      color: '#3b9972',
      weight: 2,
      opacity: 0.6,
      fillOpacity: 0.1,
      pk: feature.id,
      /*Mark the polygon with it's database id*/
      objType: 'polygon'
    }
  }
}).eachLayer(function(l){alertAreas.addLayer(l);});

// Add and remove layers individually from the clusters on checkbox change
$("#collisionCheckbox").change(function(){ this.checked ? incidentData.addLayers(collisions) : incidentData.removeLayers(collisions); });
$("#nearmissCheckbox").change(function(){ this.checked ? incidentData.addLayers(nearmisses) : incidentData.removeLayers(nearmisses); });
$("#hazardCheckbox").change(function(){ this.checked ? incidentData.addLayers(hazards) : incidentData.removeLayers(hazards); });
$("#theftCheckbox").change(function(){ this.checked ? incidentData.addLayers(thefts) : incidentData.removeLayers(thefts); });
$("#officialCheckbox").change(function(){ this.checked ? incidentData.addLayers(officials) : incidentData.removeLayers(officials); });


// Initialize the slider
$("input.slider").ready(function(){
  var mySlider = $("input.slider").slider({
    step: 1,
    max: (moment().weekYear() - 1970) * 12 + moment().month(), //months since epoch
    min: (moment().weekYear() - 1980) * 12  + moment().month(), //months since epoch minus 10 years

    range: true,
    tooltip: 'hide',
    enabled: false,
    handle: 'custom',

    formatter: function(val){
      return sliderDate(val[0]).format("MMM-YYYY") + " : " + sliderDate(val[1]).format("MMM-YYYY");
    }
  });
});

// Convert months since epoch into a moment.js date object
function sliderDate(m){
  return moment({
    year: 1970 + m/12,
    month: m%12
  });
};

// Handle slider filtering
var collisionsUnfiltered = collisions,
    nearmissesUnfiltered = nearmisses,
    hazardsUnfiltered = hazards,
    theftsUnfiltered = thefts,
    officialUnfiltered = officials;
$("input.slider").on("slideStop", function(e){ filterPoints(e.value[0], e.value[1]) });

// function to filter points and redraw map
function filterPoints(start_date, end_date) {
  var d, p;
  start_date = sliderDate(start_date);
  end_date = sliderDate(end_date).add(1,'M').subtract(1,'d'); //Get the last day of the month

  incidentData.clearLayers();

  collisions = collisionsUnfiltered.filter(function(feature, layer){
    d = moment(feature.feature.properties.date);
    return d >= start_date && d <= end_date;
  });
  nearmisses = nearmissesUnfiltered.filter(function(feature, layer){
    d = moment(feature.feature.properties.date);
    return d >= start_date && d <= end_date;
  });
  thefts = theftsUnfiltered.filter(function(feature, layer){
    d = moment(feature.feature.properties.date);
    return d >= start_date && d <= end_date;
  });
  hazards = hazardsUnfiltered.filter(function(feature, layer){
    d = moment(feature.feature.properties.date);
    return d >= start_date && d <= end_date;
  });
  officials = officialUnfiltered.filter(function(feature, layer){
    d = moment(feature.feature.properties.date);
    return d >= start_date && d <= end_date;
  });

  // Add filtered layer back if checkbox is checked
  $("#collisionCheckbox").is(":checked") && incidentData.addLayers(collisions);
  $("#nearmissCheckbox").is(":checked") && incidentData.addLayers(nearmisses);
  $("#hazardCheckbox").is(":checked") && incidentData.addLayers(hazards);
  $("#theftCheckbox").is(":checked") && incidentData.addLayers(thefts);
  $("#officialCheckbox").is(":checked") && incidentData.addLayers(officials);
};

// Add unfiltered data back
function resetPoints(){
  incidentData.clearLayers();
  collisions = collisionsUnfiltered,
  nearmisses = nearmissesUnfiltered,
  hazards = hazardsUnfiltered,
  thefts = theftsUnfiltered,
  officials = officialUnfiltered;
  $("#collisionCheckbox").is(":checked") && incidentData.addLayers(collisions);
  $("#nearmissCheckbox").is(":checked") && incidentData.addLayers(nearmisses);
  $("#hazardCheckbox").is(":checked") && incidentData.addLayers(hazards);
  $("#theftCheckbox").is(":checked") && incidentData.addLayers(thefts);
  $("#officialCheckbox").is(":checked") && incidentData.addLayers(officials);
};

$("input.slider").on("slide", function(e) {
  $("div.filter .start-date").text(sliderDate(e.value[0]).format("MMM-YYYY"));
  $("div.filter .end-date").text(sliderDate(e.value[1]).format("MMM-YYYY"));
});


// Filter checkbox handler
$("#filterCheckbox").click(function() {
  if(this.checked) {
    var sliderVal = $('input.slider').slider('getValue')
    $("input.slider").slider("enable");
    $("div.filter .start-date").text(sliderDate(sliderVal[0]).format("MMM-YYYY"));
    $("div.filter .end-date").text(sliderDate(sliderVal[1]).format("MMM-YYYY"));
    // Add filtered points to map
    filterPoints(sliderVal[0], sliderVal[1])
  }
  else {
    $("input.slider").slider("disable");
    $("div.filter .start-date").text("");
    $("div.filter .end-date").text("");
    // Add all points back to map
    resetPoints();
  }
});

// Purpose: Find the user via GPS or internet connection.
//      Parameters to determine if the maps view should be set to that location and if the position should be polled and updated
function locateUser(setView, watch) {
  this.map.locate({
    setView: setView,
    maxZoom: 16,
    watch: watch,
    enableHighAccuracy: true
  });
};

// Purpose: Initializes the Pie chart cluster icons by getting the needed attributes from each cluster
//		and passing them to the pieChart function
function serializeClusterData(cluster) {
  var children = cluster.getAllChildMarkers(),
  n = 0,
  colorRef = {};

  for (var icon in icons) {
    // Add a counting field to the icons objects
    icons[icon]["count"] = 0;
    // construct colorRef object for efficiency of bin sort
    colorRef[icons[icon].options.color] = icon;
  };

  //Count the number of markers in each cluster
  children.forEach(function(child) {
    // Match childColor to icon in icons
    var icon = colorRef[child.options.icon.options.color];
    icons[icon].count++;
    n++;
  });

  // Make array of icons data
  var data = $.map(icons, function(v) {
    return v;
  });
  // Push total points in cluster
  data.push(n);

  return data;
};

// pieChart
// 	Purpose: Builds the svg DivIcons
// 	inputs: data as list of objects containing "type", "count", "color", outer chart radius, inner chart radius, and total points for cluster
// 	output: L.DivIcon donut chart where each "type" is mapped to the corresponding "color" with a proportional section corresponding to "count"
function pieChart(data) {
  // Pop total points in cluster
  var total = data.pop();

  outerR = (total >= 10 ? (total < 50 ? 20 : 25) : 15),
  innerR = (total >= 10 ? (total < 50 ? 10 : 13) : 7);

  var arc = d3.svg.arc()
  .outerRadius(outerR)
  .innerRadius(innerR);

  var pie = d3.layout.pie()
  .sort(null)
  .value(function(d) {
    return d.count;
  });

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
  .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')');

  var g = vis.selectAll(".arc")
  .data(pie(data))
  .enter().append("g")
  .attr('class', 'arc');

  g.append('path')
  .attr("d", arc)
  .style("fill", function(d) {
    return d.data.options.color;
  });

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
  .attr('dy', '.3em')
  .text(total)

  var html = serializeXmlNode(svg);

  return new L.DivIcon({
    html: html,
    className: 'marker-cluster',
    iconSize: new L.Point(40, 40)
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

// HELPER FUNCTIONS
function getPopup(layer) {
  var feature = layer.feature,
  type = layer.options.ftype,
  popup;

  if (type === "collision" || type === "nearmiss") {
    popup = '<strong>Type:</strong> ' + feature.properties.i_type + '<br><strong>';
    if (feature.properties.i_type != "Fall") popup += 'Incident with';
    else popup += 'Due to';
    popup += ':</strong> ' + feature.properties.incident_with + '<br><strong>Date:</strong> ' + moment(feature.properties.date).format("MMM. D, YYYY, h:mma");

    if(feature.properties.details){
      popup += '<br><div class="popup-details"><strong>Details:</strong> ' + feature.properties.details + '</div>';
    }

  } else if (type === "hazard") {
    popup = '<strong>Hazard type:</strong> ' + feature.properties.i_type + '<br><strong>Date:</strong> ' + moment(feature.properties.date).format("MMM. D, YYYY, h:mma");
    if(feature.properties.details){
      popup += '<br><div class="popup-details"><strong>Details:</strong> ' + feature.properties.details + '</div>';
    }

  } else if (type === "theft") {
    popup = '<strong>Theft type:</strong> ' + feature.properties.i_type + '<br><strong>Date:</strong> ' + moment(feature.properties.date).format("MMM. D, YYYY, h:mma");
    if(feature.properties.details){
      popup += '<br><div class="popup-details"><strong>Details:</strong> ' + feature.properties.details + '</div>';
    }

  } else if (type === "official") {
    popup = "<strong>Type:</strong> " + feature.properties.official_type;
    if(feature.properties.details){
      popup += " (" + feature.properties.details + ")";
    }
    if(feature.properties.time){
      var date = moment(feature.properties.date + "T" + feature.properties.time).format("MMM. D, YYYY, h:mma");
    }else{
      var date = moment(feature.properties.date).format("MMM. D, YYYY");
    }
    popup += '<br><strong>Date:</strong> ' + date;
    popup += '<br><strong>Data source: </strong> ' + feature.properties.data_source + '<a href="#" data-toggle="collapse" data-target="#official-metadata"><small> (metadata)</small></a><br>' + '<div id="official-metadata" class="metadata collapse">' + '<strong>Metadata: </strong><small>' + feature.properties.metadata + '</small></div>';

  } else return "error";

  return popup;
};

// Purpose: Convert a given geojson dataset to a MakiMarker point layer
//  and add all latlngs to the heatmap and bind appropriate popups to markers
function geojsonMarker(data, type) {
  return L.geoJson(data, {
    pointToLayer: function(feature, latlng) {
      heatMap.addLatLng(latlng);
      return L.marker(latlng, {
        icon: getIcon(type),
        ftype: type,
        objType: feature.properties.model
      })
    },
  });
};
