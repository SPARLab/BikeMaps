/** Host location, port to construct API requests */
var hostname = window.location.hostname;

// If running locally, include port in API requests
if (window.location.port) {
  hostname = hostname + ':' + window.location.port;
}

/**
* Map set up
*/

/** Initialize the map */

// Check if map center and zoom are provided in url, otherwise default to view of north america
let mapCenter, mapZoom;
let locationNotSetInURL = (typeof lat === 'undefined' || typeof lng === 'undefined' || typeof zoom === 'undefined');
if (locationNotSetInURL){
  mapCenter = [48, -100];
  mapZoom = 4;
} else {
  mapCenter = [lat, lng];
  mapZoom = zoom;
}

//
let loadingDataFlag = 0;
let boundsOfLoadedData = L.latLngBounds(); // initalize with empty bounds

var map = L.map('map', {
    center: mapCenter,
    minZoom: 2,
    zoom: mapZoom,
    zoomControl: false,
    layers: [OpenStreetMap, CyclOSM, stravaHM],
    worldCopyJump: true,
});

// If lat/long/zoom have been passed into the URL, set view to that location
// Locate the user either way, but if view was already set don't change view to users location
console.log(`is location set in url? ${!locationNotSetInURL}`)
locateUser(setView = locationNotSetInURL, watch = false);

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

/** Add scalebar */
L.control.scale({
    position: 'bottomright'
}).addTo(map);

/* Turn off default mousewheel event (map zoom in / zoom out) when mouse is over the legend. This allows scrolling when contents overflow legend div */
var elem = L.DomUtil.get('legend');
L.DomEvent.on(elem, 'mousewheel', L.DomEvent.stopPropagation);

const loadDataIfBoundsExceedDebounce = debounce(function() {
    loadDataIfBoundsExceed(map.getBounds());
}, 1500);

map.on('moveend', function (e) {
    var zoom = map.getZoom(),
        center = map.getCenter();
        console.log('replacing window history');
    window.history.replaceState({}, "", "@" + center.lat.toFixed(7) + "," + center.lng.toFixed(7) + "," + zoom + "z");
    console.log('move end');
    // if true, load new data
    console.log('new data load needed?');
    if (!loadingDataFlag) {
      loadDataIfBoundsExceedDebounce();
    }
  });

map.on('zoomend', function(e) {
  if(map.getZoom() >= 13 && map.hasLayer(stravaHM)) {
    // stravaHM._clearBgBuffer();
  }
});

/** Locate user, set map view */

// Find the user via GPS or internet connection.
// Parameters to determine if the maps view should be set to that location and if the position should be polled and updated
// If successful, fires a 'locationfound' event
function locateUser(setView, watch) {
    this.map.locate({
        setView: setView,
        maxZoom: 16,
        watch: watch,
        enableHighAccuracy: true
    });
};

// If the users location is found, set map view to that location
map.on("locationfound", function (location) {
  console.log('location found code executing');
    var userMark = L.userMarker(location.latlng, { smallIcon: true, circleOpts: { weight: 1, opacity: 0.3, fillOpacity: 0.05 } }).addTo(map);
    if (location.accuracy < 501) {
        userMark.setAccuracy(location.accuracy);
    }
});

/**
* Data fetching
*/

/**
 * @type {Object[]} - Array of objects
 * @type {string} Object[].id - The type of incident (eg collision, hazard)
 * @type {layer} Object[].layer - leaflet layer generated from geojson data for one incident type
 */
 var incidentReferenceLayers = [];

/**
* incidentAppliedLayers is an instance of MarkerClusterGroup, a plugin type that extends FeatureGroup, which itself extends Layergroup. groups several layers and handles as one
* 'incidentReferenceLayers' stores the loaded layer data, while incidentAppliedLayers is one grouped layer that can be filtered, subsets added/removed to map with checkboxes
*/
var incidentAppliedLayers = new L.MarkerClusterGroup({
    maxClusterRadius: 70,
    polygonOptions: {
        color: '#2c3e50',
        weight: 3
    },
    animateAddingMarkers: true,
    iconCreateFunction: pieChart
});

incidentAppliedLayers.addTo(map);

// Create data feature groups
var collisions, nearmisses, hazards, thefts, newInfrastructures;

// Loads data for map view that was loaded when site first visited
// Sometimes site goes to default location and then switches to users location right away, causing an apparent double loading.
if (!loadingDataFlag) loadAllIncidentData(map.getBounds());

