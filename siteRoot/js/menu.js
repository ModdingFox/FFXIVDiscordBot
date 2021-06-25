window.addEventListener("load", function(){
    jQuery.ajax({
        type: 'GET',
        url: "rest/clubMenu.php?method=drinkMenu",
        processData: false,
        contentType: false,
        success: function (response) {
            var post_return = JSON.parse(response);
            if(post_return.status == 'Success') {
                jQuery.each(post_return.result, function() {
                    $("#drinkMenu").append("<h5>" + this["menuItem"] + " - " + this["itemCost"] + " gil</h5>");
                });
            }
            else if (post_return.status == 'Warning') {
                console.log(post_return.status + " " + post_return.warning);
            }
            else if (post_return.status == 'Error') {
                console.log(post_return.status + " " + post_return.error);
            }
            else { console.log("Did not get status from server"); }
        }
    });

    jQuery.ajax({
        type: 'GET',
        url: "rest/clubMenu.php?method=drinkSpecialMenu",
        processData: false,
        contentType: false,
        success: function (response) {
            var post_return = JSON.parse(response);
            if(post_return.status == 'Success') {
                jQuery.each(post_return.result, function() {
                    $("#drinkSpecialMenu").append("<h5>" + this["menuItem"] + " - " + this["itemCost"] + " gil</h5>");
                });
            }
            else if (post_return.status == 'Warning') {
                console.log(post_return.status + " " + post_return.warning);
            }
            else if (post_return.status == 'Error') {
                console.log(post_return.status + " " + post_return.error);
            }
            else { console.log("Did not get status from server"); }
        }
    });

    jQuery.ajax({
        type: 'GET',
        url: "rest/clubMenu.php?method=foodMenu",
        processData: false,
        contentType: false,
        success: function (response) {
            var post_return = JSON.parse(response);
            if(post_return.status == 'Success') {
                jQuery.each(post_return.result, function() {
                    $("#foodMenu").append("<h5>" + this["menuItem"] + " - " + this["itemCost"] + " gil</h5>");
                });
            }
            else if (post_return.status == 'Warning') {
                console.log(post_return.status + " " + post_return.warning);
            }
            else if (post_return.status == 'Error') {
                console.log(post_return.status + " " + post_return.error);
            }
            else { console.log("Did not get status from server"); }
        }
    });
});
