// Global layer variables
var collisionsLayer, nearmissesLayer, hazardsLayer, theftsLayer;

// Initialize the leaflet map
  map = L.map('map', {
      layers: [L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg', {
        attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        subdomains: '1234'
      })],
      worldCopyJump: true,
  });

// Add data to the map
$(document).ready(function(){
  if(data.rois.features.length > 0){
    // Add data (call to recentReports.js)
    addData(data);
    // listen for data hover to highlight points and data (call to recentReports.js)
    listenForHover();
  } else {
    map.fitWorld();
    $('#data').append('<h2>Instructions:</h2><ol>'
                    + '<li>Login in to your account</li>'
                    + '<li>Trace an alert area on the home page map</li>'
                    + '<li>Visit this page to see recent incidents in your alert area</li>'
                    + '</ol>');
  }
});

// add data defined in data variable to data panel and to map as L.circleMarker
function addData(data){
  // Add geojson features to map
  collisionsLayer = geojsonCircleMarker( data.collisions , "collision").addTo(map);
  nearmissesLayer = geojsonCircleMarker( data.nearmisses , "nearmiss").addTo(map);
  hazardsLayer = geojsonCircleMarker( data.hazards , "hazard").addTo(map);
  theftsLayer = geojsonCircleMarker( data.thefts , "theft").addTo(map);
  rois = geojsonPolygonMarker(data.rois).addTo(map);

  // Fit map extent to alert areas boundary
  map.fitBounds(rois);

  // Add text to data column
  pprint("Collisions", data.collisions);
  pprint("Nearmisses", data.nearmisses);
  pprint("Hazards", data.hazards);
  pprint("Thefts", data.thefts);
}

// Highlight list item and highlight corresponding pnt on map
function highlightPoint(type, pk){
  getPointLayer(type).eachLayer(function(layer){
    if(layer.feature.id == pk){
      map.panTo(layer.getBounds().getCenter());
      layer.bringToFront();
      layer.setStyle({
          fillColor: '#0ff',
          fillOpacity: 1
      });
    }
  });
}

// Return a highlighted point to it's original color
function unhighlightPoint(type){
  getPointLayer(type).eachLayer(function(layer){
    layer.setStyle({
      fillColor: getColor(type),
      fillOpacity: 0.8
    });
  });
}

// Given a incident type, return the layer where points of that type are located
function getPointLayer(type){
  switch(type){
    case "collision": return collisionsLayer;
    case "nearmiss": return nearmissesLayer;
    case "hazard": return hazardsLayer;
    case "theft": return theftsLayer;
  }
}

// Print different point types in a nice formatted list TODO move to new js file
function pprint(title, jsonData){
  $('#data').append('<h2>'+ title +'</h2>');
  var str = "<ol>";
  if(jsonData.features.length === 0){
    str += "<em>No reports this week</em>";
  }
  else{
    jsonData.features.forEach(function(obj) {
      if(title === "Collisions"){
        str += "<li layer='collision' pk=" + obj.properties.pk + ">"
          + "<strong>Date: </strong>" + moment(obj.properties.date).calendar() + "<br>"
          + "<strong>Type: </strong>" + obj.properties.incident_type + " (" + obj.properties.incident_with + ")<br>";
          if(obj.properties.incident_detail != ''){
            str+= "<strong>Description: </strong>" + obj.properties.incident_detail + "</li>";
          }
      }
      else if(title === "Nearmisses") {
        str += "<li layer='nearmiss' pk=" + obj.properties.pk + ">"
          + "<strong>Date: </strong>" + moment(obj.properties.date).calendar() + "<br>"
          + "<strong>Type: </strong>" + obj.properties.incident_type + " (" + obj.properties.incident_with + ")<br>";
          if(obj.properties.details != ''){
            str+= "<strong>Description: </strong>" + obj.properties.details + "</li>";
          }
      }
      else if(title === "Hazards"){
        str += "<li layer='hazard' pk=" + obj.properties.pk + ">"
          + "<strong>Date: </strong>" + moment(obj.properties.date).calendar() + "<br>"
          + "<strong>Type: </strong>" + obj.properties.hazard_type + "<br>";
          if(obj.properties.details != ''){
            str += "<strong>Description: </strong>" + obj.properties.details + "</li>";
          };
      }
      else if(title === "Thefts"){
        str += "<li layer='theft' pk=" + obj.properties.pk + ">"
          + "<strong>Date: </strong>" + moment(obj.properties.date).calendar() + "<br>"
          + "<strong>Type: </strong>" + obj.properties.theft_type + "<br>";
        if(obj.properties.details != ''){
          str += "<strong>Description: </strong>" + obj.properties.details + "</li>";
        };
      }
      else{
        console.log("Unknown type error in pprint");
      }
    });
  }
  $('#data').append(str + "</ol>");
};

// Listen for and handle hovering over list item in data pane
function listenForHover(){
  // Toggle data and point highlighting
  $('#data li').hover(function(){
    // Highlight list item
    $(this).toggleClass('highlight');
    // highlight corresponding point (call to cfax.js)
    highlightPoint($(this).attr('layer'), $(this).attr('pk'));
  });
  $('#data li').mouseleave(function(){
    // unhighlight all points (call to cfax.js)
    unhighlightPoint($(this).attr('layer'));
  });
}
