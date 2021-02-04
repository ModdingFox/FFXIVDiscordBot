$.updateEditPlayerCharacterClassModalData = function (){
    var payload = {};
    payload['playeruserCN'] = $.cookie("cn");
    payload['playerCharacterId'] = $('#Modal-editPlayerCharacter-selectCharacter').val();
    
    if(payload['playerCharacterId'] == null) { payload['playerCharacterId'] = -1; }
    
    formdata = new FormData();
    formdata.append('Method', 'retrievePlayerCharacterClassesByUserCNAndCharacterId');
    formdata.append('JSON', JSON.stringify(payload));
    
    jQuery.ajax({
        type: 'POST',
        url: "/Rest/playerCharacter.php",
        data: formdata,
        processData: false,
        contentType: false,
        success: function (response) {
            var post_return = JSON.parse(response);
            if(post_return.status == 'Success') {
                $('#Modal-editPlayerCharacter-form')[0].reset();
                $('#Modal-editPlayerCharacter-characterFirstName').val($('#Modal-editPlayerCharacter-selectCharacter').children("option:selected").attr('characterFirstName'));
                $('#Modal-editPlayerCharacter-characterLastName').val($('#Modal-editPlayerCharacter-selectCharacter').children("option:selected").attr('characterLastName'));
                post_return.result.forEach(function(element) {
                    $('#Modal-editPlayerCharacter-class' + element['classId'] + 'Checkbox').prop('checked', true);
                    $('#Modal-editPlayerCharacter-class' + element['classId'] + 'Level').val(element['currentLevel']);
                    $('#Modal-editPlayerCharacter-class' + element['classId'] + 'AverageILevel').val(element['averageILevel']);
                    $('#Modal-editPlayerCharacter-class' + element['classId'] + 'HasMeldsCheckbox').prop('checked', element['hasMeldsCheckbox']);
                });
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
};

$.updateEditPlayerCharacterModalData = function (selectedCharacter = -1){
    var payload = {};
    payload['playeruserCN'] = $.cookie("cn");

    formdata = new FormData();
    formdata.append('Method', 'retrievePlayerCharactersByUserCN');
    formdata.append('JSON', JSON.stringify(payload));

    jQuery.ajax({
        type: 'POST',
        url: "/Rest/playerCharacter.php",
        data: formdata,
        processData: false,
        contentType: false,
        success: function (response) {
            var post_return = JSON.parse(response);
            if(post_return.status == 'Success') {
                $('#Modal-editPlayerCharacter-selectCharacter').children().remove().end();
                post_return.result.forEach(element => $('#Modal-editPlayerCharacter-selectCharacter').append($('<option>', {value:element['id'], text:element['characterFirstName'] + ' ' + element['characterLastName'], characterFirstName:element['characterFirstName'], characterLastName:element['characterLastName']})));
                if(selectedCharacter == -1) {
                    $("#Modal-editPlayerCharacter-selectCharacter")[0].selectedIndex = 0;
                }
                else { $('#Modal-editPlayerCharacter-selectCharacter').val(selectedCharacter); }
                $.updateEditPlayerCharacterClassModalData();
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
};

$.updatePlayerCharacterData = function (){
    var payload = {};
    
    payload['playerCharacterId'] = $('#Modal-editPlayerCharacter-selectCharacter').val();
    
    $('input[id^="Modal-editPlayerCharacter"]').each(function( ) {
        if($( this ).attr('type') == 'checkbox') {
            payload[$( this ).attr('id')] = $( this ).is(':checked');
        } else {
            payload[$( this ).attr('id')] = $( this ).val();
        }
    });
    
    formdata = new FormData();
    formdata.append('Method', 'updateCharacterClassesByUserCNAndCharacterId');
    formdata.append('JSON', JSON.stringify(payload));
    
    jQuery.ajax({
        type: 'POST',
        url: "/Rest/playerCharacter.php",
        data: formdata,
        processData: false,
        contentType: false,
        success: function (response) {
            var post_return = JSON.parse(response);
            if(post_return.status == 'Success') {
                $.updateEditPlayerCharacterModalData(payload['playerCharacterId']);
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
};

$(document).ready(function(){
    $("#Modal-createPlayerCharacter-save").click(function(){
        var payload = {};
        
        $('input[id^="Modal-createPlayerCharacter"]').each(function( ) {
            if($( this ).attr('type') == 'checkbox') {
                payload[$( this ).attr('id')] = $( this ).is(':checked');
            } else {
                payload[$( this ).attr('id')] = $( this ).val();
            }
        });
        
        formdata = new FormData();
        formdata.append('Method', 'createPlayerCharacter');
        formdata.append('JSON', JSON.stringify(payload));
        
        jQuery.ajax({
            type: 'POST',
            url: "/Rest/playerCharacter.php",
            data: formdata,
            processData: false,
            contentType: false,
            success: function (response) {
                var post_return = JSON.parse(response);
                if(post_return.status == 'Success') {
                      $.updateEditPlayerCharacterModalData(post_return.result); 
                      $('#Modal-editPlayerCharacter-modal').modal('show'); 
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
    
    $('#Modal-editPlayerCharacter-selectCharacter').change(function() { $.updateEditPlayerCharacterClassModalData(); });
    $.updateEditPlayerCharacterModalData();
    
    $("#Modal-editPlayerCharacter-save").click(function(){
        var payload = {};
        
        payload['playerCharacterId'] = $('#Modal-editPlayerCharacter-selectCharacter').val();
        payload['characterFirstName'] = $("#Modal-editPlayerCharacter-characterFirstName").val();
        payload['characterLastName'] = $("#Modal-editPlayerCharacter-characterLastName").val();
        
        formdata = new FormData();
        formdata.append('Method', 'updatePlayerCharacterByUserCNAndCharacterId');
        formdata.append('JSON', JSON.stringify(payload));

        jQuery.ajax({
            type: 'POST',
            url: "/Rest/playerCharacter.php",
            data: formdata,
            processData: false,
            contentType: false,
            success: function (response) {
                var post_return = JSON.parse(response);
                if(post_return.status == 'Success') {
                    $.updatePlayerCharacterData();
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
    
    $("#Modal-editPlayerCharacter-delete").click(function(){
        $("#Modal-editPlayerCharacter-modal").modal('hide');
        $.confirmAction("About to delete a character(" + $('#Modal-editPlayerCharacter-selectCharacter :selected').text() + ")", function(){
            var payload = {};
            
            payload['playerCharacterId'] = $('#Modal-editPlayerCharacter-selectCharacter').val();
            
            formdata = new FormData();
            formdata.append('Method', 'deletePlayerCharacterByUserCNAndCharacterId');
            formdata.append('JSON', JSON.stringify(payload));
            
            jQuery.ajax({
                type: 'POST',
                url: "/Rest/playerCharacter.php",
                data: formdata,
                processData: false,
                contentType: false,
                success: function (response) {
                    var post_return = JSON.parse(response);
                    if(post_return.status == 'Success') {
                        $.updateEditPlayerCharacterModalData();
                        $("#Modal-editPlayerCharacter-modal").modal('show');
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
    });
});

