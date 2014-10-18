// TODO add axis
// 	Make height nicer

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

    var y = d3.scale.linear() // function that translates data to a height value based on the value of d in data
    .domain([0, d3.max(data, function(d) {
        return d.value;
    })])
        .range([height, 0]);

    // SVG chart elemet
    var chart = d3.select("#barchart")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Create a bar for each element in data
    var bar = chart.selectAll("g") // creates d and i. i is the i'th element in data and d is the data at data[i]
    .data(data)
        .enter().append("g")
        .attr("transform", function(d, i) {
            return "translate(" + i * barWidth + ",0)";
        });

    bar.append("rect")
        .attr("y", function(d) {
            return y(d.value);
        })
        .attr("height", function(d) {
            return height - y(d.value);
        })
        .attr("width", barWidth - 5)
        .attr("fill", function(d) {
            return d.color;
        });

    bar.append("text")
        .attr("x", 5)
        .attr("y", height - 3)
    // .attr("dy", "1em")
    .text(function(d) {
        return d.type;
    });

    // TODO add x and y axis
    // y axis
    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    chart.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    // x axis
    // var xAxis = d3.svg.axis()
    //     .orient("bottom");

    // chart.append("g")
    //     .attr("class", "x axis")
    //     .translate
    //     .call(xAxis);

    // $(window).resize(function() {
    //     // Updated parameters
    //     var width = $("#barchart").parent().width() - margin.left - margin.right,
    //         height = width / 2 - margin.top - margin.bottom,
    //         barWidth = width / data.length;
    //     x.range([0, height]);

    //     // Resize chart according to new width and height
    //     chart
    //         .attr("width", width + margin.left + margin.right)
    //         .attr("height", height + margin.top + margin.bottom);

    //     bar.attr("transform", function(d, i) {
    //         return "translate(" + i * barWidth + ",)";
    //     })
    //     bar.select("rect")
    //         .attr("width", barWidth - 5)
    //         .attr("y", function(d) {
    //             return height - y(d.value);
    //         })
    //         .attr("height", function(d) {
    //             return y(d.value);
    //         });
    //     bar.select("text")
    //         .attr("y", height - 3);

    // });
};