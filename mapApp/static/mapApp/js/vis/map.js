// Leaflet heatmap
var heatLayer = new HeatmapOverlay({ "radius": 40, "maxOpacity": 0.3 });
var heat_data;
var Esri_Streets_Basemap_Vis = L.esri.basemapLayer("Streets");
var map = L.map('map', {
  center: [15,6],
  zoom: 1,
  minZoom: 1,
  zoomControl: false,
  scrollWheelZoom: true,
  worldCopyJump: true,
  layers: [Esri_Streets_Basemap_Vis, heatLayer]
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
