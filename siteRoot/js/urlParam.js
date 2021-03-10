$.urlParam = function(name){
	var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if(results == null) { return 'undefined'; }
	else { return results[1] || 0; }
}

