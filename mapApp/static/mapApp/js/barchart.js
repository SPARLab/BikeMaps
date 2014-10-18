// TODO add axis
// 	Make height nicer
//  Make chart responsive to window resize

function initializeBarChart(data) {
    var margin = {
        top: 20,
        right: 30,
        bottom: 30,
        left: 40
    };

    var width = $('#barchart').width() - margin.left - margin.right,
        height = width / 2 - margin.top - margin.bottom,
        barWidth = width / data.length;

    // SCALES
    var x = d3.scale.ordinal()
        .domain(data.map(function(d) {
            return d.type;
        }))
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear() // function that translates data to a height value based on the value of d in data
    .domain([0, d3.max(data, function(d) {
        return d.value;
    })])
        .range([height, 0]);

    // AXES
    // y axis
    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(d3.max(data, function(d) {
            return d.value
        }))
        .tickFormat(d3.format("d"))
        .tickSubdivide(0);

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
        .attr("fill", function(d) {
            return d.color;
        })
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


};