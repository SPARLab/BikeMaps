// Icon definitions
var iconColors = {
    "collision": "pink",
    "nearmiss": "#f3952f",
    "hazard": "#72b026",
    "theft": "#575757",
    "official": "#436978",
    "undefined": "#a3a3a3",
    "geocode": "#a23336",
    "location": "#a23336",
    "newInfrastructure": "#ffff00"
};

// Given type, return the icon color as defined in iconColors
function getColor(t) {
  return iconColors[t];
};

L.ExtraMarkers.Icon.prototype.options.prefix = 'fa';
// Icon definitions
var icons = {
  "bikeRedIcon": L.ExtraMarkers.icon({
    icon: "fa-bicycle",
    markerColor: '#785EF0',
    iconColor: 'black',
    color: "#785EF0",
    svg: "true"
  }),
  "bikeYellowIcon": L.ExtraMarkers.icon({
    icon: "fa-bicycle",
    markerColor: 'orange',
    iconColor: 'black',
    color: getColor("nearmiss"),
    svg: "true"
  }),
  "bikeGreyIcon": L.ExtraMarkers.icon({
    icon: "fa-crosshairs",
    markerColor: 'lightblue',
    iconColor: 'black',
    color: getColor("undefined"),
    svg: "true"
  }),
  "hazardIcon": L.ExtraMarkers.icon({
    icon: "fa-warning",
    markerColor: 'green',
    iconColor: 'black',
    color: getColor("hazard"),
    svg: "true"
  }),
  "theftIcon": L.ExtraMarkers.icon({
    icon: "fa-bicycle",
    markerColor: 'gray',
    iconColor: '#cbcbcb',
    color: getColor("theft"),
    svg: "true"
  }),
  "officialIcon": L.ExtraMarkers.icon({
    icon: "fa-certificate",
    markerColor: 'cadetblue',
    iconColor: 'orange',
    color: getColor("official"),
    svg: "true"
  }),
  "geocodeIcon": L.ExtraMarkers.icon({
    icon: "fa-flag",
    markerColor: 'darkred',
    iconColor: 'black',
    color: getColor("geocode"),
    svg: "true"
  }),
  "locationIcon": L.ExtraMarkers.icon({
    icon: "fa-user",
    markerColor: 'darkred',
    iconColor: 'black',
    color: getColor("location"),
    svg: "true"
  }),
    "newInfrastructureIcon": L.ExtraMarkers.icon({
    icon: "fa-star",
    markerColor: 'gray',
    iconColor: 'yellow',
    color: getColor("newInfrastructure"),
    svg: "true"
  })
};

// Purpose: Convert a given geojson dataset to a CircleMarker point layer
function geojsonCircleMarker(data, type) {
  return L.geoJson(data, {
    pointToLayer: function(feature, latlng) {
      return L.circleMarker(latlng, {
        radius: 3,
        fillColor: getColor(type),
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
      })
    }
  });
};

// Purpose: Convert a given geojson polygon dataset to a polygon layer
function geojsonPolygonMarker(data) {
  return L.geoJson(data, {
    style: {
      color: '#3b9972',
      weight: 2,
      opacity: 0.6,
      fillOpacity: 0.1,
    }
  });
};

// Get the appropriate icon from dataset name
function getIcon(t) {
  if (t === "collision")
    return icons["bikeRedIcon"];
  else if (t === "nearmiss")
    return icons["bikeYellowIcon"];
  else if (t === "hazard")
    return icons["hazardIcon"];
  else if (t === "theft")
    return icons["theftIcon"];
  else if (t === "official")
    return icons["officialIcon"];
  else if (t === "newInfrastructure")
    return icons["newInfrastructureIcon"];
  else return;
};
