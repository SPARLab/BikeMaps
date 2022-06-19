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

/* If coordinates have been passed in through the URL, go to that location
** If not, go to the last known location for a smooth transition between
** homepage and vis page
** Default view is global (zoom of 1)
*/
if (typeof zoom !== 'undefined') {
  map.setView(L.latLng(lat, lng), zoom);
} else if (localStorage.getItem('lastKnownLat') !== null) {
  let lastKnownLat = localStorage.getItem('lastKnownLat');
  let lastKnownLng = localStorage.getItem('lastKnownLng');
  let lastKnownZoom = localStorage.getItem('lastKnownZoom');
  map.setView(L.latLng(lastKnownLat, lastKnownLng), lastKnownZoom);
}

/** Add geocoder control */
var geocodeMarker;
var geocoder = L.Control.geocoder({
    defaultMarkGeocode: false,
    position: "topleft",
    placeholder: gettext('Search...'),
    errorMessage: gettext('Nothing found.')
}).on('markgeocode', function(result) {
  console.log(result.geocode);
  map.fitBounds(result.geocode.bbox);
  geocodeMarker && map.removeLayer(geocodeMarker); //remove old marker if it exists
  geocodeMarker = new L.Marker(result.geocode.center, {
      icon: icons["geocodeIcon"]
  }).bindPopup(result.geocode.name).addTo(map).openPopup();
}).addTo(map);
