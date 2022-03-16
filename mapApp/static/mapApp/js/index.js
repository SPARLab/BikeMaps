initializeMapOnPageLoad();

function initializeMapOnPageLoad() {

  if ('geolocation' in navigator) {
    console.log('geolocation in navigator');
  } else {
    console.log('geolocation is not in navigator');
  }

  if (!navigator.geolocation) {
    console.log('this browser doesnt support geolocation')
  }

  navigator.permissions.query({
    name: 'geolocation'
  }).then(function(result) {
    console.log(result);
    if (result.state === 'granted') {
      console.log('location permissions granted')
    } else if (result.state === 'prompt') {
      console.log('location permissions is prompt')
    } else if (result.state === 'denied') {
      console.log('location permissions is denied')
    }
    // Don't do anything if the permission was denied.
  });

  /**
   * Map set up
   */

  /** Initialize the map location */

  // lat, lng, zoom are retreived from URL and will be undefined if not set. Last known lat, long, zoom are from local storage and will be null if not set.



  let locationNotSetInURL = (typeof lat === 'undefined' || typeof lng === 'undefined' || typeof zoom === 'undefined');

  let haveCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.permissions.query({
        name: 'geolocation'
      }).then(function(result) {
        if (result.state === 'granted') {
          console.log('location permissions granted');
          navigator.geolocation.getCurrentPosition(success, error);
        } else return false;
      });
    }
    return false;
  }

  let lastKnownLat = localStorage.getItem('lastKnownLat');
  let lastKnownLng = localStorage.getItem('lastKnownLng');
  let lastKnownZoom = localStorage.getItem('lastKnownZoom');

  let haveLastKnownLocation = (lastKnownLat && lastKnownLng && lastKnownZoom);

  // 1. If location is in URL, go there
  if (!locationNotSetInURL) {
    mapCenter = [lat, lng];
    mapZoom = zoom;
  }
  // 2. If we already have location permissions, go to current location
  // else if ()
  // 3. If last known lat, long, zoom are available, go there
  else if (haveLastKnownLocation) {
    mapCenter = [lastKnownLat, lastKnownLng];
    mapZoom = lastKnownZoom;
    window.history.replaceState({}, "", "@" + Number(lastKnownLat).toFixed(7) + "," + Number(lastKnownLng).toFixed(7) + "," + Number(lastKnownZoom) + "z");
  }
  // 4. If no location info, default to North America
  else {
    mapCenter = [48, -100];
    mapZoom = 4;
  }

  // Initalize data loading vars
  let loadingDataFlag = 0;

  map = L.map('map', {
    center: mapCenter,
    minZoom: 2,
    zoom: mapZoom,
    zoomControl: false,
    layers: [OpenStreetMap, CyclOSM, stravaHM],
    worldCopyJump: true,
  });

  /** Add geocoder control */
  var geocodeMarker;
  var geocoder = L.Control.geocoder({
    defaultMarkGeocode: false,
    position: "topleft",
    placeholder: gettext('Search...'),
    errorMessage: gettext('Nothing found.')
  }).on('markgeocode', function(result) {
    map.fitBounds(result.geocode.bbox);
    geocodeMarker && map.removeLayer(geocodeMarker); //remove old marker if it exists
    geocodeMarker = new L.Marker(result.geocode.center, {
      icon: icons["geocodeIcon"]
    }).bindPopup(result.geocode.name).addTo(map).openPopup();
  }).addTo(map);

  // If lat/long/zoom have been passed into the URL, set view to that location
  // Locate the user either way, but if view was already set don't change view to users location

  /** TEMPORARILY TURN OFF GEOLOCATION WHILE WORKING ON LOCAL STORAGE **/
  // locateUser(setView = locationNotSetInURL, watch = false);
  const lc = L.control.locate({
    strings: {
      title: "Go to my location"
    },
    locateOptions: {
      maxZoom: 16
    }
  }).addTo(map);

  /** Add scalebar */
  L.control.scale({
    position: 'bottomright'
  }).addTo(map);

  /* Turn off default mousewheel event (map zoom in / zoom out) when mouse is over the legend. This allows scrolling when contents overflow legend div */
  var elem = L.DomUtil.get('legend');
  L.DomEvent.on(elem, 'mousewheel', L.DomEvent.stopPropagation);
  // Disallow panning when mouse is on about legend or using the date filter
  L.DomEvent.on(elem, 'mouseover', () => map.dragging.disable());
  L.DomEvent.on(elem, 'mouseleave', () => map.dragging.enable());


  map.on('moveend', function(e) {
    let center = map.getCenter();
    lastKnownZoom = map.getZoom();
    lastKnownLat = center.lat;
    lastKnownLng = center.lng;

    localStorage.setItem('lastKnownZoom', lastKnownZoom);
    localStorage.setItem('lastKnownLat', lastKnownLat);
    localStorage.setItem('lastKnownLng', lastKnownLng);
    window.history.replaceState({}, "", "@" + lastKnownLat.toFixed(7) + "," + lastKnownLng.toFixed(7) + "," + lastKnownZoom + "z");
    if (!loadingDataFlag) {
      loadDataIfBoundsExceedDebounce();
    }
  });

  // /** Locate user, set map's view */
  //
  // // Find the user via GPS or internet connection.
  // // Parameters to determine if the maps view should be set to that location and if the position should be polled and updated
  // // If successful, fires a 'locationfound' event
  // function locateUser(setView, watch) {
  //     this.map.locate({
  //         setView: setView,
  //         maxZoom: 16,
  //         watch: watch,
  //         enableHighAccuracy: true
  //     });
  // };
  //
  // // If the users location is found, set map view to that location
  // map.on("locationfound", function (location) {
  //
  // });

  incidentAppliedLayers.addTo(map);


  // Loads data for map view that was loaded when site first visited
  // Sometimes site goes to default location and then receives 'locationfound' event and switches to users location right away, causing an apparent double loading. Don't want to wait for location found to load data so don't think this is a bug, but maybe a better way of doing it?
  // if (!loadingDataFlag) loadAllIncidentData(map.getBounds());

  // Define popup getter function
  incidentAppliedLayers.on('click', function(e) {
    var layer = e.layer;
    getXHRPopup(layer);
  });

  /**
   * Alert areas
   */

  alertAreas.addTo(map);
  // Add geofence alert areas to map
  addAlertAreas(geofences);

}
