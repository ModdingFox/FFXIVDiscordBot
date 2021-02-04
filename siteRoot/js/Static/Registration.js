function reloadStaticRegistrationData(){
    var payload = {};
    
    payload['playeruserCN'] = $.cookie("cn");
    
    formdata = new FormData();
    formdata.append('Method', 'viewRegistration');
    formdata.append('JSON', JSON.stringify(payload));

    jQuery.ajax({
        type: 'POST',
        url: "/Rest/Static/Registration.php",
        data: formdata,
        processData: false,
        contentType: false,
        success: function (response) {
            var post_return = JSON.parse(response);
            if(post_return.status == 'Success') {
                $('#Modal-playerRegistrationStatic-form')[0].reset();
                $('#Modal-playerRegistrationStatic-hasSavageExperience').prop('checked', post_return.result['hasSavageExperience']);
                $('#Modal-playerRegistrationStatic-hasRaidExperience').prop('checked', post_return.result['hasRaidExperience']);
                $('#Modal-playerRegistrationStatic-playerAvaliabliltySunday').prop('checked', post_return.result['sunday']);
                $('#Modal-playerRegistrationStatic-playerAvaliabliltyMonday').prop('checked', post_return.result['monday']);
                $('#Modal-playerRegistrationStatic-playerAvaliabliltyTuesday').prop('checked', post_return.result['tuesday']);
                $('#Modal-playerRegistrationStatic-playerAvaliabliltyWednesday').prop('checked', post_return.result['wednesday']);
                $('#Modal-playerRegistrationStatic-playerAvaliabliltyThursday').prop('checked', post_return.result['thursday']);
                $('#Modal-playerRegistrationStatic-playerAvaliabliltyFriday').prop('checked', post_return.result['friday']);
                $('#Modal-playerRegistrationStatic-playerAvaliabliltySaturday').prop('checked', post_return.result['saturday']);
            }
            else if (post_return.status == 'Warning') {
                alert(post_return.status + " " + post_return.warning);
            }
            else if (post_return.status == 'Error') {
                alert(post_return.status + " " + post_return.error);
            }
            else { alert("Did not get status from server"); }
        }
    });
}

$(document).ready(function(){
    $("#Modal-playerRegistrationStatic-save").click(function(){
        var payload = {};
        
        $('input[id^="Modal-playerRegistrationStatic"]').each(function( ) {
            if($( this ).attr('type') == 'checkbox') {
                payload[$( this ).attr('id').replace("Modal-playerRegistrationStatic-", "")] = $( this ).is(':checked');
            } else {
                payload[$( this ).attr('id').replace("Modal-playerRegistrationStatic-", "")] = $( this ).val();
            }
        });

        formdata = new FormData();
        formdata.append('Method', 'updateRegistration');
        formdata.append('JSON', JSON.stringify(payload));

        jQuery.ajax({
            type: 'POST',
            url: "/Rest/Static/Registration.php",
            data: formdata,
            processData: false,
            contentType: false,
            success: function (response) {
                var post_return = JSON.parse(response);
                if(post_return.status == 'Success') {
                    reloadStaticRegistrationData();
                }
                else if (post_return.status == 'Warning') {
                    alert(post_return.status + " " + post_return.warning);
                }
                else if (post_return.status == 'Error') {
                    alert(post_return.status + " " + post_return.error);
                }
                else { alert("Did not get status from server"); }
            }
        });
    });
    
    $("#Modal-playerRegistrationStatic-delete").click(function(){
        var payload = {};
        
        formdata = new FormData();
        formdata.append('Method', 'deleteRegistration');
        formdata.append('JSON', JSON.stringify(payload));
        
        jQuery.ajax({
            type: 'POST',
            url: "/Rest/Static/Registration.php",
            data: formdata,
            processData: false,
            contentType: false,
            success: function (response) {
                var post_return = JSON.parse(response);
                if(post_return.status == 'Success') {
                    reloadStaticRegistrationData();
                }
                else if (post_return.status == 'Warning') {
                    alert(post_return.status + " " + post_return.warning);
                }
                else if (post_return.status == 'Error') {
                    alert(post_return.status + " " + post_return.error);
                }
                else { alert("Did not get status from server"); }
            }
        });
    });
    
    reloadStaticRegistrationData();
});
