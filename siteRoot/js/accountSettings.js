$(document).ready(function(){
    $("#Modal-accountSettings-discordLinkCodeRequest").click(function(){
        var payload = {};
        
        formdata = new FormData();
        formdata.append('Method', 'generateDiscordLinkToken');
        formdata.append('JSON', JSON.stringify(payload));
        
        jQuery.ajax({
            type: 'POST',
            url: "/Rest/discordLink.php",
            data: formdata,
            processData: false,
            contentType: false,
            success: function (response) {
                var post_return = JSON.parse(response);
                if(post_return.status == 'Success') {
                    $("#Modal-accountSettings-discordLinkCode").text("!register " + post_return.result);
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
    return;
});

