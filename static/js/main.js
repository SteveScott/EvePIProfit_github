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
        "formatNumber": function (toFormat){
        return toFormat.toString().replace(
        /\B(?=(\d{3})+(?!\d))/g, ",");
        };
        "aaSorting": [[ 4, "asc" ]]
    } );
} );
