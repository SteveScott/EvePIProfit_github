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
        "aaSorting": [[ 4, "asc" ]]
    } );
} );
