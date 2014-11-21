// Global layer variables
var collisionsLayer, nearmissesLayer, hazardsLayer, theftsLayer;

// Create the a simple leaflet map centered around Victoria
function initializeCfaxMap(){
  // Map init and default layers
  map = L.map('map', {
      layers: [L.tileLayer('https://tiles1-b586b1453a9d82677351c34485e59108.skobblermaps.com/TileService/tiles/2.0/011011321101/10/{z}/{x}/{y}.png@2x', {
        minZoom: 2,
        attribution: '© Tiles: <a href="http://maps.skobbler.com/">skobbler</a>, Map data: <a href=http://openstreetmap.org>OpenStreetMap</a> contributors, CC-BY-SA'})
      ],
      worldCopyJump: true,
  }).fitBounds([
    [48.40185599006367, -123.34625244140624], //Top
    [48.69821216562637, -123.44650268554688], //Bottom
    [48.45653041501911, -123.26660156249999], //Right
    [48.47565256743914, -123.4588623046875] //Left
  ]);
};

// add data defined in data variable to data panel and to map as L.circleMarker
function addData(data){
  collisionsLayer = geojsonCircleMarker( data.collisions , "collision").addTo(map);
  nearmissesLayer = geojsonCircleMarker( data.nearmisses , "nearmiss").addTo(map);
  hazardsLayer = geojsonCircleMarker( data.hazards , "hazard").addTo(map);
  theftsLayer = geojsonCircleMarker( data.thefts , "theft").addTo(map);

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
          + "<strong>Date: </strong>" + moment(obj.properties.incident_date).calendar() + "<br>"
          + "<strong>Type: </strong>" + obj.properties.incident + " (" + obj.properties.incident_with + ")<br>";
          if(obj.properties.incident_detail != ''){
            str+= "<strong>Description: </strong>" + obj.properties.incident_detail + "</li>";
          }
      }
      else if(title === "Nearmisses") {
        str += "<li layer='nearmiss' pk=" + obj.properties.pk + ">"
          + "<strong>Date: </strong>" + moment(obj.properties.incident_date).calendar() + "<br>"
          + "<strong>Type: </strong>" + obj.properties.incident + " (" + obj.properties.incident_with + ")<br>";
          if(obj.properties.incident_detail != ''){
            str+= "<strong>Description: </strong>" + obj.properties.incident_detail + "</li>";
          }
      }
      else if(title === "Hazards"){
        str += "<li layer='hazard' pk=" + obj.properties.pk + ">"
          + "<strong>Date: </strong>" + moment(obj.properties.hazard_date).calendar() + "<br>"
          + "<strong>Type: </strong>" + obj.properties.hazard + "<br>";
          if(obj.properties.hazard_detail != ''){
            str += "<strong>Description: </strong>" + obj.properties.hazard_detail + "</li>";
          };
      }
      else if(title === "Thefts"){
        str += "<li layer='theft' pk=" + obj.properties.pk + ">"
          + "<strong>Date: </strong>" + moment(obj.properties.theft_date).calendar() + "<br>"
          + "<strong>Type: </strong>" + obj.properties.theft + "<br>";
        if(obj.properties.theft_detail != ''){
          str += "<strong>Description: </strong>" + obj.properties.theft_detail + "</li>";
        };
      }
      else{
        console.log("Unknown type error in pprint");
      }
    });
  }
  $('#data').append(str + "</ol>");
};



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
