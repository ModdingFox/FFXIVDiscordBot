$(document).ready(function(){
    if($.urlParam('resetToken') != 'undefined') {
        $('#Modal-userPasswordReset-modal').modal('show');
    }
    
    var userRegistration_constraints = {
        'Modal-userRegistration-username': {
            presence: { message: "^Username cannot be blank" },
            length: {
                minimum: 3,
                tooShort: "^Username must be at least 3 characters long",
                maximum: 20,
                tooLong: "^Username cannot be longer than 20 characters"
            },
            format: {
                pattern: "[a-z0-9]+",
                flags: "i",
                message: "^Username can only contain a-z and 0-9"
            }
        },
        'Modal-userRegistration-password': {
            presence: { message: "^Password cannot be blank" },
            length: {
                minimum: 5,
                message: "^Password must be at least 5 characters long"
            }
        },
        'Modal-userRegistration-confirmPassword': {
            presence: { message: "^Confirm password cannot be blank" },
            equality: {
                attribute: "Modal-userRegistration-password",
                message: "^The passwords do not match"
            }
        },
        'Modal-userRegistration-email': {
            presence: { message: "^Email cannot be blank" },
            email: true
        },
        'Modal-userRegistration-confirmEmail': {
            presence: { message: "^Confirm email cannot be blank" },
            equality: {
                attribute: "Modal-userRegistration-email",
                message: "^The emails do not match"
            }
        }
    };
    
    var userLogin_constraints = {
        'Modal-userLogin-username': {
            presence: { message: "^Username cannot be blank" },
            length: {
                minimum: 3,
                tooShort: "^Username must be at least 3 characters long",
                maximum: 20,
                tooLong: "^Username cannot be longer than 20 characters"
            },
            format: {
                pattern: "[a-z0-9]+",
                flags: "i",
                message: "^Username can only contain a-z and 0-9"
            }
        },
        'Modal-userLogin-password': {
            presence: { message: "^Password cannot be blank" },
            length: {
                minimum: 5,
                message: "^Password must be at least 5 characters long"
            }
        }
    };
    
    var userPasswordResetRequest_constraints = {
        'Modal-userPasswordResetRequest-username': {
            presence: { message: "^Username cannot be blank" },
            length: {
                minimum: 3,
                tooShort: "^Username must be at least 3 characters long",
                maximum: 20,
                tooLong: "^Username cannot be longer than 20 characters"
            },
            format: {
                pattern: "[a-z0-9]+",
                flags: "i",
                message: "^Username can only contain a-z and 0-9"
            }
        }
    };
    
    var userPasswordReset_constraints = {
        'Modal-userPasswordReset-password': {
            presence: { message: "^Password cannot be blank" },
            length: {
                minimum: 5,
                message: "^Password must be at least 5 characters long"
            }
        },
        'Modal-userPasswordReset-confirmPassword': {
            presence: { message: "^Confirm password cannot be blank" },
            equality: {
                attribute: "Modal-userPasswordReset-password",
                message: "^The passwords do not match"
            }
        }
    };
    
    $.addFormValidation(userRegistration_constraints, "Modal-userRegistration-form", "Modal-userRegistration-", "userRegistration", "/Rest/userAuthentication.php", function(){ $('#Modal-userRegistration-modal').modal('hide'); });
    $.addFormValidation(userLogin_constraints, "Modal-userLogin-form", "Modal-userLogin-", "userLogin", "/Rest/userAuthentication.php", function(){ location.reload(); });
    $.addFormValidation(userPasswordResetRequest_constraints, "Modal-userPasswordResetRequest-form", "Modal-userPasswordResetRequest-", "userPasswordResetTokenRequest", "/Rest/userAuthentication.php", function(){ $('#Modal-userPasswordResetRequest-modal').modal('hide'); });
    $.addFormValidation(userPasswordReset_constraints, "Modal-userPasswordReset-form", "Modal-userPasswordReset-", "userPasswordReset", "/Rest/userAuthentication.php?resetToken=" + $.urlParam('resetToken'), function(){ $('#Modal-userPasswordReset-modal').modal('hide'); });
});
