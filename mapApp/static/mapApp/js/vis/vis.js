dc.dataCount('.dc-data-count')
  .crossfilter(xf)
  .groupAll(all);

// Bar chart for counts by type
var barTypes = new dc.BarChart('#barTypes');
barTypes
  .width(null) // setting height & width to null tells them to fit to the size of the parent div
  .height(null)
  .margins({top: 10, right: 50, bottom: 30, left: 40})
  .x(d3.scaleBand().domain(["collision", "nearmiss", "hazard", "theft"]))
  .xUnits(dc.units.ordinal)
  .yAxisLabel(gettext("Count"))
  .elasticY(true)
  .title(function(d){ return d.value; })
  .dimension(p_typeDimension)
  .group(countTypes)
  .colors(colorScale)
  .colorAccessor(function(d){return (d.key);})
  .on('filtered', changeMap);
barTypes.xAxis()
  .tickFormat(function(v){ return labels[v]; });
barTypes.yAxis().ticks(6).tickSizeOuter(0);
barTypes.render();

// Bar chart for reports this week
var barWeek = new dc.BarChart("#barWeek");
barWeek
  .width(null)
  .height(null)
  .margins({top: 10, right: 50, bottom: 30, left: 40})
  .x(d3.scaleLinear().domain([-0.5,6.5]))
  .yAxisLabel(gettext("Count"))
  .centerBar(true)
  .elasticY(true)
  .dimension(weekdayDimension)
  .group(weekdayCount, gettext("Collisions")).valueAccessor(function(d){return d.value.collision; })
  .stack(weekdayCount, gettext("Nearmisses"), function(d){ return d.value.nearmiss; })
  .stack(weekdayCount, gettext("Hazards"), function(d){ return d.value.hazard; })
  .stack(weekdayCount, gettext("Thefts"), function(d){ return d.value.theft; })
  .brushOn(true)
  .colors(colorScale)
  .on('filtered', changeMap);
barWeek.yAxis()
  .tickFormat(d3.format("d"))
  .tickSizeOuter(0)
  .ticks(6);
barWeek.xAxis()
  .tickValues([0,1,2,3,4,5,6])
  .tickFormat(function(v){ return weekdayScale((v+1)%7); });
barWeek.render();

// Bar chart for reports by hour of day
var barHour = new dc.BarChart("#barHour");
barHour
  .width(null)
  .height(null)
  .margins({top: 10, right: 50, bottom: 30, left: 40})
  .x(d3.scaleLinear().domain([0,24]))
  .yAxisLabel(gettext("Count"))
  .elasticY(true)
  .dimension(hourDimension)
  .group(countPerHour, "Collisions").valueAccessor(function(d){return d.value.collision; })
  .stack(countPerHour, "Nearmisses", function(d){ return d.value.nearmiss; })
  .stack(countPerHour, "Hazards", function(d){ return d.value.hazard; })
  .stack(countPerHour, "Thefts", function(d){ return d.value.theft; })
  .brushOn(true)
  .colors(colorScaleHour)
  .on('filtered', changeMap);
barHour.yAxis()
  .tickFormat(d3.format("d"))
  .tickSizeOuter(0)
  .ticks(6);
barHour.render();

// bar chart of total reports per day
var barDate = new dc.BarChart("#barDate");
barDate
  .width(575)
  .height(200)
  .x(d3.scaleLinear().domain([-360, 0]))
  .yAxisLabel(gettext("Count"))
  .centerBar(true)
  .elasticY(true)
  .dimension(dateDimension)
  .group(countPerDay)
  .brushOn(true)
  .on('filtered', changeMap);
barDate.yAxis()
  .tickFormat(d3.format("d"))
  .tickSizeOuter(0)
  .ticks(4);
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