// Define popup getter function
incidentAppliedLayers.on('click', function (e) {
    var layer = e.layer;
    getXHRPopup(layer);
});

/**
* Alert areas
*/

var alertAreas = L.featureGroup();
alertAreas.addTo(map);

// Add geofence alert areas to map
addAlertAreas(geofences);
function addAlertAreas(geofences) {
    L.geoJson(geofences, {
        style: function (feature) {
            return {
                color: '#3b9972',
                weight: 2,
                opacity: 0.6,
                fillOpacity: 0.1,
                pk: (feature.id ? feature.id : feature.properties.id)
            }
        }
    }).eachLayer(function (l) { alertAreas.addLayer(l); });
}

/**
* Data filtering by date
*/

/** Initialize the slider */
$("input.slider").ready(function () {
    var mySlider = $("input.slider").slider({
        step: 1,
        max: (moment().weekYear() - 1970) * 12 + moment().month(), //months since epoch
        min: (moment().weekYear() - 1980) * 12 + moment().month(), //months since epoch minus 10 years

        range: true,
        tooltip: 'hide',
        enabled: false,
        handle: 'custom',

        formatter: function (val) {
            return sliderDate(val[0]).format("MMM-YYYY") + " : " + sliderDate(val[1]).format("MMM-YYYY");
        }
    });
});

// Convert months since epoch into a moment.js date object
function sliderDate(m) {
    return moment({
        year: 1970 + m / 12,
        month: m % 12
    });
};

// Handle slider filtering
var collisionsUnfiltered = collisions,
    nearmissesUnfiltered = nearmisses,
    hazardsUnfiltered = hazards,
    theftsUnfiltered = thefts;
    newInfrastructuresUnfiltered = newInfrastructures;
$("input.slider").on("slideStop", function (e) { filterPoints(e.value[0], e.value[1]) });

function getIncidentLayer(incLayerId, incLayers) {
    var tempLyr;
    for (var tlayer in incLayers) {
        if (incLayers[tlayer].id === incLayerId) {
            tempLyr = incLayers[tlayer].layer;
        }
    }
    return tempLyr
}

// function to filter points and redraw map
function filterPoints(start_date, end_date) {

    var d, p;
    start_date = sliderDate(start_date);
    end_date = sliderDate(end_date).add(1, 'M').subtract(1, 'd'); //Get the last day of the month

    incidentAppliedLayers.clearLayers();

    collisionsUnfiltered = getIncidentLayer("collision", incidentReferenceLayers);
    nearmissesUnfiltered = getIncidentLayer("nearmiss", incidentReferenceLayers);
    hazardsUnfiltered = getIncidentLayer("hazard", incidentReferenceLayers);
    theftsUnfiltered = getIncidentLayer("theft", incidentReferenceLayers);
    newInfrastructuresUnfiltered = getIncidentLayer("newInfrastructure", incidentReferenceLayers);

    collisions = collisionsUnfiltered.filter(function (feature, layer) {
        d = moment(feature.feature.properties.date);
        return d >= start_date && d <= end_date;
    });
    nearmisses = nearmissesUnfiltered.filter(function (feature, layer) {
        d = moment(feature.feature.properties.date);
        return d >= start_date && d <= end_date;
    });
    thefts = theftsUnfiltered.filter(function (feature, layer) {
        d = moment(feature.feature.properties.date);
        return d >= start_date && d <= end_date;
    });
    hazards = hazardsUnfiltered.filter(function (feature, layer) {
        d = moment(feature.feature.properties.date);
        return d >= start_date && d <= end_date;
    });
    newInfrastructures = newInfrastructuresUnfiltered.filter(function (feature, layer) {
        d = moment(feature.feature.properties.dateAdded);
        return d >= start_date && d <= end_date;
    });
    // Add filtered layer back if checkbox is checked
    $("#collisionCheckbox").is(":checked") && incidentAppliedLayers.addLayers(collisions);
    $("#nearmissCheckbox").is(":checked") && incidentAppliedLayers.addLayers(nearmisses);
    $("#hazardCheckbox").is(":checked") && incidentAppliedLayers.addLayers(hazards);
    $("#theftCheckbox").is(":checked") && incidentAppliedLayers.addLayers(thefts);
    $("#newInfrastructureCheckbox").is(":checked") && incidentAppliedLayers.addLayers(newInfrastructures);

};

