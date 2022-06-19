/* This is the entry point into the script that runs on the main page of BikeMaps. The inital location for the map is determined before any of the map tiles are rendered or incident data is retreived. Any code that requires the map to be initalized and location set runs in this block, while other variable and function definitions can be found in 'index-helpers.js'
 */

initializeMapLocation().then(() => {

  /** Initalize map */
  map = L.map('map', {
    center: mapCenter,
    minZoom: 2,
    zoom: mapZoom,
    zoomControl: false,
    layers: [OpenStreetMap, HOTOSM, CyclOSM, stravaHM],
    worldCopyJump: true,
  });

  /** The drawing functionality is stored in 'draw.html', which allows it to access Django template tags. This custom event fires to let draw.html know the map has been initialized and the drawing code can run. It runs document is ready to make sure listener in draw.html has been added.  */
  const mapInitializedEvent = new Event('mapInitializedEvent', {
    bubbles: true,
  });

  $(document).ready(function() {
    document.dispatchEvent(mapInitializedEvent);
  });

  /** Style map control tooltips once draw control has loaded */
  map.on('drawControlReady', function() {
    // All left side controls
    $('.leaflet-left .leaflet-control a').tooltip({
      placement: 'right',
      delay: 400
    });
  });

  /** Load the data for the initial map bounds and add layer to map */
  loadAllIncidentData(map.getBounds());
  incidentAppliedLayers.addTo(map);

  /** Define data fetch function for popup content when marker is clicked */
  incidentAppliedLayers.on('click', function(e) {
    var layer = e.layer;
    getXHRPopup(layer);
  });

  /** Add geocoder control to toolbar */
  var geocodeMarker;
  var geocoder = L.Control.geocoder({
    defaultMarkGeocode: false,
    position: "topleft",
    placeholder: gettext('Search...'),
    errorMessage: gettext('Nothing found.')
  }).on('markgeocode', function(result) {
    map.fitBounds(result.geocode.bbox);
    // remove old marker if it exists
    geocodeMarker && map.removeLayer(geocodeMarker);
    geocodeMarker = new L.Marker(result.geocode.center, {
      icon: icons["geocodeIcon"]
    }).bindPopup(result.geocode.name).addTo(map).openPopup();
  }).addTo(map);

  $('.leaflet-control-geocoder').tooltip({
    placement: 'right',
    delay: 400,
    title: function() {
      return gettext("Search for an address")
    }
  });

  /** Add user location control to toolbar */
  const lc = L.control.locate({
    strings: {
      title: "Go to my location"
    },
    locateOptions: {
      maxZoom: 16
    }
  }).addTo(map);

  /** Add zoom control to toolbar */
  const zoomControl = L.control.zoom({
    zoomInTitle: gettext('Zoom in'),
    zoomOutTitle: gettext('Zoom out'),
  });
  map.addControl(zoomControl);

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

  /** Actions to take when user has panned or jumped to a new location */
  map.on('moveend', function(e) {

    /** Map center and zoom level are updated in the URL. They are also saved to local storage, which can be used to set the initial map location if the user revisits the site */
    let center = map.getCenter();
    lastKnownZoom = map.getZoom();
    lastKnownLat = center.lat;
    lastKnownLng = center.lng;

    localStorage.setItem('lastKnownZoom', lastKnownZoom);
    localStorage.setItem('lastKnownLat', lastKnownLat);
    localStorage.setItem('lastKnownLng', lastKnownLng);
    window.history.replaceState({}, "", "@" + lastKnownLat.toFixed(7) + "," + lastKnownLng.toFixed(7) + "," + lastKnownZoom + "z");

    /** Load new data if new map bounds exceed the area we currently have data loaded for. Won't run if a data load is already running (!loadingDataFlag) and debounce delays execution in case user is panning around and firing many 'moveend' events */
    if (!loadingDataFlag && initialDataLoaded) {
      loadDataIfBoundsExceedDebounce();
    }
  });

  /** Add alert areas and geofences to map */
  alertAreas.addTo(map);
  addAlertAreas(geofences);
});

/** Check if the URL contains lat/long/zoom that can be used to initalize map location */
function trySettingLocationFromURL() {
  let locationNotSetInURL = (typeof lat === 'undefined' || typeof lng === 'undefined' || typeof zoom === 'undefined');
  // Set map center and map zoom if available in URL
  if (!locationNotSetInURL) {
    mapCenter = [lat, lng];
    mapZoom = zoom;
    return true;
  }
  return false;
}

/** This functions checks if the user has granted location permissions without requesting them. This aligns with Google's recommendation to only 'request geolocation information in response to a user gesture' rather than on page load, which can make users mistrustful or confused. */
async function checkLocationPermissions() {
  if (navigator.geolocation) {
    const result = await navigator.permissions.query({
      name: 'geolocation'
    });
    if (result.state === 'granted') {
      // Location permissions have already been granted
      return true;
    } else {
      // Permissions either denied or not requested yet
      return false;
    }
  }
  // Geolocation is not supported by this browser
  return false;
}

/** This function fetches users location */
function getUserLocation() {
  return new Promise(function(resolve, reject) {
    navigator.geolocation.getCurrentPosition(
      pos => {
        resolve(pos);
      },
      err => {
        reject(err);
      }, {
        timeout: 5000
      }
    );
  });
}

//* This function checks if we have the location that the user last visited in local storage, and uses it if available */
function trySettingLocationFromStorage() {
  let lastKnownLat = localStorage.getItem('lastKnownLat');
  let lastKnownLng = localStorage.getItem('lastKnownLng');
  let lastKnownZoom = localStorage.getItem('lastKnownZoom');

  let haveLastKnownLocation = (lastKnownLat && lastKnownLng && lastKnownZoom);

  if (haveLastKnownLocation) {
    mapCenter = [lastKnownLat, lastKnownLng];
    mapZoom = lastKnownZoom;
    window.history.replaceState({}, "", "@" + Number(lastKnownLat).toFixed(7) + "," + Number(lastKnownLng).toFixed(7) + "," + Number(lastKnownZoom) + "z");
  }
  // If every other map initalization option has failed, load the default location
  else setDefaultLocation();
}

/** This function sets the location to a zoomed-out view of North America */
function setDefaultLocation() {
  mapCenter = [48, -100];
  mapZoom = 4;
}

/** This function determines where the map location will be initialized to when the front page loads. The order of priority is:
1. The location and zoom level set in the url (eg bikemaps.org/@48.5,-123.5,13z)
2. The user's current location, IF location permissions have previously been granted
3. The last location visited by the user if available
4. A view of North America
*/
async function initializeMapLocation() {

  const locationInURL = trySettingLocationFromURL();

  if (!locationInURL) {
    try {
      const haveLocationPermission = await checkLocationPermissions();
      if (haveLocationPermission) {
        try {
          const position = await getUserLocation();

          if (position) {
            // Successfully retreived user's location, set map view
            mapCenter = [position.coords.latitude, position.coords.longitude];
            mapZoom = 16;
          } else {
            // Did not successfully retreive users location
            trySettingLocationFromStorage();
          }
        } catch (error) {
          // We have location permissions but there was an error getting the user's location
          trySettingLocationFromStorage();
        }
      } else {
        // We don't have location permissions
        trySettingLocationFromStorage();
      }
    } catch (error) {
      // There was an error when trying to get location permissions
      trySettingLocationFromStorage();
    }
  }
}
