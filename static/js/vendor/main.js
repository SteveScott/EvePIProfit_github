/*
$(document).ready(function() {
    $('#mainTable').DataTable( {
        paging:   true,
        ordering: true,
        info:     true,
        aaSorting: [[4, "asc"]]
    } );
} );
*/

$(document).ready(function() {
    $('#mainTable').dataTable( {
        stateSave: true,
        "iDisplayLength": 100,
        "aaSorting": [[ 4, "asc" ]],
        "columns": [ {"data": "Level"},
                    {"data": "Name"},
            {
                //"data": "Price"

                 render: function (data, row, meta) {
                 var num = $.fn.dataTable.render.number(',', '.', 2, '\u01B5 ').display(data);
                 return num;
                 }


            },
                    {render: function (data, row, meta) {
                 var num = $.fn.dataTable.render.number(',', '.', 2, '\u01B5 ').display(data);
                 return num;
                 }},
                    {render: function (data, row, meta) {
                 var num = $.fn.dataTable.render.number(',', '.', 2).display(data);
                 return '\u01B5 ' + num;
                 }},
                    {"data": "Profit-Margin"},
                    {"data": "Datetime"}


                   ]
    } );

} );

/*
$(document).ready(function() {
    $('#mainTable').dataTable({
        stateSave: true,
        "iDisplayLength": 100,
        "aaSorting": [[4, "asc"]],
        'columns': [{
            render: function (data, type, row, meta) {
                if (type === 'currency') {
                    var num = $.fn.dataTable.render.number(',', '.', 2, '$').display(data);
                    return num;
                }
            }
        }
        ]
    })
});



/*
var h = 100;
var w = 200;

    monthlySales = [
      {"month":10, "sales":20},
      {"month":20, "sales":14},
      {"month":30, "sales":20},
      {"month":40, "sales":21},
      {"month":50, "sales":15}
    ];

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
      */