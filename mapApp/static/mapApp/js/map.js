// Define tile layers
var MapQuestOpen_OSM = L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg', {
      attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      subdomains: '1234'
    }),
    OpenStreetMap = L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
      minZoom: 15,
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }),
    OpenStreetMapNoZoom = L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }),
    CyclOSM = L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
        minZoom: 15,
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }),
    // http://leaflet-extras.github.io/leaflet-providers/preview/
    HOTOSM = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        maxZoom: 14,
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }),
    Mapnik_BW = L.tileLayer('http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png', {
      attribution: '<a href="https://openstreetmap.org/">&copy OpenStreetMap contributors, CC-BY-SA</a>',
      subdomains: '1234'
    }),
    stravaHM = L.tileLayer('https://heatmap-external-{s}.strava.com/tiles/ride/gray/{z}/{x}/{y}.png', {
      minZoom: 3,
      maxZoom: 13,
      maxNativeZoom: 11,
      opacity: 0.8,
      attribution: '<a href=http://labs.strava.com/heatmap/>http://labs.strava.com/heatmap/</a>'
    });

var osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib = 'Map data � <a href="https://openstreetmap.org">OpenStreetMap</a>';
var osm = new L.TileLayer(osmUrl);
