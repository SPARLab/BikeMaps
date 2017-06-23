// Create data feature groups
var incidentData = new L.MarkerClusterGroup({
      maxClusterRadius: 70,
      polygonOptions: {
        color: '#2c3e50',
        weight: 3
      },
      animateAddingMarkers: true,
      iconCreateFunction: pieChart
    }),
    alertAreas = L.featureGroup();

// Define popup getter function
incidentData.on('click', function(e){
  var layer = e.layer;
  layer.bindPopup(getPopup(layer)).openPopup();
});

// Initialize the map
var map = L.map('map', {
  center: [48, -100],
  minZoom: 2,
  zoom: 4,
  zoomControl: false,
  layers: [Esri_Streets_Basemap, stravaHM, incidentData, alertAreas],
  worldCopyJump: true,
});

// Add i18n zoom control
L.control.zoom({
  zoomInTitle: gettext('Zoom in'),
  zoomOutTitle: gettext('Zoom out'),
}).addTo(map);

// Set map view
map.on("locationfound", function(location) {
    var userMark = L.userMarker(location.latlng, {smallIcon:true, circleOpts:{weight: 1, opacity: 0.3, fillOpacity: 0.05}}).addTo(map);
    if (location.accuracy < 500){
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
  position: "topleft",
  placeholder: gettext('Search...'),
  errorMessage: gettext('Nothing found.')
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
    thefts = geojsonMarker(thefts, "theft").addTo(incidentData).getLayers();
    officials = geojsonMarker(officials, "official").addTo(incidentData).getLayers();

// Add geofence alert areas to map
addAlertAreas(geofences);
function addAlertAreas(geofences){
  L.geoJson(geofences, {
    style: function(feature) {
      return {
        color: '#3b9972',
        weight: 2,
        opacity: 0.6,
        fillOpacity: 0.1,
        pk: (feature.id ? feature.id : feature.properties.id)
      }
    }
  }).eachLayer(function(l){alertAreas.addLayer(l);});
}

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
    theftsUnfiltered = thefts;
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
  thefts = theftsUnfiltered;
  // officials = officialUnfiltered;
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

// pieChart
// 	Purpose: Builds svg cluster DivIcons
// 	inputs: clusters passed from Leaflet.markercluster
// 	output: L.DivIcon donut chart where the number of points in a cluster are represented by a proportional donut chart arc of the same color as the underlying marker
function pieChart(cluster) {
  var children = cluster.getAllChildMarkers();

  // Count the number of points of each kind in the cluster using underscore.js
  var data = _.chain(children)
    .countBy(function(i){ return i.options.icon.options.color })
    .map(function(count, color){ return {"color": color, "count": count} })
    .sortBy(function(i){ return -i.count })
    .value();

  var total = children.length;

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
    return d.data.color;
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

  return new L.DivIcon({
    html: (new window.XMLSerializer()).serializeToString(svg),
    className: 'marker-cluster',
    iconSize: new L.Point(40, 40)
  });
};

// HELPER FUNCTIONS
function getPopup(layer) {
  var feature = layer.feature,
  type = layer.options.ftype,
  popup;

  if (type === "official") {
    popup = '<strong>'+gettext('Type')+':</strong> ' + feature.properties.official_type;
   // popup = "<strong>Type:</strong> " + feature.properties.official_type;
    //if(feature.properties.details){
    //  popup += " (" + feature.properties.details + ")";
    //}
    if(feature.properties.time){
      var date = moment(feature.properties.date + "T" + feature.properties.time);//.format("MMM. D, YYYY, h:mma");
    }else{
      var date = moment(feature.properties.date).format("MMM. D, YYYY");
    }
    popup += '<br><strong>'+ gettext('Date')+': </strong> ' + moment(date).locale(LANGUAGE_CODE).format("lll");
   // popup += '<br><strong>' + gettext('Date') + ':</strong> ' + date;

    // Append details if present
    if(feature.properties.details){
      popup += '<br><div class="popup-details"><strong>'+ gettext('Details')+':</strong> ' + feature.properties.details + '</div>';
    }
    // popup += '<br><strong>Data source: </strong> ' + feature.properties.data_source + '<a href="#" data-toggle="collapse" data-target="#official-metadata"><small> (metadata)</small></a><br>' + '<div id="official-metadata" class="metadata collapse">' + '<strong>Metadata: </strong><small>' + feature.properties.metadata + '</small></div>';
  }
  else{
    if (type === "collision" || type === "nearmiss") {
      popup = '<strong>'+gettext('Type')+':</strong> ' + gettext(feature.properties.i_type) + '<br><strong>';
      if (feature.properties.i_type != "Fall") popup += gettext('Incident with');
      else popup += gettext('Due to');
      popup += ':</strong> ' + gettext(feature.properties.incident_with)

    } else if (type === "hazard") {
      popup = '<strong>'+gettext('Hazard type')+':</strong> ' + gettext(feature.properties.i_type);

    } else if (type === "theft") {
      popup = '<strong>'+gettext('Theft type')+':</strong> ' + gettext(feature.properties.i_type);
    }
    else return "error"; //Return error if type not found

    // Append date
    popup += '<br><strong>'+gettext('Date')+': </strong> ' + moment(feature.properties.date).locale(LANGUAGE_CODE).format("lll");

    // Append details if present
    if(feature.properties.details){
      popup += '<br><div class="popup-details"><strong>'+ gettext('Details')+':</strong> ' + feature.properties.details + '</div>';
    }

    return popup;
  }


  return popup;
};

// Purpose: Convert a given geojson dataset to a MakiMarker point layer
//  and add all latlngs to the heatmap and bind appropriate popups to markers
function geojsonMarker(data, type) {
  return L.geoJson(data, {
    pointToLayer: function(feature, latlng) {
      return L.marker(latlng, {
        icon: getIcon(type),
        ftype: type,
        objType: feature.properties.model
      })
    },
  });
};

map.on('moveend', function(e){
  var zoom = map.getZoom(),
      center = map.getCenter();
  window.history.replaceState({}, "", "@" + center.lat.toFixed(7) + "," + center.lng.toFixed(7) + "," + zoom + "z");
});

map.on('zoomend', function(e) {
  if(map.getZoom() >= 18 && map.hasLayer(stravaHM)) {
    stravaHM._clearBgBuffer();
  }
});
