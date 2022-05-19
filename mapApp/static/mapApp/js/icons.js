// Icon definitions
var iconColors = {
    "collision": "#D73027",
    "nearmiss": "#F46D43",
    "hazard": "#FECE54",
    "theft": "#74ADD1",
    "official": "#436978",
    "undefined": "#a3a3a3",
    "geocode": "#313695",
    "location": "#313695",
    "newInfrastructure": "#4575B4"
};

// Given type, return the icon color as defined in iconColors
function getColor(t) {
  return iconColors[t];
};

L.ExtraMarkers.Icon.prototype.options.prefix = 'fa';
// Icon definitions
var icons = {
  "bikeRedIcon": L.ExtraMarkers.icon({
    // icon: "fa-bicycle",
    // innerHTML: '<img src="{% static \'mapApp/images/bike_crash.png\' %}">',
    innerHTML: '<img src="/media/mapApp/collision_teardrop_with_shadow.png" width=\'45px\' height=\'43px\' >',
      pieColor: getColor("collision"),
    // shape: 'circle',
    svg: "false"
  }),
  // "bikeYellowIcon": L.ExtraMarkers.icon({
  //   innerHTML: '<img src="/media/mapApp/bike_near_miss.png" width=\'19px\' height=\'15px\' style=\'margin-top:11px\'>',
  //   markerColor: "yellow",
  //   shape: 'circle',
  //   iconColor: 'black',
  //   pieColor: getColor("nearmiss"),
  //   svg: "false"
  // }),


  // custom collison / near miss icons
  // "bikeRedIcon": L.ExtraMarkers.icon({
  //   markerColor: "orange",
  //   shape: 'circle',
  //   innerHTML: "<img src=\'/media/mapApp/bike_crash.png\' width=\'22px\' height=\'12.6px\' style=\'margin-top:11px\'>",
  //   pieColor: getColor("collision"),
  // }),
  // "bikeYellowIcon": L.ExtraMarkers.icon({
  //   shape: 'circle',
  //   markerColor: 'yellow',
  //   innerHTML: "<img src=\'/media/mapApp/bike_near_miss.png\' width=\'17px\' height=\'13.4px\' style=\'margin-top:11px\'>",
  //   pieColor: getColor("nearmiss"),
  // }),
  // standard collision / near miss icons

  // "bikeRedIcon": L.ExtraMarkers.icon({
  //   icon: "fa-bicycle",
  //   iconColor: 'white',
  //   markerColor: getColor("collision"),
  //   pieColor: getColor("collision"),
  //   svg: "true"
  // }),
  "bikeYellowIcon": L.ExtraMarkers.icon({
    icon: "fa-bicycle",
    iconColor: 'black',
    markerColor: getColor("nearmiss"),
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
    iconColor: 'black',
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
    markerColor: '#313695',
    iconColor: '#cbcbcb',
    pieColor: getColor("geocode"),
    svg: "true"
  }),
  "locationIcon": L.ExtraMarkers.icon({
    icon: "fa-user",
    markerColor: '#313695',
    iconColor: '#cbcbcb',
    pieColor: getColor("location"),
    svg: "true"
  }),
    "newInfrastructureIcon": L.ExtraMarkers.icon({
    icon: "fa-star",
    markerColor: '#4575B4',
    iconColor: '#FEE090',
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
