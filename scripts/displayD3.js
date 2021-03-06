function displayD3(){
    var persistentData = {{chart|safe}};
    var h = 100;
    var w = 200;

    monthlySales = [
      {"month":10, "sales":20},
      {"month":20, "sales":14},
      {"month":30, "sales":20},
      {"month":40, "sales":21},
      {"month":50, "sales":15}
    ];


    var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;


    var lineFun = d3.svg.line()
      .x(function(d) {return d.month*2;})
      .y(function(d) {return h-d.sales;})
      .interpolate("linear")

    var svg = d3.select("body").append("svg")
        .attr({width:w, height:h});

    var viz = svg.append("path")
      .attr({
        d: lineFun(monthlySales),
        "stroke": "purple",
        "fill":"none",
        "stroke-width":2,
      })

    var lineFun2 = d3.svg.line()
    persistentData.forEach(function(d){
        d.mytime = parseDate(d.myTime);
        });
}