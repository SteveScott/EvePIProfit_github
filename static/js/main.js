
$(document).ready(function() {
    $('#mainTable').DataTable( {
        "paging":   true,
        "ordering": true,
        "info":     true,
        "order": [[4, "asc"]]
    } );
} );