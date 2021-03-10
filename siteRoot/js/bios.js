function createBioCard(bioName, bioText, bioImage, channelId) {
    return '<div class="sm-3 mb-4 d-none biosCard ' + channelId + '"><div class="card" style="width: 18rem;">' +
           '    <img class="card-img-top" src="' + bioImage + '" alt="Card image cap">' +
           '    <div class="card-body">' +
           '        <h4 class="card-title">' + bioName + '</h4>' +
           '        <p class="card-text text-left">' + bioText.replace(/(?:\r\n|\r|\n)/g, '<br>') + '</p>' +
           '    </div>' +
           '</div></div>';
}

function displayBiosByChannelId(channelId) {
    $("a.biosButton").each(function removeClass(element){ $(this).removeClass("active") });
    $("div.biosCard").each(function addClass(element){ $(this).addClass("d-none") });

    $("a." + channelId).each(function addClass(element){ $(this).addClass("active") });
    $("div." + channelId).each(function removeClass(element){ $(this).removeClass("d-none") });
}

window.addEventListener("load", function(){
    jQuery.ajax({
        type: 'GET',
        url: "/rest/bios.php?method=getBio",
        processData: false,
        contentType: false,
        success: function (response) {
            var post_return = JSON.parse(response);
            if(post_return.status == 'Success') {
                jQuery.each(post_return.result, function() {
		    $("#biosCardDeck").append(createBioCard(this["bioName"], this["bioText"], this["bioImage"], this["channelId"]));
		    displayBiosByChannelId("816834122541432852");
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

