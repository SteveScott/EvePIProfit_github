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
function roundMe (number) {
                return Math.round((number * 100)) / 100;
            }

$(document).ready(function() {
    $('#mainTable').dataTable( {
        stateSave: true,
        "dom":'<<"#filter"f><"#lenght_field"l>r<t>ip>',
        "iDisplayLength": 100,
        "aaSorting": [[ 4, "asc" ]],
        "columnDefs":[
            {"type": "string"},
            {"type": "string"},
            {
                targets:[3],
                data:{
                    _: "3.display",
                    type: "3.@data-order",
                    sort: "3.@data-order"
                }
            },
            {
                targets:[4],
                data:{
                _: "4.display",
                  type: "4.@data-order",
                sort : "4.@data-order"
                }
            },
            {
                targets: [5],
                data: {
                   _: "5.display",
                         type: "5.@data-order",
                    sort: "5.@data-order"
                }
            },
            {targets:[6],
            data: {
                _: "6.display",
                      type: "5.@data-order",
                 sort : "6.@data-order"
            }},
            {"type": "date"}
            ],
        "columns": [{"data": "Level"},
                    {"data": "Name"},


           /*\u01B5*/
                    {
                        //"data": "Price"
                         render: function (data, row, meta) {
                             var num = $.fn.dataTable.render.number(',', '.', 2).display(data);
                             return num;
                         }
                    },
                    {render: function (data, row, meta) {
                        var num = $.fn.dataTable.render.number(',', '.', 2).display(data);
                        return num;
                     }},
                    {render: function (data, row, meta) {
                        var num = $.fn.dataTable.render.number(',', '.', 2).display(data);
                        return num;
                        }
                    },
                    {"data": "Profit-Margin"},
                    {"data": "Datetime"}
                   ]
    } );



            $(document).ready(function() {
                // CSS selector
                $("input[name=tax_rate]").on('input', function() {

                    var taxRate = parseFloat($(this).val()) / 100.0;

                    // corner case
                    if (isNaN(taxRate))
                        taxRate = 0;

                    $("#mainTable tbody tr").each(function () {
                        var newCost = -9999999999999;
                        var level = $(this).find(".level").text()
                        //var level = $(this).children(":first").text();
                        var sellPriceTd = $(this).find(".price").first();
                        //var priceTd = $(this).find(".cost").first();
                        var costTd = $(this).find(".cost").first();
                        var profitTd = $(this).find(".profit").first();
                        var marginTd = $(this).find(".margin").first();
                        var cmdtyName = $(this).children(":nth-child(2)").text();
                        var originalPrice = $(costTd).data("original");
                        originalPrice = Number(originalPrice);
                        var sellPrice = $(sellPriceTd).data("original");
                        // level == "P0"/"P1"/"P2"
                        if (level == "P0") {
                            newCost = (5 * taxRate);
                        } else if (level == "P1") {
                            newCost = originalPrice + (400.0 * taxRate);
                        } else if (level == "P2") {
                            newCost = originalPrice + (10400.0 * taxRate);
                        } else if (level == "P3") {
                            if (cmdtyName == "Biotech Research Reports"
                                || cmdtyName == "Cryoprotectant Solutions"
                                || cmdtyName == "Gel-Matrix Biopaste"
                                || cmdtyName == "Hazmat Detection Systems"
                                || cmdtyName == "Planetary Vehicles"
                                || cmdtyName == "Supercomputers") {
                                newCost = originalPrice + (168000.0 * taxRate);
                            } else if (    cmdtyName == "Camera Drones"
                                        || cmdtyName == "Condensates"
                                        || cmdtyName == "Data Chips"
                                        || cmdtyName == "Guidance Systems"
                                        || cmdtyName == "Hermetic Membranes"
                                        || cmdtyName == "High-Tech Transmitters"
                                        || cmdtyName == "Industrial Explosives"
                                        || cmdtyName == "Neocoms"
                                        || cmdtyName == "Nuclear Reactors"
                                        || cmdtyName == "Robotics"
                                        || cmdtyName == "Smartfab Units"
                                        || cmdtyName == "Synthetic Synapses"
                                        || cmdtyName == "Transcranial Microcontrollers"
                                        || cmdtyName == "Ukomi Superconductors"
                                        || cmdtyName == "Vaccines") {
                                newCost = originalPrice + (84000.0 * taxRate);
                            } else {
                                newCost = -99999999;
                                    }
                        } else if (level == "P4"){
                            if (cmdtyName == "Broadcast Node"
                                || cmdtyName == "Integrity Response Drones"
                                || cmdtyName == "Recursive Computing Module"
                                || cmdtyName == "Self-Harmonizing Power Core"
                                || cmdtyName == "Wetware Mainframe") {
                                newCost = originalPrice + (1740000.0 * taxRate);
                            } else if (cmdtyName == "Nano-Factory"
                                       || cmdtyName == "Organic Mortar Applicators"
                                       || cmdtyName == "Sterile Conduits") {
                                      newCost = originalPrice + (1704000.0 * taxRate);
                            } else {
                                newCost = -9999999999;
                            }
                        }

                        var profit = sellPrice - newCost;
                        var profitMargin = profit / sellPrice * 100;
                        var priceString = roundMe(sellPrice).toLocaleString();
                        var profitString =  roundMe(profit).toLocaleString();
                        var newCostString = roundMe(newCost).toLocaleString();
                        var profitMarginString = roundMe(profitMargin).toLocaleString();


                        var price2 = roundMe(sellPrice);
                        var profit2 =  roundMe(profit);
                        var newCost2 = roundMe(newCost);
                        var profitMargin2 = roundMe(profitMargin);

                        $(sellPriceTd).text(priceString);
                        $(sellPriceTd).attr('data-order', price2);
                        $('#mainTable').DataTable().cell($(sellPriceTd)).invalidate().draw();


                        $(costTd).text(newCostString);
                        $(costTd).attr('data-order', newCost2);
                        $('#mainTable').DataTable().cell($(costTd)).invalidate().draw();


                        $(profitTd).text(profitString);
                        $(profitTd).attr('data-order', profit2);
                        $('#mainTable').DataTable().cell($(profitTd)).invalidate().draw();


                        $(marginTd).text(profitMarginString);
                        $(marginTd).attr('data-order', profitMargin2);
                        $('#mainTable').DataTable().cell($(marginTd)).invalidate().draw();
                        
                    });
                });
            });
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



/* //Some D3 waiting to be implemented
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