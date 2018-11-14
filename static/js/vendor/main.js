

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
                type: "6.@data-order",
                sort : "6.@data-order"
            }},
            {targets:[7],
            data:{

                type:"7.@data-order",
                sort:"7.@data-order"
            }},
            {targets:[8],
                data:{

                type: "8.@data-order",
                sort: "8.@data-order"
            }},
            {
                targets:[9],
                data:{
                       type: "9.@data-order",
                       sort: "9.@data-order"
                }
            },
            {
                targets:[10],
                data:{
                    type:"10.@data-order",
                    sort:"10.@data-order"
                }
            },
            {"type": "date"}
        ]
            ,
        "columns": [{"data": "Level"},
                    {"data": "Name"},


           /*\u01B5*/
                    {
                        type: "num-fmt",
                        //"data": "Price"
                        name:'sell-price',
                         render: function (data, row, meta) {
                             var num = $.fn.dataTable.render.number(',', '.', 2).display(data);
                             return num;
                         }
                    },
                    {
                        type:"num-fmt",
                        name: 'buy-price',
                        render: function (data, row, meta) {
                        var num = $.fn.dataTable.render.number(',', '.', 2).display(data);
                        return num;
                     }},
                    {
                        type:"num-fmt",
                        name:"taxes",
                        render: function (data, row, meta) {
                        var num = $.fn.dataTable.render.number(',', '.', 2).display(data);
                        return num;
                        }
                    },
                    {
                        type:"num-fmt",
                        name: 'sell-cost',
                        render: function (data, row, meta) {
                        var num = $.fn.dataTable.render.number(',', '.', 2).display(data);
                        return num;
                        }
                    },
                    {
                        type:"num-fmt",
                        name: 'buy-cost',
                        render: function (data, row, meta) {
                        var num = $.fn.dataTable.render.number(',', '.', 2).display(data);
                        return num;
                        }
                    },
                    {
                        type:"num-fmt",
                        render: function (data, row, meta) {
                        var num = $.fn.dataTable.render.number(',', '.', 2).display(data);
                        return num;
                        }
                    },
                    {
                        type: "num-fmt",
                        "data": "Profit-Margin"
                    },
                    {
                        type:"num-fmt"

                    },
                    {"data": "Datetime"}
                   ]
    } );




                // CSS selector
                $("input[name=tax_rate]").on('input', function() {
                    updateTaxes();
                });

                    $(document).on('change load', function() {
                        updateTaxes();
                });





    buyFromBuyAction();
    sellToSellAction();
    var event = new Event('change');
    document.dispatchEvent(event);


} );



function roundMe (number) {
                if (isNaN(number)){
                    return 0;
                }
                return Math.round((number * 100)) / 100;
            }

function buyFromBuyAction(){
                        var table = $('#mainTable').DataTable();
                        table.columns(5).visible(false);
                        table.columns(6).visible(true);
}

function buyFromSellAction(){
    var table = $('#mainTable').DataTable();
    table.columns(5).visible(true);
    table.columns(6).visible(false);
}

function sellToBuyAction(){
        var table = $('#mainTable').DataTable();
        //table.columns(2).visible(true);
        //table.columns(3).visible(true);
}



function sellToSellAction() {
            var table = $('#mainTable').DataTable();
            //table.columns(2).visible(true);
            //table.columns(3).visible(true);
}

function triggerChangeEvent(){
    var event = new Event('change');
    document.dispatchEvent(event);
}



