$.confirmAction = function (warning, acceptFunction){
    $('#Modal-confirmAction-text').text(warning);
    $('#Modal-confirmAction-save').click(function(){ acceptFunction(); });
    $('#Modal-confirmAction-modal').modal('show');
};
