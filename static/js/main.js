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
        "aaSorting": [[ 4, "asc" ]]
    } );
    $.fn.digits = function(){
        return this.each(function(){
            $(this).text($(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
            })
    }
    $("span.numbers").digits();
} );
