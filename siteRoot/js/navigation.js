function doNavigation() {
    $("a[id$='Button']").each(function removeClass(element){ $(this).removeClass("active") });
    $("div[id$='CardBody']").each(function addClass(element){ $(this).addClass("d-none") });

    if(window.location.hash) {
        if(window.location.hash.toLowerCase() == "#discord") {
            window.location = "https://discord.gg/32WZHSyxws";
        } else {
            button = $(window.location.hash + "Button");
            cardBody = $(window.location.hash + "CardBody");
            
            button.addClass("active");
            cardBody.removeClass("d-none");
         }
    } else {
       button = $("#homeButton");
       cardBody = $("#homeCardBody");

       button.addClass("active");
       cardBody.removeClass("d-none");
    }
}

window.addEventListener("load", function(){
    doNavigation();
});

window.addEventListener('popstate', function(){
    doNavigation();
});
