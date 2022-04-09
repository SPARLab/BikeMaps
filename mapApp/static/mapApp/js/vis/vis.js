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
  .title(function(d){return `${labels[d.key]}: ${d.value}`; })
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
  // .renderTitle(true)
  // .title(function(d){return `${this.layer}: ${this.y1 - this.y0}`})
  .brushOn(true)
  .dimension(weekdayDimension)
  .group(weekdayCount, gettext("Collisions")).valueAccessor(function(d){
    // console.log(d);

    return d.value.collision; })
  .stack(weekdayCount, gettext("Nearmisses"), function(d){ return d.value.nearmiss; })
  .stack(weekdayCount, gettext("Hazards"), function(d){ return d.value.hazard; })
  .stack(weekdayCount, gettext("Thefts"), function(d){ return d.value.theft; })
  .colors(colorScale)
  .on('filtered', changeMap);
barWeek.yAxis()
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
  .renderTitle(true)
  .title(function(d){
    // console.log(d);
    // console.log(this);
    return `${this.layer}: ${this.y1 - this.y0}`})
  .brushOn(false)
  .dimension(hourDimension)
  .group(countPerHour, gettext("Collisions")).valueAccessor(function(d){return d.value.collision; })
  .stack(countPerHour, gettext("Nearmisses"), function(d){ return d.value.nearmiss; })
  .stack(countPerHour, gettext("Hazards"), function(d){ return d.value.hazard; })
  .stack(countPerHour, gettext("Thefts"), function(d){ return d.value.theft; })
  .colors(colorScale)
  .on('filtered', changeMap);
barHour.yAxis()
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
  .colors(d3.schemeSet2)
  .on('filtered', changeMap);
barDate.yAxis().ticks(3);
barDate.xAxis()
  .tickFormat(function(v){
    return moment().add(v, "days").format("ll").slice(0, -6);
  })
  .tickValues(dateTickValues());

barDate.render();

var lineDate = new dc.CompositeChart("#lineDate");
lineDate
  .width(null)
  .height(null)
  .x(timeScale)
  .round(d3.timeMonth.round)
  .xUnits(d3.timeMonths)
  .yAxisLabel(gettext("Count"))
  .elasticY(true)
  .colors(colorScale)
  .renderTitle(true)
  .title(function(d) {
    return `${moment(this.x).format('MMM YYYY')}\n${this.layer}: ${this.y1 - this.y0}`
  })
  .brushOn(false)
  .compose([
    new dc.LineChart(lineDate)
    .dimension(monthDimension)
    .colors(colorScale)
    .group(countPerMonth, gettext("Collisions")).valueAccessor(function(d) {
      return d.value.collision;
    }),
    new dc.LineChart(lineDate)
    .dimension(monthDimension)
    .colors(colorScale)
    .group(countPerMonth, gettext("Nearmisses")).valueAccessor(function(d) {
      return d.value.nearmiss;
    }),
    new dc.LineChart(lineDate)
    .dimension(monthDimension)
    .colors(colorScale)
    .group(countPerMonth, gettext("Hazards")).valueAccessor(function(d) {
      return d.value.hazard;
    }),
    new dc.LineChart(lineDate)
    .dimension(monthDimension)
    .colors(colorScale)
    .group(countPerMonth, gettext("Thefts")).valueAccessor(function(d) {
      return d.value.theft;
    }),
  ])

// Fit map extent to alert areas boundary
if (alertAreas.getLayers().length > 0) {
  map.fitBounds(alertAreas.getBounds());
}

dc.renderAll();
dc.redrawAll();
