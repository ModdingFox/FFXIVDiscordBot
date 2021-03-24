$(document).ready(function() {
    $("#applicationForm").on('submit', function(e){
        e.preventDefault();
	var form = $(this);
	form.parsley().validate();
	if (form.parsley().isValid()){
	    $(this).unbind();
            $(this).submit();
        }
    });
});
