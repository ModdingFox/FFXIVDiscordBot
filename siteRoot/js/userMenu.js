$(document).ready(function(){
    $("#Navbar-userMenu-a").click(function(){
        var payload = {};
        
        formdata = new FormData();
        formdata.append('Method', 'userLogout');
        formdata.append('JSON', JSON.stringify(payload));

        jQuery.ajax({
            type: 'POST',
            url: "/Rest/userAuthentication.php",
            data: formdata,
            processData: false,
            contentType: false,
            success: function (response) {
                var post_return = JSON.parse(response);
                if(post_return.status == 'Success') {
                    location.reload(); 
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
