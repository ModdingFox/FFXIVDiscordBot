window.addEventListener("load", function(){
    jQuery.ajax({
        type: 'GET',
        url: "/rest/applications.php?method=getApplication&applicationId=" + $.urlParam('applicationId'),
        processData: false,
        contentType: false,
        success: function (response) {
            var post_return = JSON.parse(response);
            if(post_return.status == 'Success') {
                $("#question1").html(post_return.result["question1"]);
                $("#question2").html(post_return.result["question2"]);
                $("#question3").html(post_return.result["question3"]);
                $("#question4").html(post_return.result["question4"]);
                $("#question5").html(post_return.result["question5"]);
                $("#question6").html(post_return.result["question6"]);
                $("#question7").html(post_return.result["question7"]);
                $("#question8").html(post_return.result["question8"]);
                $("#question9").html(post_return.result["question9"]);
                $("#question10").html(post_return.result["question10"]);
                $("#question11").html(post_return.result["question11"]);
                $("#question12").html(post_return.result["question12"]);
                $("#question13").html(post_return.result["question13"]);
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

function getPreviousApplication() {
    window.location.assign('/staff.php/?applicationId=' + (parseInt($.urlParam('applicationId')) - 1) + '#application');
}

function getNextApplication() {
    window.location.assign('/staff.php/?applicationId=' + (parseInt($.urlParam('applicationId')) + 1) + '#application');
}
