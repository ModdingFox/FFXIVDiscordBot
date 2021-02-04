$.addFormValidation = function(constraints, formName, inputPrefix, method, targetUrl, successFunction) {
    var form = document.querySelector("form#" + formName);
    form.addEventListener("submit", function(ev) {
        ev.preventDefault();
        handleFormSubmit(form);
    });
    
    var inputs = document.querySelectorAll("input, textarea, select")
    for (var i = 0; i < inputs.length; ++i) {
        inputs.item(i).addEventListener("change", function(ev) {
            var errors = validate(form, constraints) || {};
            showErrorsForInput(this, errors[this.name])
        });
    }
    
    function handleFormSubmit(form, input) {
        var errors = validate(form, constraints);
        showErrors(form, errors || {});
        if (!errors) {
            showSuccess();
        }
    }
    
    function showErrors(form, errors) {
        _.each(form.querySelectorAll("input[name], select[name]"), function(input) {
            showErrorsForInput(input, errors && errors[input.name]);
        });
    }
    
    function showErrorsForInput(input, errors) {
        var formGroup = closestParent(input.parentNode, "form-group"), messages = formGroup.querySelector(".messages");
        resetFormGroup(formGroup);
        if (errors) {
            formGroup.classList.add("has-error");
            _.each(errors, function(error) {
                addError(messages, error);
            });
        } else {
            formGroup.classList.add("has-success");
        }
    }
    
    function closestParent(child, className) {
        if (!child || child == document) {
            return null;
        }
        if (child.classList.contains(className)) {
            return child;
        } else {
            return closestParent(child.parentNode, className);
        }
    }
    
    function resetFormGroup(formGroup) {
        formGroup.classList.remove("has-error");
        formGroup.classList.remove("has-success");
        _.each(formGroup.querySelectorAll(".help-block.error"), function(el) {
            el.parentNode.removeChild(el);
        });
    }
    
    function addError(messages, error) {
        var block = document.createElement("p");
        block.classList.add("help-block");
        block.classList.add("error");
        block.innerText = error;
        messages.appendChild(block);
    }
    
    function showSuccess() {
        var payload = {};
        
        $('input[id^=' + inputPrefix + ']').each(function( ) {
            if($( this ).attr('type') == 'checkbox') {
                payload[$( this ).attr('id')] = $( this ).is(':checked');
            } else {
                payload[$( this ).attr('id')] = $( this ).val();
            }
        });
        
        formdata = new FormData();
        formdata.append('Method', method);
        formdata.append('JSON', JSON.stringify(payload));
        
        jQuery.ajax({
            type: 'POST',
            url: targetUrl,
            data: formdata,
            processData: false,
            contentType: false,
            success: function (response) {
                var post_return = JSON.parse(response);
                if(post_return.status == 'Success') {
                    successFunction();
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
    }
};
