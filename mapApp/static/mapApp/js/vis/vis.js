dc.dataCount('.dc-data-count')
  .dimension(xf)
  .group(all);

// Bar chart for counts by type
var barTypes = dc.barChart('#barTypes');
barTypes
  .width(400)
  .height(200)
  .x(d3.scale.ordinal().domain(["collision", "nearmiss", "hazard", "theft"]))
  .xUnits(dc.units.ordinal)
  .yAxisLabel(gettext("Count"))
  .centerBar(true)
  .elasticY(true)
  .title(function(d){ return d.value; })
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
  .yAxisLabel(gettext("Count"))
  .centerBar(true)
  .elasticY(true)
  .dimension(weekdayDimension)
  .group(weekdayCount, gettext("Collisions")).valueAccessor(function(d){return d.value.collision; })
  .stack(weekdayCount, gettext("Nearmisses"), function(d){ return d.value.nearmiss; })
  .stack(weekdayCount, gettext("Hazards"), function(d){ return d.value.hazard; })
  .stack(weekdayCount, gettext("Thefts"), function(d){ return d.value.theft; })
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

// Bar chart for reports by hour of day
var barHour = dc.barChart("#barHour");
barHour
  .width(400)
  .height(200)
  .x(d3.scale.linear().domain([0,24]))
  .yAxisLabel(gettext("Count"))
  // .centerBar(true)
  .elasticY(true)
  .dimension(hourDimension)
  .group(countPerHour, "Collisions").valueAccessor(function(d){return d.value.collision; })
  .stack(countPerHour, "Nearmisses", function(d){ return d.value.nearmiss; })
  .stack(countPerHour, "Hazards", function(d){ return d.value.hazard; })
  .stack(countPerHour, "Thefts", function(d){ return d.value.theft; })
  .brushOn(true)
  .colors(colorScale.range())
  .colorAccessor(function(d){return d.layer;})
  .on('filtered', changeMap);
barHour.yAxis()
  .tickFormat(d3.format("d"));
// barHour.xAxis()
//   .tickValues([0,1,2,3,4,5,6])
//   .tickFormat(function(v){ return weekdayScale((v+1)%7); });
barHour.render();

// bar chart of total reports per day
var barDate = dc.barChart("#barDate");
barDate
  .width(575)
  .height(200)
  .x(d3.scale.linear().domain([-360, 0]))
  .yAxisLabel(gettext("Count"))
  .centerBar(true)
  .elasticY(true)
  .dimension(dateDimension)
  .group(countPerDay)
  .brushOn(true)
  .on('filtered', changeMap);
barDate.yAxis()
  .tickFormat(d3.format("d"));
barDate.xAxis()
  .tickFormat(function(v){ return moment().add(v, "days").format("ll").slice(0, -5); })
  .tickValues(function(){
    var firsts = [];
    // Calculate the day difference between now and the first of every month
    for(var i = 0; i<12; i++) firsts.push(moment().subtract(moment().date()-1, "days").subtract(i, "months").diff(moment(), "days"));
    return firsts;
  });
barDate.render();

// Fit map extent to alert areas boundary
if (alertAreas.getLayers().length > 0) {
  map.fitBounds(alertAreas.getBounds());
}

dc.renderAll();
dc.redrawAll();
