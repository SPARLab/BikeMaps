// Create data feature groups
var collisions, nearmisses, hazards, thefts, newInfrastructures;

//'159.203.2.12' for dev
var srv = window.location.hostname;

// If running locally, include port in API requests
if (window.location.port) {
  srv = srv + ':' + window.location.port;
}

loadIncidenLayerXHR("/nearmisses_tiny?format=json", "nearmiss", nearmisses);
loadIncidenLayerXHR("/hazards_tiny?format=json", "hazard", hazards);
loadIncidenLayerXHR("/thefts_tiny?format=json", "theft", thefts);
loadIncidenLayerXHR("/collisions_tiny?format=json", "collision", collisions);
loadIncidenLayerXHR("/newInfrastructures_tiny?format=json", "newInfrastructure", newInfrastructures);

var xhrLayersLoaded = 0;
var refLayers = [];

var incidentData = new L.MarkerClusterGroup({
    maxClusterRadius: 70,
    polygonOptions: {
        color: '#2c3e50',
        weight: 3
    },
    animateAddingMarkers: true,
    iconCreateFunction: pieChart
}),
    alertAreas = L.featureGroup();

// Define popup getter function
incidentData.on('click', function (e) {
    var layer = e.layer;
    //layer.bindPopup(getPopup(layer)).openPopup();
    getXHRPopup(layer);
});



// Initialize the map
var map = L.map('map', {
    center: [48, -100],
    minZoom: 2,
    zoom: 4,
    zoomControl: false,
    layers: [OpenStreetMap, CyclOSM, stravaHM, incidentData, alertAreas],
    worldCopyJump: true,
});

// If the users location is found, set map view to that location
map.on("locationfound", function (location) {
    var userMark = L.userMarker(location.latlng, { smallIcon: true, circleOpts: { weight: 1, opacity: 0.3, fillOpacity: 0.05 } }).addTo(map);
    if (location.accuracy < 501) {
        userMark.setAccuracy(location.accuracy);
    }
});

if (typeof zoom !== 'undefined') {
    map.setView(L.latLng(lat, lng), zoom);
    locateUser(setView = false, watch = false);
} else {
    locateUser(setView = true, watch = false);
}

// Add geocoder control
var geocoder = L.Control.geocoder({
    position: "topleft",
    placeholder: gettext('Search...'),
    errorMessage: gettext('Nothing found.')
}).addTo(map);
var geocodeMarker;
geocoder.markGeocode = function (result) {
    map.fitBounds(result.bbox);
    geocodeMarker && map.removeLayer(geocodeMarker); //remove old marker if it exists

    geocodeMarker = new L.Marker(result.center, {
        icon: icons["geocodeIcon"]
    }).bindPopup(result.name).addTo(map).openPopup();
};

// Add scalebar
L.control.scale({
    position: 'bottomright'
}).addTo(map);

/* Turn off default mousewheel event (map zoom in / zoom out) when mouse is over the legend. This allows scrolling when contents overflow legend div */
var elem = L.DomUtil.get('legend');
L.DomEvent.on(elem, 'mousewheel', L.DomEvent.stopPropagation);

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

// Initialize the slider
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

function getRefLyr(in_lyr_id, in_refLayers) {
    var tempLyr;
    for (var tlyr in in_refLayers) {
        if (in_refLayers[tlyr].id === in_lyr_id) {
            tempLyr = in_refLayers[tlyr].lyr;
        }
    }
    return tempLyr
}
// function to filter points and redraw map
function filterPoints(start_date, end_date) {

    var d, p;
    start_date = sliderDate(start_date);
    end_date = sliderDate(end_date).add(1, 'M').subtract(1, 'd'); //Get the last day of the month

    incidentData.clearLayers();

    collisionsUnfiltered = getRefLyr("collision", refLayers);
    nearmissesUnfiltered = getRefLyr("nearmiss", refLayers);
    hazardsUnfiltered = getRefLyr("hazard", refLayers);
    theftsUnfiltered = getRefLyr("theft", refLayers);
    newInfrastructuresUnfiltered = getRefLyr("newInfrastructure", refLayers);

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
    $("#collisionCheckbox").is(":checked") && incidentData.addLayers(collisions);
    $("#nearmissCheckbox").is(":checked") && incidentData.addLayers(nearmisses);
    $("#hazardCheckbox").is(":checked") && incidentData.addLayers(hazards);
    $("#theftCheckbox").is(":checked") && incidentData.addLayers(thefts);
    $("#newInfrastructureCheckbox").is(":checked") && incidentData.addLayers(newInfrastructures);

};

