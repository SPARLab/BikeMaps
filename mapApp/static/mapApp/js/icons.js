// Icon definitions
var iconColors = {
    "collision": "#d63e2a",
    "nearmiss": "#f3952f",
    "hazard": "#72b026",
    "theft": "#a3a3a3",
    "official": "#436978",
    "undefined": "#999999",
    "geocode": "#a23336",
    "location": "#a23336"
};

// Given type, return the icon color as defined in iconColors
function getColor(t) {
  return iconColors[t];
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
