// Icon definitions
var iconColors = {
    "collision": "#d9534f",
    "nearmiss": "#f0ad4e",
    "hazard": "#3eab45",
    "theft": "#000000",
    "official": "#1D84A6",
    "undefined": "#999999",
    "geocode": "#CC2A01",
    "location": "#CC2A01"
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
