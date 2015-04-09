// TODO
// On mouse rollover, display the number of points in each category on barchart

// Initialize the SVG barchart via calls to d3.js library
function initializeBarChart(data) {
    var margin = {
        top: 20,
        right: 30,
        bottom: 30,
        left: 40
    };

    var width = 500 - margin.left - margin.right,
        height = 250 - margin.top - margin.bottom,
        barWidth = width / data.length;

    // SCALES
    var x = d3.scale.ordinal()
        .domain(data.map(function(d) {
            return d.type;
        }))
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .domain([0, d3.max(data, function(d) {
            return d.value;
        })])
        .nice(10)
        .range([height, 0]);

    // AXES
    // y axis
    var yAxis = d3.svg.axis().scale(y)
        .orient("left")
        // .ticks(10)
        .tickSubdivide(0)
        .tickFormat(d3.format("d"));

    // x axis
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    // SVG CHART ELEMENT
    var chart = d3.select("#barchart")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    chart.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    chart.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // Create a bar for each element in data
    chart.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("type", function(d) {
            return d.type;
        })
        .attr("fill", function(d) {
            return d.color;
        })
        .attr("stroke", "#0ff")
        .attr("stroke-width", "0")
        .attr("x", function(d) {
            return x(d.type);
        })
        .attr("y", function(d) {
            return y(d.value);
        })
        .attr("height", function(d) {
            return height - y(d.value);
        })
        .attr("width", x.rangeBand());

    highlightPoints();
};


// Controls the highlight of barchart rectangles and corresponding points on map. Called by initialize barchart
function highlightPoints(){
    $("#barchart rect").mouseenter(function(){
        // highlight chart rectangle
        $(this).attr("stroke-width", "3");

        // show highlighted points on map
        var layer = getLayer($(this).attr("type"));
        layer[0].setStyle({
            fillColor: '#0ff',
            fillOpacity: 1
        });

        if (!L.Browser.ie && !L.Browser.opera) {
            layer[1].bringToFront();
            layer[0].bringToFront();
        }
    }).mouseleave(function(){
        // Unhighlight rect in char
        $(this).attr("stroke-width", "0");

        // Unhighlight points on map
        var type = $(this).attr("type");
        getLayer(type)[0].setStyle({
            fillColor: getColor(type),
            fillOpacity: 0.8
        });
    });
};

// Helper method returns the var layer names in stats.html using simple type parameter. eg, calling with type 'collision' returns all the collision layers
function getLayer(type){
    if(type == "collision") return [recentCollisionsLayer, allCollisionsLayer]
    else if(type == "nearmiss") return [recentNearmissesLayer, allNearmissesLayer];
    else if(type == "hazard") return [recentHazardsLayer, allHazardsLayer];
    else return [recentTheftsLayer, allTheftsLayer];
};

// Filter a GeoJSON object with date property by a range starting with startDate, ending with endDate
// 	startDate is exclusive, endDate is inclusive.
// 	if startDate null, all dates prior or equal to endDate inclusive
function filterGeoJSONByDate(geojson, startDate, endDate){
  var result = geojson;
  result.features = $.grep(geojson.features, function(n,i){ return (moment(n.properties.date) <= endDate); });
  if(startDate)
    result.features = $.grep(geojson.features, function(n,i){ return (moment(n.properties.date) > startDate); });
  return result;
};

// Initialize the SVG linechart via calls to the d3.js library
function initializeLineChart(data){
    return;
};