function updateTaxes() {


    var taxValue = document.getElementsByName('tax-rate')[0].value;
    var taxRate = parseFloat(taxValue) / 100.0;

    // corner case
    if (isNaN(taxRate))
        taxRate = 0;

    $("#mainTable tbody tr").each(function () {
        var newCost = -9999999999999;
        var level = $(this).find(".level").text()
        //var level = $(this).children(":first").text();
        var sellPriceTd = $(this).find(".price").first();
        var buyPriceTd = $(this).find(".buy-price").first();
        var sellCostTd = $(this).find(".cost").first();
        var buyCostTd = $(this).find(".buy-cost").first();
        //var priceTd = $(this).find(".cost").first();
        var taxesTd = $(this).find(".taxes").first();
        var costTd = $(this).find(".cost").first();
        var spreadTd = $(this).find(".spread").first();
        var profitTd = $(this).find(".profit").first();
        var marginTd = $(this).find(".margin").first();
        var cmdtyName = $(this).children(":nth-child(2)").text();
        var buySpread = parseFloat($(buyPriceTd).data("original"));
        var sellSpread = parseFloat($(sellPriceTd).data("original"));
        var taxes = 0;

        var originalPrice = null;
        if (document.getElementById('buy-from-buy').checked) {
            originalPrice = $(buyCostTd).data("original");
        }
        else {
            originalPrice = $(costTd).data("original");
        }

        originalPrice = Number(originalPrice);
        var sellPrice = null;
        if (document.getElementById('sell-to-buy').checked) {
            sellPrice = $(buyPriceTd).data("original");
        }
        else {
            sellPrice = $(sellPriceTd).data("original");
        }
        //var sellPrice = $(sellPriceTd).data("original");
        sellPrice = Number(sellPrice);
        // level == "P0"/"P1"/"P2"
        if (level == "P0") {
            taxes = 5 * taxRate;
            newCost = (taxes);
        } else if (level == "P1") {
            taxes = (400.0 * taxRate);
            newCost = originalPrice + taxes;
        } else if (level == "P2") {
            taxes = 10400.0 * taxRate;
            newCost = originalPrice + taxes;
        } else if (level == "P3") {
            if (cmdtyName == "Biotech Research Reports"
                || cmdtyName == "Cryoprotectant Solutions"
                || cmdtyName == "Gel-Matrix Biopaste"
                || cmdtyName == "Hazmat Detection Systems"
                || cmdtyName == "Planetary Vehicles"
                || cmdtyName == "Supercomputers") {
                taxes = 168000.0 * taxRate;
                newCost = originalPrice + taxes;
            } else if (cmdtyName == "Camera Drones"
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
                taxes = 84000.0 * taxRate;
                newCost = originalPrice + taxes;
            } else {
                newCost = -99999999;
            }
        } else if (level == "P4") {
            if (cmdtyName == "Broadcast Node"
                || cmdtyName == "Integrity Response Drones"
                || cmdtyName == "Recursive Computing Module"
                || cmdtyName == "Self-Harmonizing Power Core"
                || cmdtyName == "Wetware Mainframe") {
                taxes = 1740000.0 * taxRate;
                newCost = originalPrice + taxes;
            } else if (cmdtyName == "Nano-Factory"
                || cmdtyName == "Organic Mortar Applicators"
                || cmdtyName == "Sterile Conduits") {
                taxes = 1704000.0 * taxRate;
                newCost = originalPrice + taxes;
            } else {
                newCost = -999999999999999;
            }
        }

        var profit = sellPrice - newCost;
        var profitMargin = profit / sellPrice * 100;
        var spread = ((sellSpread - buySpread) / ((buySpread + sellSpread) / 2)) * 100

        //have to reset the prices because sell price is used in all calculations. Need original sell prices
        var sellToBuyPrice = $(buyPriceTd).data("original");
        var sellToSellPrice = $(sellPriceTd).data("original");

        var priceString = roundMe(sellPrice).toLocaleString();
        var profitString = roundMe(profit).toLocaleString();
        var newCostString = roundMe(newCost).toLocaleString();
        var profitMarginString = roundMe(profitMargin).toLocaleString();
        var spreadString = roundMe(spread).toLocaleString();
        var taxesString = roundMe(taxes).toLocaleString();
        var sellToBuyPriceString = roundMe(sellToBuyPrice).toLocaleString();
        var sellToSellPriceString = roundMe(sellToSellPrice).toLocaleString();


        var price2 = roundMe(sellPrice);
        var profit2 = roundMe(profit);
        var newCost2 = roundMe(newCost);
        var profitMargin2 = roundMe(profitMargin);
        var spread2 = roundMe(spread);
        var sellToBuyPrice2 = roundMe(sellToBuyPrice);
        var sellToSellPrice2 = roundMe(sellToSellPrice);
        var taxes2 = roundMe(taxes);

        $(spreadTd).text(spreadString);
        $(spreadTd).attr('data-order', spread2);
        //$('#mainTable').DataTable().cell($(spreadTd)).invalidate().draw();


        //$(sellPriceTd).text(priceString);
        //$(sellPriceTd).attr('data-order', price2);
        //$('#mainTable').DataTable().cell($(sellPriceTd)).invalidate().draw();


        $(costTd).text(newCostString);
        $(costTd).attr('data-order', newCost2);
        //$('#mainTable').DataTable().cell($(costTd)).invalidate().draw();

        $(buyCostTd).text(newCostString);
        $(buyCostTd).attr('data-order', newCost2);
        //$('#mainTable').DataTable().cell($(costTd)).invalidate().draw();


        $(profitTd).text(profitString);
        $(profitTd).attr('data-order', profit2);
        //$('#mainTable').DataTable().cell($(profitTd)).invalidate().draw();


        $(marginTd).text(profitMarginString);
        $(marginTd).attr('data-order', profitMargin2);
        //$('#mainTable').DataTable().cell($(marginTd)).invalidate().draw();

        $(sellPriceTd).text(sellToSellPriceString);
        $(sellPriceTd).attr('data-order', sellToSellPrice2);
        //$('#mainTable').DataTable().cell($(sellPriceTd)).invalidate().draw();


        $(buyPriceTd).text(sellToBuyPriceString);
        $(buyPriceTd).attr('data-order', sellToBuyPrice2);
        //$('#mainTable').DataTable().cell($(buyPriceTd)).invalidate().draw();

        $(taxesTd).text(taxesString);
        $(taxesTd).attr('data-order', taxes2);
        //$('#mainTable').DataTable().cell($(taxesTd)).invalidate().draw();


    });

    rows().invalidate();
}


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