// Leaflet heatmap
var heatLayer = new HeatmapOverlay({ "radius": 20, "maxOpacity": 0.3 });
var heat_data;
var map = L.map('map', {
  center: [15,6],
  zoom: 1,
  minZoom: 1,
  zoomControl: false,
  scrollWheelZoom: true,
  worldCopyJump: true,
  layers: [OpenStreetMap, heatLayer]
}).on('load', changeMap())
  .on('moveend', mapFilter);

  // Add i18n zoom control
  L.control.zoom({
    zoomInTitle: gettext('Zoom in'),
    zoomOutTitle: gettext('Zoom out'),
  }).addTo(map);

if (typeof zoom !== 'undefined') {
  map.setView(L.latLng(lat, lng), zoom);
}
