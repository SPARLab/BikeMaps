var fixedColor = "#18bc9c";
var notFixedColor = "#e74c3c";

// Global layer variables
var hazardsNotFixed = L.featureGroup([]);
var hazardsFixed = L.featureGroup([]);

// Preprocess dates for performance
hazards.features = hazards.features.map(function(obj){
  return {
    "coordinates": obj.geometry.coordinates.reverse(),
    "id": obj.id,
    "details": obj.properties.details,
    "hazard_fixed": obj.properties.hazard_fixed,
    "i_type": obj. properties.i_type,
    "report_date": moment(obj.properties.report_date)
  }
})

var ndx = crossfilter(hazards.features);
var all = ndx.groupAll();

var hazardFixedDimension = ndx.dimension(function(d){return d.hazard_fixed;});
var iTypeDimension = ndx.dimension(function(d){return d.i_type;});
var yearDimension = ndx.dimension(function(d){return (parseInt(d.report_date.year()) < moment().year()-3 ? "Older" : d.report_date.format("YYYY"));});
var geomDimension = ndx.dimension(function(d){ return {'lat': d.coordinates[0], 'lng': d.coordinates[1]} });
var tableDimension = ndx.dimension(function(d){ return d;});

var hazardFixedGroup = hazardFixedDimension.group().reduceCount();
var iTypeGroup = iTypeDimension.group().reduceCount();
var yearGroup = yearDimension.group(function(year){
  return (parseInt(year) < moment().year()-3 ? "Older" : year);
}).reduceCount();

var yearPie = dc.pieChart('#year-pie')
  .width(200)
  .height(200)
  .dimension(yearDimension)
  .group(yearGroup);

var statusPie = dc.pieChart('#status-pie')
  .width(200)
  .height(200)
  .dimension(hazardFixedDimension)
  .group(hazardFixedGroup)
  .label(function(d){ return (d.data.key ? "Fixed" : "Not Fixed"); })
  .title(function(d){ return d.data.value; })
  .colors([notFixedColor, fixedColor]);

var iTypeBar = dc.barChart('#i-type-bar')
  .width(400)
  .height(400)
  .margins({top: 10, right: 50, bottom: 90, left: 40})
  .dimension(iTypeDimension)
  .group(iTypeGroup)
  .x(d3.scale.ordinal().domain(iTypeGroup.all().map(function(obj){return obj.key})))
  .xUnits(dc.units.ordinal)
  .yAxisLabel("Count")
  .centerBar(true)
  .elasticY(true)
  .renderTitle(false)
  .colors(d3.scale.category20b())
  .colorAccessor(function(d, i){return i;});


$(function(){
  // Initialize the leaflet map
  var map = L.map('map', {
      center: [48, -100],
      zoom: 4,
      layers: [OpenStreetMap, hazardsNotFixed, hazardsFixed],
      worldCopyJump: true,
  }).on('load', changeMap)
    .on('moveend', mapFilter);

  function changeMap(){
    hazardsNotFixed.clearLayers();
    hazardsFixed.clearLayers();

    geomDimension.top(Infinity).forEach(function(feature){
      var layer = L.circleMarker(feature.coordinates)
        .bindPopup(renderPopup(feature)).on('popupopen', function(ev){
          $("input.check").change(function(e){
            checkFnx(e.target, ev.target);
          });
        });
      if (feature.hazard_fixed) {
        layer.setStyle({radius: 3, color: "black", weight: 2, fillColor: fixedColor, fillOpacity: 1, id:feature.id });
        hazardsFixed.addLayer(layer);
      }
      else {
        layer.setStyle({radius: 3, color: "black", weight: 2, fillColor: notFixedColor, fillOpacity: 1, id:feature.id });
        hazardsNotFixed.addLayer(layer);
      }
    });
  };

  function mapFilter(){
    var bounds = map.getBounds();
    geomDimension.filterFunction(function(d){
      return bounds.contains([d.lat, d.lng]);
    });
    changeMap();
    dc.redrawAll();
  }

  function renderPopup(feature) {
    var content = "<strong>ID:</strong> " + feature.id + "<br>" +
      "<strong>Type:</strong> " + feature.i_type + "<br>" +
      "<strong>Reported:</strong> " + feature.report_date.format("DD/MM/YYYY");
    if (feature.details) content += "<br><strong>Details:</strong> " + feature.details;
    content += "<br><strong>Fixed:</strong> <input class='check' type='checkbox' " + (feature.hazard_fixed ? 'checked':'') + ">";

    return content;
  }
  geofences = geojsonPolygonMarker(geofences);
  geofences.setStyle({color: "blue"});
  geofences.addTo(map);
  map.fitBounds(geofences);

  for (var i = 0; i < dc.chartRegistry.list().length; i++) {
    var chartI = dc.chartRegistry.list()[i];
    chartI.on("filtered", changeMap);
  }

  function checkFnx(checkbox, layer){
    var checked = $(checkbox).is(':checked');
    var pID = layer.options.id;

    // Change the crossfilter dataset
    for(var i = 0; i < hazards.features.length; i++){
      if(hazards.features[i].id === pID){
        hazards.features[i].hazard_fixed = checked;
      }
    }
    ndx.remove();
    ndx.add(hazards.features);
    dc.redrawAll();
    changeMap();

    // AJAX change to server
    var fd = new FormData();
    fd.append('pk', pID);
    fd.append('fixed', checked);

    // Ajax changes to server
    $.ajax({
      url: "/update_hazard/",
      type: 'POST',
      data: fd,
      dataType: "json",
      processData: false,
      contentType: false,
      success: function(data) {
        if (!data['success']) {
          $('#message').append('<div class="alert alert-danger" role="alert">' +
            '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
            'There was a database failure saving the point.<br>' +
            'Please contact tech-support@bikemaps.org' +
            '</div>'
          );
          setTimeout(function(){
            $('#message .alert').alert('close');
          }, 7000);
        }
      }
    });
  }
});

dc.renderAll();
dc.redrawAll();
