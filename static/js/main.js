
$(document).ready(function() {
    $('#mainTable').DataTable( {
        paging:   true,
        ordering: true,
        info:     true,
        aaSorting: [[4, "asc"]]
    } );
} );