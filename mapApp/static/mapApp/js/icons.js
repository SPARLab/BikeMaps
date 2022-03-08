// Icon definitions
var iconColors = {
    "collision": "#fe6100",
    "nearmiss": "#ffb000",
    "hazard": "#648fff",
    "theft": "#785ef0",
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
    markerColor: getColor("collision"),
    iconColor: 'black',
    pieColor: getColor("collision"),
    svg: "true"
  }),
  "bikeYellowIcon": L.ExtraMarkers.icon({
    icon: "fa-bicycle",
    markerColor: getColor("nearmiss"),
    iconColor: 'black',
    pieColor: getColor("nearmiss"),
    svg: "true"
  }),
  "bikeGreyIcon": L.ExtraMarkers.icon({
    icon: "fa-crosshairs",
    markerColor: 'lightblue',
    iconColor: 'black',
    pieColor: getColor("undefined"),
    svg: "true"
  }),
  "hazardIcon": L.ExtraMarkers.icon({
    icon: "fa-warning",
    markerColor: getColor("hazard"),
    iconColor: 'black',
    pieColor: getColor("hazard"),
    svg: "true"
  }),
  "theftIcon": L.ExtraMarkers.icon({
    icon: "fa-unlock",
    markerColor: getColor("theft"),
    iconColor: '#cbcbcb',
    pieColor: getColor("theft"),
    svg: "true"
  }),
  "officialIcon": L.ExtraMarkers.icon({
    icon: "fa-certificate",
    markerColor: 'cadetblue',
    iconColor: 'orange',
    pieColor: getColor("official"),
    svg: "true"
  }),
  "geocodeIcon": L.ExtraMarkers.icon({
    icon: "fa-flag",
    markerColor: 'darkred',
    iconColor: 'black',
    pieColor: getColor("geocode"),
    svg: "true"
  }),
  "locationIcon": L.ExtraMarkers.icon({
    icon: "fa-user",
    markerColor: 'darkred',
    iconColor: 'black',
    pieColor: getColor("location"),
    svg: "true"
  }),
    "newInfrastructureIcon": L.ExtraMarkers.icon({
    icon: "fa-star",
    markerColor: 'gray',
    iconColor: 'yellow',
    pieColor: getColor("newInfrastructure"),
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