// Add unfiltered data back
function resetPoints() {
    incidentData.clearLayers();
    collisions = collisionsUnfiltered,
        nearmisses = nearmissesUnfiltered,
        hazards = hazardsUnfiltered,
        thefts = theftsUnfiltered;
    newInfrastructures = newInfrastructuresUnfiltered;

    $("#collisionCheckbox").is(":checked") && incidentData.addLayers(collisions);
    $("#nearmissCheckbox").is(":checked") && incidentData.addLayers(nearmisses);
    $("#hazardCheckbox").is(":checked") && incidentData.addLayers(hazards);
    $("#theftCheckbox").is(":checked") && incidentData.addLayers(thefts);
    $("#newInfrastructureCheckbox").is(":checked") && incidentData.addLayers(newInfrastructures);
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

// Purpose: Find the user via GPS or internet connection.
//      Parameters to determine if the maps view should be set to that location and if the position should be polled and updated
function locateUser(setView, watch) {
    this.map.locate({
        setView: setView,
        maxZoom: 16,
        watch: watch,
        enableHighAccuracy: true
    });
};

// pieChart
// Purpose: Builds svg cluster DivIcons
// inputs: clusters passed from Leaflet.markercluster
// output: L.DivIcon donut chart where the number of points in a cluster are represented by a proportional donut chart arc of the same color as the underlying marker
function pieChart(cluster) {
    var children = cluster.getAllChildMarkers();

    // Count the number of points of each kind in the cluster using underscore.js
    var data = _.chain(children)
        .countBy(function (i) { return i.options.icon.options.color })
        .map(function (count, color) { return { "color": color, "count": count } })
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

map.on('moveend', function (e) {
    var zoom = map.getZoom(),
        center = map.getCenter();
    window.history.replaceState({}, "", "@" + center.lat.toFixed(7) + "," + center.lng.toFixed(7) + "," + zoom + "z");
});

map.on('zoomend', function(e) {
  if(map.getZoom() >= 13 && map.hasLayer(stravaHM)) {
    // stravaHM._clearBgBuffer();
  }
});


function loadIncidenLayerXHR(in_relink, in_lyr_type, in_ref_lyr) {
    //https://bikemaps.org/hazards?format=json
    //hazard
    $.ajax({
        url: in_relink,
        dataType: 'json',
        success: function (response) {
            //console.log('trying to add the xhr layer');
            in_ref_lyr = geojsonMarker(response, in_lyr_type).addTo(incidentData).getLayers();
            $("#" + in_lyr_type + "Checkbox").change(function () { this.checked ? incidentData.addLayers(in_ref_lyr) : incidentData.removeLayers(in_ref_lyr); });
            refLayers.push({ id: in_lyr_type, lyr: in_ref_lyr });
        },
        error: function (err) {
            console.log(err);
        }
    });

}



function loadInfoDetails(in_pk, ref_popup, in_type, in_url) {
    console.log(in_pk)
    $.ajax({
        url: in_url + in_pk,
        dataType: 'json',
        success: function (response) {
            //console.log(response);
            ref_popup.setContent(getPopupText(in_type, response));
        },
        error: function (err) {
            ref_popup.setContent('Could not get Xhr details');
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

    if (type === "newInfrastructure") {
        //there is an extra s in the path
        loadInfoDetails(feature.properties.pk, popup, type, "//" + srv + "/" + type + "s_xhr?format=json&pk=");
    }
    else {
        loadInfoDetails(feature.properties.pk, popup, type, "//" + srv + "/" + type + "_xhr?format=json&pk=");
    }

};

function getPopupText(in_type, in_data) {
    var tempContent = "";
    var tempPath = "";

    if (in_type === "hazard") {
        tempContent = '<strong>' + gettext('Hazard type') + ':</strong> ' + gettext(in_data.properties.i_type);
        tempPath = "/mapApp/hazard/";
    }
    else if (in_type === "theft") {
        tempContent = '<strong>' + gettext('Theft type') + ':</strong> ' + gettext(in_data.properties.i_type);
        tempPath = "/mapApp/theft/"
    }
    else if (in_type === "collision" || in_type === "nearmiss") {
        tempContent = '<strong>' + gettext('Type') + ':</strong> ' + gettext(in_data.properties.i_type) + '<br><strong>';
        if (in_data.properties.i_type != "Fall") tempContent += gettext('Incident with');
        else tempContent += gettext('Due to');
        tempContent += ':</strong> ' + gettext(in_data.properties.incident_with)
        tempPath = "/mapApp/incident/";
    }
    else if (in_type === "newInfrastructure") {
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
