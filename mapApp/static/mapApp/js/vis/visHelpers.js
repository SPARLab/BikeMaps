/** SET UP **/

// Set date formats to local language
moment.locale(LANGUAGE_CODE)

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

// var timeScale = d3.scaleTime()
    // .domain(d3.extent(data, d => d.momentDate));

var timeScale = d3.scaleTime().domain([new Date(2012, 0, 1), new Date(2022, 05, 31)])

data.forEach(d => {
    d.momentDate = moment(d.properties.date);
    d.month = d3.timeMonth(d.momentDate); // pre-calculate month for better performance
});

const dateTickValues = () => {
  var firsts = [];
  // Calculate the day difference between now and the first of every month
  for(var i = 0; i<12; i++) {
        firsts.push(moment()
        .subtract(moment().date()-1, "days")
        .subtract(i, "months")
        .diff(moment(), "days"));
  }
  return firsts;
}

// Define crossfilter dataset
var xf = crossfilter(data);
console.log(data[0])

// Define dimensions to filter according to defined value accessor functions
var p_typeDimension = xf.dimension(d=> d.properties.p_type),
    weekdayDimension = xf.dimension(d => (d.momentDate.weekday()+6)%7),
    dateDimension = xf.dimension(d => d.momentDate.diff(moment(), "days")),
    geomDimension = xf.dimension(d => ({'lat': d.geometry.coordinates[1], 'lng': d.geometry.coordinates[0]})),
    hourDimension = xf.dimension(d => d.momentDate.hour()),
    monthDimension = xf.dimension(d => d.month);

// Define groups to count records
var all = xf.groupAll(),
    countTypes = p_typeDimension.group().reduceCount(),
    weekdayCount = weekdayDimension.group().reduce(reduceAddTypeCount(), reduceRemoveTypeCount(), reduceInitTypeCount()),
    countPerHour = hourDimension.group().reduce(reduceAddTypeCount(), reduceRemoveTypeCount(), reduceInitTypeCount()),
    countPerDay = dateDimension.group().reduceCount();
    countPerMonth = monthDimension.group().reduce(reduceAddTypeCount(), reduceRemoveTypeCount(), reduceInitTypeCount());

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
