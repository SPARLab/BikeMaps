// Define tile layers
var MapQuestOpen_OSM = L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg', {
      attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      subdomains: '1234'
    }),
    Mapnik_BW = L.tileLayer('http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png', {
      attribution: '<a href="https://openstreetmap.org/">&copy OpenStreetMap contributors, CC-BY-SA</a>',
      subdomains: '1234'
    }),
    stravaHM = L.tileLayer('https://d2z9m7k9h4f0yp.cloudfront.net/tiles/cycling/color5/{z}/{x}/{y}.png', {
      minZoom: 3,
      maxZoom: 17,
      opacity: 0.8,
      attribution: '<a href=http://labs.strava.com/heatmap/>http://labs.strava.com/heatmap/</a>'
    }),
    infrastructure = L.tileLayer.wms("https://sparii.geog.uvic.ca/WMS", {
      layers: 'bikemaps_infrastructure',
      format: 'image/png',
      transparent: true,
      version: '1.3.0'
    });
