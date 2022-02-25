/** SET UP **/

// map p_types of points to nice labels
var labels = {
  "collision": gettext("Collisions"),
  "nearmiss": gettext("Nearmisses"),
  "hazard": gettext("Hazards"),
  "theft": gettext("Thefts"),
}
// Define scales
// map p_type to appropriate colors
var colorScale = d3.scaleOrdinal()
    .domain(["collision", "nearmiss", "hazard", "theft"])
    .range([iconColors.collision, iconColors.nearmiss, iconColors.hazard, iconColors.theft]);

var weekdayScale = d3.scaleQuantize()
    .domain([0,6])
    .range(moment.weekdaysShort());

// Set date formats to local language
moment.locale(LANGUAGE_CODE)

// Define crossfilter dataset
var xf = crossfilter(data);

// Define dimensions
var p_typeDimension = xf.dimension(function(d) {return d.properties.p_type;}),
    weekdayDimension = xf.dimension(function(d) {return (moment(d.properties.date).weekday()+6)%7 }),
    dateDimension = xf.dimension(function(d){ return moment(d.properties.date).diff(moment(), "days"); }),
    geomDimension = xf.dimension(function(d){ return {'lat': d.geometry.coordinates[1], 'lng': d.geometry.coordinates[0]} }),
    hourDimension = xf.dimension(function(d){ return moment(d.properties.date).hour(); });

// Define groups
var all = xf.groupAll(),
    countTypes = p_typeDimension.group().reduceCount(),
    weekdayCount = weekdayDimension.group().reduce(reduceAddTypeCount(), reduceRemoveTypeCount(), reduceInitTypeCount()),
    countPerHour = hourDimension.group().reduce(reduceAddTypeCount(), reduceRemoveTypeCount(), reduceInitTypeCount()),
    countPerDay = dateDimension.group().reduceCount();

/** DATA FILTER FUNCTIONS **/
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

/** MAP UPDATE FUNCTIONS **/
function urlUpdate(){
  var zoom = map.getZoom(),
      center = map.getCenter();
  window.history.replaceState({}, "", "@" + center.lat.toFixed(7) + "," + center.lng.toFixed(7) + "," + zoom + "z");
}

function changeMap(){
  heat_data = [];

  geomDimension.top(Infinity).forEach(function(feature){
    heat_data.push({
      'lat': feature.geometry.coordinates[1],
      'lng': feature.geometry.coordinates[0],
      'value': 1
    });
  });
  heatLayer.setData({ max:1, data: heat_data });

};

function mapFilter(){
  var bounds = map.getBounds();
  geomDimension.filterFunction(function(d){
    return bounds.contains([d.lat, d.lng]);
  })
  changeMap();
  dc.redrawAll();

  urlUpdate();
}