// Add unfiltered data back
function resetPoints() {
    incidentAppliedLayers.clearLayers();
    collisions = collisionsUnfiltered,
        nearmisses = nearmissesUnfiltered,
        hazards = hazardsUnfiltered,
        thefts = theftsUnfiltered;
    newInfrastructures = newInfrastructuresUnfiltered;

    $("#collisionCheckbox").is(":checked") && incidentAppliedLayers.addLayers(collisions);
    $("#nearmissCheckbox").is(":checked") && incidentAppliedLayers.addLayers(nearmisses);
    $("#hazardCheckbox").is(":checked") && incidentAppliedLayers.addLayers(hazards);
    $("#theftCheckbox").is(":checked") && incidentAppliedLayers.addLayers(thefts);
    $("#newInfrastructureCheckbox").is(":checked") && incidentAppliedLayers.addLayers(newInfrastructures);
};

$("input.slider").on("slide", function (e) {
    $("div.filter .start-date").text(sliderDate(e.value[0]).format("MMM-YYYY"));
    $("div.filter .end-date").text(sliderDate(e.value[1]).format("MMM-YYYY"));
});


// Filter checkbox handler
$("#filterCheckbox").click(function () {
    if (this.checked) {
        var sliderVal = $('input.slider').slider('getValue')
        $("input.slider").slider("enable");
        $("div.filter .start-date").text(sliderDate(sliderVal[0]).format("MMM-YYYY"));
        $("div.filter .end-date").text(sliderDate(sliderVal[1]).format("MMM-YYYY"));
        // Add filtered points to map
        filterPoints(sliderVal[0], sliderVal[1])
    }
    else {
        $("input.slider").slider("disable");
        $("div.filter .start-date").text("");
        $("div.filter .end-date").text("");
        // Add all points back to map
        resetPoints();
    }
});


// pieChart
// Purpose: Builds svg cluster DivIcons
// inputs: clusters passed from Leaflet.markercluster
// output: L.DivIcon donut chart where the number of points in a cluster are represented by a proportional donut chart arc of the same color as the underlying marker
function pieChart(cluster) {
    var children = cluster.getAllChildMarkers();

    // Count the number of points of each kind in the cluster using underscore.js
    var data = _.chain(children)
        .countBy(function (i) { return i.options.icon.options.pieColor })
        .map(function (count, pieColor) { return { "color": pieColor, "count": count } })
        .sortBy(function (i) { return -i.count })
        .value();

    var total = children.length;

    outerR = (total >= 10 ? (total < 50 ? 20 : 25) : 15),
        innerR = (total >= 10 ? (total < 50 ? 10 : 13) : 7);

    var arc = d3.svg.arc()
        .outerRadius(outerR)
        .innerRadius(innerR);

    var pie = d3.layout.pie()
        .sort(null)
        .value(function (d) {
            return d.count;
        });

    // Define the svg layer
    var width = 50,
        height = 50;
    var svg = document.createElementNS(d3.ns.prefix.svg, 'svg');
    var vis = d3.select(svg)
        .data(data)
        .attr('class', 'marker-cluster-pie')
        .attr('width', width)
        .attr('height', height)
        .append("g")
        .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')');

    var g = vis.selectAll(".arc")
        .data(pie(data))
        .enter().append("g")
        .attr('class', 'arc');

    g.append('path')
        .attr("d", arc)
        .style("fill", function (d) {
            return d.data.color;
        });

    // Add center fill
    vis.append("circle")
        .attr("cx", 0)
        .attr("cy", 0)
        .attr("r", innerR)
        .attr('class', 'center')
        .attr("fill", "#f1f1f1");

    // Add count text
    vis.append('text')
        .attr('class', 'pieLabel')
        .attr('text-anchor', 'middle')
        .attr('dy', '.3em')
        .text(total)

    return new L.DivIcon({
        html: (new window.XMLSerializer()).serializeToString(svg),
        className: 'marker-cluster',
        iconSize: new L.Point(40, 40)
    });
};

