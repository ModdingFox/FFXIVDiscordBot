window.addEventListener("load", function(){
    if(location.pathname.substring(location.pathname.lastIndexOf("/") + 1) == "indexVIP.php") {
        jQuery.ajax({
            type: 'GET',
            url: "rest/clubMenu.php?method=drinkVIPMenu",
            processData: false,
            contentType: false,
            success: function (response) {
                var post_return = JSON.parse(response);
                if(post_return.status == 'Success') {
                    jQuery.each(post_return.result, function() {
                        $("#vipDrinkMenu").append("<h5>" + this["menuItem"] + " - " + this["itemCost"] + " gil</h5>");
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
            url: "rest/clubMenu.php?method=drinkSpecialVIPMenu",
            processData: false,
            contentType: false,
            success: function (response) {
                var post_return = JSON.parse(response);
                if(post_return.status == 'Success') {
                    jQuery.each(post_return.result, function() {
                        $("#vipDrinkSpecialMenu").append("<h5>" + this["menuItem"] + " - " + this["itemCost"] + " gil</h5>");
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
            url: "rest/clubMenu.php?method=foodVIPMenu",
            processData: false,
            contentType: false,
            success: function (response) {
                var post_return = JSON.parse(response);
                if(post_return.status == 'Success') {
                    jQuery.each(post_return.result, function() {
                        $("#vipFoodMenu").append("<h5>" + this["menuItem"] + " - " + this["itemCost"] + " gil</h5>");
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
    }
});
