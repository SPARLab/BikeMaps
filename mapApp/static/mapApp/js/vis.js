// map p_types of points to nice labels
var labels = {
  "collision": "Collisions",
  "nearmiss": "Nearmisses",
  "hazard": "Hazards",
  "theft": "Thefts",
}
// Define scales
// map p_type to appropriate colors
var colorScale = d3.scale.ordinal()
  .domain(["collision", "nearmiss", "hazard", "theft"])
  .range([iconColors.collision, iconColors.nearmiss, iconColors.hazard, iconColors.theft]);
var weekdayScale = d3.scale.quantize()
    .domain([0,1,2,3,4,5,6])
    .range(moment.weekdaysShort());

// Define crossfilter dataset
var xf = crossfilter(data);

// Define dimensions
var p_typeDimension = xf.dimension(function(d) {return d.properties.p_type;}),
    weekdayDimension = xf.dimension(function(d) {return (moment(d.properties.date).weekday()+6)%7 }),
    dateDimension = xf.dimension(function(d){ return moment(d.properties.date).diff(moment(), "days"); }),
    i_typeDimension = xf.dimension(function(d){ return d.properties.i_type });

// Define groups
// Reusable reduce function for counting different types of reports
function reduceAddTypeCount() {
  return function(p,v){
    var p_type = v.properties.p_type;
    if(p_type === "collision") p.collision++;
    else if(p_type === "nearmiss") p.nearmiss++;
    else if(p_type === "hazard") p.hazard++;
    else if(p_type === "theft") p.theft++;
    return p;
  };
};
function reduceRemoveTypeCount() {
  return function(p,v){
    var p_type = v.properties.p_type;
    if(p_type === "collision") p.collision--;
    else if(p_type === "nearmiss") p.nearmiss--;
    else if(p_type === "hazard") p.hazard--;
    else if(p_type === "theft") p.theft--;
    return p;
  };
};
function reduceInitTypeCount() {
  return function(){
    return {
      collision: 0,
      nearmiss: 0,
      hazard: 0,
      theft: 0
    };
  };
}
var countTypes = p_typeDimension.group().reduceCount(),
    weekdayCount = weekdayDimension.group().reduce(reduceAddTypeCount(), reduceRemoveTypeCount(), reduceInitTypeCount()),
    countPerDay = dateDimension.group().reduceCount(),
    aveDelayGroup = i_typeDimension.group().reduce(
      function(p,v) {
        ++p.count
        p.sum += moment(v.properties.report_date).diff(moment(v.properties.date), "days");
        p.avg = (p.count !== 0 ? p.sum/p.count : 0);
        p.p_type = v.properties.p_type;
        return p;
      },
      function(p,v) {
        --p.count
        p.sum -= moment(v.properties.report_date).diff(moment(v.properties.date), "days");
        p.avg = (p.count !== 0 ? p.sum/p.count : 0);
        return p;
      },
      function(){
        return {count:0, sum:0, avg:0, p_type:""};
      }
    );

// Bar chart for counts by type
var barTypes = dc.barChart('#barTypes');
barTypes
  .width(400)
  .height(200)
  .x(d3.scale.ordinal().domain(["collision", "nearmiss", "hazard", "theft"]))
  .xUnits(dc.units.ordinal)
  .yAxisLabel("Count")
  .centerBar(true)
  .elasticY(true)
  .dimension(p_typeDimension)
  .group(countTypes)
  .colors(colorScale.range())
  .colorAccessor(function(d){return colorScale.domain().indexOf(d.data.key);})
  .on('filtered', changeMap);
barTypes.xAxis()
  .tickFormat(function(v){ return labels[v]; });
barTypes.render();

// Bar chart for reports this week
var barWeek = dc.barChart("#barWeek");
barWeek
  .width(400)
  .height(200)
  .x(d3.scale.linear().domain([-0.5,6.5]))
  .yAxisLabel("Count")
  .centerBar(true)
  .elasticY(true)
  .dimension(weekdayDimension)
  .group(weekdayCount, "Collisions").valueAccessor(function(d){return d.value.collision; })
  .stack(weekdayCount, "Nearmisses", function(d){ return d.value.nearmiss; })
  .stack(weekdayCount, "Hazards", function(d){ return d.value.hazard; })
  .stack(weekdayCount, "Thefts", function(d){ return d.value.theft; })
  .brushOn(true)
  .colors(colorScale.range())
  .colorAccessor(function(d){return d.layer;})
  .on('filtered', changeMap);
barWeek.yAxis()
  .tickFormat(d3.format("d"));
barWeek.xAxis()
  .tickValues([0,1,2,3,4,5,6])
  .tickFormat(function(v){ return weekdayScale((v+1)%7); });
barWeek.render();

// bar chart of total reports per day
var barDate = dc.barChart("#barDate");
barDate
  .width(800)
  .height(175)
  .x(d3.scale.linear().domain([-360, 0]))
  .yAxisLabel("Count")
  .centerBar(true)
  .elasticY(true)
  .dimension(dateDimension)
  .group(countPerDay)
  .brushOn(true)
  .on('filtered', changeMap);
barDate.yAxis()
  .tickFormat(d3.format("d"));
barDate.xAxis()
  .tickFormat(function(v){ return moment().add(v, "days").format("MMM. D"); })
  .tickValues(function(){
    var firsts = [];
    // Calculate the day difference between now and the first of every month
    for(var i = 0; i<12; i++) firsts.push(moment().subtract(moment().date()-1, "days").subtract(i, "months").diff(moment(), "days"));
    return firsts;
  });
barDate.render();

// row chart of delay in reporting
var delayRows = dc.rowChart("#delayRows");
delayRows
  .width(500)
  .height(400)
  .dimension(i_typeDimension).keyAccessor(function(d){ return d.key; })
  .group(aveDelayGroup).valueAccessor(function(d){ return d.value.avg; })
  .ordering(function(d){ return -d.value.avg })
  .elasticX(true)
  .renderLabel(false)
  .colors(colorScale.range())
  .colorAccessor(function(d){ return colorScale.domain().indexOf(d.value.p_type); })
  .on('filtered', changeMap);
delayRows.render();

// Leaflet heatmap
var heatLayer = new HeatmapOverlay({ "radius": 40, "maxOpacity": 0.3 });
var heat_data;
var map = L.map('map', {
  center: [15,6],
  zoom: 1,
  minZoom: 1,
  scrollWheelZoom: true,
  worldCopyJump: true,
  layers: [Mapnik_BW, heatLayer]
}).on('load', changeMap());

function changeMap(){
  heat_data = { data: [] };
  p_typeDimension.top(Infinity).forEach(function(feature){
    heat_data.data.push({
      'lat': feature.geometry.coordinates[1],
      'lng': feature.geometry.coordinates[0],
      'value': 1
    });
  });
  heatLayer.setData(heat_data);
};


dc.renderAll();
dc.redrawAll();