// HELPER FUNCTIONS
function getPopup(layer) {
    var feature = layer.feature,
        type = layer.options.ftype,
        popup;

    if (type === "newInfrastructure") {
        popup = '<strong>' + gettext('New infrastructure') + ':</strong> ' + gettext(feature.properties.infra_type);
        popup += '<br><strong>' + gettext('Date changed') + ': </strong> ' + moment(feature.properties.dateAdded).locale(LANGUAGE_CODE).format('MMMM YYYY');
        popup += '<br><div class="popup-details"><strong>' + gettext('Details') + ':</strong> ' + feature.properties.details + '</div>';
    } else {
        if (type === "collision" || type === "nearmiss") {
            popup = '<strong>' + gettext('Type') + ':</strong> ' + gettext(feature.properties.i_type) + '<br><strong>';
            if (feature.properties.i_type != "Fall") popup += gettext('Incident with');
            else popup += gettext('Due to');
            popup += ':</strong> ' + gettext(feature.properties.incident_with)

        } else if (type === "hazard") {
            popup = '<strong>' + gettext('Hazard type') + ':</strong> ' + gettext(feature.properties.i_type);

        } else if (type === "theft") {
            popup = '<strong>' + gettext('Theft type') + ':</strong> ' + gettext(feature.properties.i_type);

        }
        else return "error"; //Return error if type not found

        // Append date
        popup += '<br><strong>'+gettext('Date')+': </strong> ' + moment(feature.properties.date).locale(LANGUAGE_CODE).format("lll")+'<br>';
        popup += '<strong>'+gettext('Incident ID')+':</strong> '+ feature.id;

        // Append details if present
        if (feature.properties.details) {
            popup += '<br><div class="popup-details"><strong>' + gettext('Details') + ':</strong> ' + feature.properties.details + '</div>';
        }
        return popup;
    }
    return popup;
};

// Purpose: Convert a given geojson dataset to a MakiMarker point layer
//  and add all latlngs to the heatmap and bind appropriate popups to markers
function geojsonMarker(data, type) {
    return L.geoJson(data, {
        pointToLayer: function (feature, latlng) {
            return L.marker(latlng, {
                icon: getIcon(type),
                ftype: type,
                objType: feature.properties.model
            })
        },
    });
};

/**
 * Refresh layers for all incident data types for the requested bounds
 * @param {L.bounds} boundsToLoad - leaflet type representing area of map to load data for
 */
function loadAllIncidentData(currentMapBounds){
  loadingDataFlag = 1;
  const incidentTypeStrings = ['collisions', 'nearmisses', 'hazards', 'thefts', 'newInfrastructures'];
  // Load data for area 50% greater than current bounds
  let boundsToLoad = currentMapBounds.pad(0.5);

  // clear all existing layers
  incidentAppliedLayers.clearLayers();

  const loadDataPromsies = incidentTypeStrings.map(i => {
    return asyncLoadIncidentData(i, boundsToLoad.toBBoxString()).then((data) => {
      processLayerFromData(data, getIncidentTypeFromURL(i));
      return `finished loading ${i}`;
    });
  })
  Promise.all(loadDataPromsies).then(r => {
    console.log('done loading all');
    loadingDataFlag = 0;
    boundsOfLoadedData = boundsToLoad;
    // Check if the map moved while the last data was being loaded
    loadDataIfBoundsExceedDebounce();
  }).catch(e => {
    loadingDataFlag = 0;
    console.log(e)
  })
}

/**
 * Load data for single incident type within requested bounds
 * @param {string} incidentType - type to load data for (eg collision, theft)
 * @param {string} bboxString - bounds converted to string format accepted by restApi.py
 */
async function asyncLoadIncidentData(incidentType, bboxString){
  let result;
  const requestURL = `/${incidentType}_tiny?bbox=${bboxString}&format=json`;

  try {
    result = await $.ajax({
            type: 'GET',
            url: requestURL,
            dataType: 'json'
          });
      return result;
  } catch(error) {
    console.log(error);
  }
};

/**
 * Actions to take after new incident data is loaded:
 * Convert retreived data to geojson feature collection/group, add layer to incidentAppliedLayers group as well as reference layers array, conditionally apply to map based on checkbox status
 * @param {Obj} data - data for single incident type retreived from db
 * @param {string} incidentType - incident type of data
 */
function processLayerFromData(data, incidentType){
  let incidentLayer =
    geojsonMarker(data, incidentType)
    .addTo(incidentAppliedLayers)
    .getLayers();

  $("#" + incidentType + "Checkbox").change(function () {
    this.checked ?
    incidentAppliedLayers.addLayers(incidentLayer) : incidentAppliedLayers.removeLayers(incidentLayer);
  });

  // for now, just remove old layer if already exists
  // TODO: merge old and new data together?
  let oldLayerIndex = incidentReferenceLayers.findIndex(l => l.incidentType === incidentType)
  if (oldLayerIndex > -1) incidentReferenceLayers.splice(oldLayerIndex, 1)

  incidentReferenceLayers.push({ id: incidentType, layer: incidentLayer });
}

