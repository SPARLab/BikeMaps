// Function to create doughnut chart from dataset
//   * 'data' parameter should be in form of array with each array item a js object.
//   * Each of these objects must have a 'name', 'count', and 'color' field.
//      *  'name' is the data label, e.g. 'Collisions'
//      *  'count' is the number of items in that class, e.g. '8'
//      *  'color' will be used to fill the pie slice, 'e.g. #333228791'
//   * The chart is appended to the DOM as a child of the body element.
//
//   example dataset
//   var data = [
//     {
//         "name": "Collisions",
//         "count": {{ collisions|length }},
//         "color": getColor("collision"),
//     },{
//         "name": "Near misses",
//         "count": {{ nearmisses|length }},
//         "color": getColor("nearmiss"),
//     },{
//         "name": "Hazards",
//         "count": {{ hazards|length }},
//         "color": getColor("hazard"),
//     },{
//         "name": "Thefts",
//         "count": {{ thefts|length }},
//         "color": getColor("theft"),
//     },
//   ]

function doughnutChart(data) {
  var svg = d3.select("body")
    .append("svg")
    .append("g");

  svg.append("g")
  	.attr("class", "slices");
  svg.append("g")
  	.attr("class", "labels");
  svg.append("g")
  	.attr("class", "lines");

  var width = 960,
    height = 450,
  	radius = Math.min(width, height) / 2;

  var pie = d3.layout.pie()
    .sort(null)
    .value(function(d){ return d.count; });

  var arc = d3.svg.arc()
  	.outerRadius(radius * 0.8)
  	.innerRadius(radius * 0.4);

  var outerArc = d3.svg.arc()
  	.innerRadius(radius * 0.9)
  	.outerRadius(radius * 0.9);

  svg.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  var key = function(d){ return d.data.name; };


  /* ------- PIE SLICES -------*/
  var slice = svg.select(".slices").selectAll("path.slice")
  	.data(pie(data), key);

  slice.enter()
  	.insert("path")
  	.style("fill", function(d) { return d.data.color; })
  	.attr("class", "slice");

  slice
  	.attr("d", function(d) {
  		return arc(d);
  	});


  /* ------- TEXT LABELS -------*/
  var text = svg.select(".labels").selectAll("text")
  	.data(pie(data), key);

  text.enter()
  	.append("text")
  	.attr("dy", ".35em")
  	.text(function(d) {
  		return d.data.name;
  	});

  function midAngle(d){
  	return d.startAngle + (d.endAngle - d.startAngle)/2;
  }

  text
  	.attr("transform", function(d) {
  			var pos = outerArc.centroid(d);
  			pos[0] = radius * (midAngle(d) < Math.PI ? 1 : -1);
  			return "translate("+ pos +")";
  	})
  	.style("text-anchor", function(d){
  			return midAngle(d) < Math.PI ? "start":"end";
  	});

  /* ------- SLICE TO TEXT POLYLINES -------*/
  var polyline = svg.select(".lines").selectAll("polyline")
  	.data(pie(data), key);

  polyline.enter()
  	.append("polyline");

  polyline
  	.attr("points", function(d){
  			var pos = outerArc.centroid(d);
  			pos[0] = radius * 0.95 * (midAngle(d) < Math.PI ? 1 : -1);
  			return [arc.centroid(d), outerArc.centroid(d), pos];
  	});
};
