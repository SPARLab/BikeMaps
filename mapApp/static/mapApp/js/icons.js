// Icon definitions
var iconColors = {
    "collision": "#d63e2a",
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

// Icon definitions
L.AwesomeMarkers.Icon.prototype.options.prefix = 'fa';
var icons = {
  "bikeRedIcon": L.AwesomeMarkers.icon({
    icon: "fa-bicycle",
    markerColor: 'red',
    iconColor: 'black',
    color: getColor("collision")
  }),
  "bikeYellowIcon": L.AwesomeMarkers.icon({
    icon: "fa-bicycle",
    markerColor: 'orange',
    iconColor: 'black',
    color: getColor("nearmiss")
  }),
  "bikeGreyIcon": L.AwesomeMarkers.icon({
    icon: "fa-crosshairs",
    markerColor: 'lightblue',
    iconColor: 'black',
    color: getColor("undefined")
  }),
  "hazardIcon": L.AwesomeMarkers.icon({
    icon: "fa-warning",
    markerColor: 'green',
    iconColor: 'black',
    color: getColor("hazard")
  }),
  "theftIcon": L.AwesomeMarkers.icon({
    icon: "fa-bicycle",
    markerColor: 'gray',
    iconColor: '#cbcbcb',
    color: getColor("theft")
  }),
  "officialIcon": L.AwesomeMarkers.icon({
    icon: "fa-certificate",
    markerColor: 'cadetblue',
    iconColor: 'orange',
    color: getColor("official")
  }),
  "geocodeIcon": L.AwesomeMarkers.icon({
    icon: "fa-flag",
    markerColor: 'darkred',
    iconColor: 'black',
    color: getColor("geocode")
  }),
  "locationIcon": L.AwesomeMarkers.icon({
    icon: "fa-user",
    markerColor: 'darkred',
    iconColor: 'black',
    color: getColor("location")
  }),
    "newInfrastructureIcon": L.AwesomeMarkers.icon({
    icon: "fa-star",
    markerColor: 'gray',
    iconColor: 'yellow',
    color: getColor("newInfrastructure")
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