// URLs use incident types in plural form, checkboxes use singular. Convert between for convenience
function getIncidentTypeFromURL(URLSubstring){
  if (URLSubstring === "nearmisses") return "nearmiss";
  else return URLSubstring.slice(0, -1);
}

/* TODO: add debounce to wait until user stops zooming/scrolling around to load new data */
function loadDataIfBoundsExceed(currentMapBounds){
  // if loaded data bounds are empty or current bounds exceed them, load new data
  if (!boundsOfLoadedData.isValid() || !boundsOfLoadedData.contains(currentMapBounds)){
    loadAllIncidentData(currentMapBounds);
  }
}

function debounce(func, wait, immediate) {
    var timeout;
    return function () {
        var context = this, args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
};

function loadPopupDetails(incidentPk, popup, incidentType, incidentURL) {
    console.log(incidentPk)
    $.ajax({
        url: incidentURL + incidentPk,
        dataType: 'json',
        success: function (response) {
            //console.log(response);
            popup.setContent(getPopupText(incidentType, response));
        },
        error: function (err) {
            popup.setContent('Could not get Xhr details');
        }
    });
}

function getXHRPopup(layer) {
    var feature = layer.feature,
        type = layer.options.ftype,
        popup;

    var popup = L.popup({ offset: new L.Point(0, -30) })
        .setLatLng(L.latLng(feature.geometry.coordinates[1], feature.geometry.coordinates[0]))
        .setContent("Loading data off server ...")
        .openOn(map);

    // PK is stored in under key 'pk' for data loaded from database, 'id' for points just created and added to incidentAppliedLayers from submitted form
    let pk = feature.properties.pk || feature.properties.id;

    if (type === "newInfrastructure") {
        //there is an extra s in the path
        loadPopupDetails(pk, popup, type, "//" + hostname + "/" + type + "s_xhr?format=json&pk=");
    }
    else {
        loadPopupDetails(pk, popup, type, "//" + hostname + "/" + type + "_xhr?format=json&pk=");
    }
};

function getPopupText(incidentType, in_data) {
    var tempContent = "";
    var tempPath = "";

    if (incidentType === "hazard") {
        tempContent = '<strong>' + gettext('Hazard type') + ':</strong> ' + gettext(in_data.properties.i_type);
        tempPath = "/mapApp/hazard/";
    }
    else if (incidentType === "theft") {
        tempContent = '<strong>' + gettext('Theft type') + ':</strong> ' + gettext(in_data.properties.i_type);
        tempPath = "/mapApp/theft/"
    }
    else if (incidentType === "collision" || incidentType === "nearmiss") {
        tempContent = '<strong>' + gettext('Type') + ':</strong> ' + gettext(in_data.properties.i_type) + '<br><strong>';
        if (in_data.properties.i_type != "Fall") tempContent += gettext('Incident with');
        else tempContent += gettext('Due to');
        tempContent += ':</strong> ' + gettext(in_data.properties.incident_with)
        tempPath = "/mapApp/incident/";
    }
    else if (incidentType === "newInfrastructure") {
        tempContent = '<strong>' + gettext('New infrastructure') + ':</strong> ' + gettext(in_data.properties.infra_type);
        tempContent += '<br><strong>' + gettext('Date changed') + ': </strong> ' + moment(in_data.properties.dateAdded).locale(LANGUAGE_CODE).format('MMMM YYYY');
        tempContent += '<br><div class="popup-details"><strong>' + gettext('Details') + ':</strong> ' + in_data.properties.details + '</div>';
        tempPath = "/mapApp/newinfrastructure/";
    }
    else {
        tempContent += "Type not found.";
    }
    tempContent += '<br><strong>' + gettext('Date') + ': </strong> ' + moment(in_data.properties.date).locale(LANGUAGE_CODE).format("lll");
    tempContent += '<br><strong>' + gettext('Incident ID') + ':</strong> ' + in_data.properties.pk;

    // Append details if present
    if (in_data.properties.details) {
        tempContent += '<br><div class="popup-details"><strong>' + gettext('Details') + ':</strong> ' + in_data.properties.details + '</div>';
    }

    //Append the data for editing if in role
    if (typeof checkEdit === "function") {
        tempContent += checkEdit(in_data, tempPath);
    }

    return tempContent;
}
