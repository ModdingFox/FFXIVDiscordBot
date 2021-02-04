$(document).ready(function () {
    $('#Body-Static_Search-playerTable').DataTable();
    $('.dataTables_length').addClass('bs-select');

    $("#Body-Static_Search-search").click(function(){
        var payload = {};

        $(':input[id^="Body-Static_Search"]:not(:button)').each(function( ) {
            if($( this ).attr('type') == 'checkbox') {
                payload[$( this ).attr('id')] = $( this ).is(':checked');
            } else {
                payload[$( this ).attr('id')] = $( this ).val();
            }
        });

        formdata = new FormData();
        formdata.append('Method', 'searchPlayer');
        formdata.append('JSON', JSON.stringify(payload));
        
        jQuery.ajax({
            type: 'POST',
            url: "/Rest/Static/Search.php",
            data: formdata,
            processData: false,
            contentType: false,
            success: function (response) {
                var post_return = JSON.parse(response);
                if(post_return.status == 'Success') {
                    $('#Body-Static_Search-playerTable').DataTable().clear().draw();
                    $.each(post_return.result, function( index, value ) {
                        $('#Body-Static_Search-playerTable').dataTable().fnAddData( [
                            value.characterName,
                            value.hasSavageExperience,
                            value.hasRaidExperience,
                            value.name,
                            value.currentLevel,
                            value.averageILevel,
                            value.hasMeldsCheckbox,
                            value.playerAvaliablilty
                        ]);
                    });
                }
                else if (post_return.status == 'Warning') {
                    alert(post_return.status + " " + post_return.warning);
                    window.location.href = "index.php?Page_Name=Home";
                }
                else if (post_return.status == 'Error') {
                    alert(post_return.status + " " + post_return.error);
                }
                else { alert("Did not get status from server"); }
            }
        });
    });
});
