<div class="modal text-light" id="Modal-userRegistration-modal">
    <div class="modal-dialog">
        <div class="modal-content bg-dark">
            <div class="modal-header">
                <h4 class="modal-title">User Registration</h4>
                <button class="close" data-dismiss="modal" type="button">&times;</button>
            </div>
            <form id="Modal-userRegistration-form">
                <div class="modal-body">
                    <div class="form-group">
                        <label for="Modal-userRegistration-username">Username:</label>
                        <input class="form-control" id="Modal-userRegistration-username" name="Modal-userRegistration-username" type="text" placeholder="">
                        <div class="messages"></div>
                    </div>
                    <div class="form-group">
                        <label for="Modal-userRegistration-password">Password:</label>
                        <input class="form-control" id="Modal-userRegistration-password" name="Modal-userRegistration-password" type="password" placeholder="">
                        <div class="messages"></div>
                    </div>
                    <div class="form-group">
                        <label for="Modal-userRegistration-confirmPassword">Confirm Password:</label>
                        <input class="form-control" id="Modal-userRegistration-confirmPassword" name="Modal-userRegistration-confirmPassword" type="password" placeholder="">
                        <div class="messages"></div>
                    </div>
                    <div class="form-group">
                        <label for="Modal-userRegistration-email">Email:</label>
                        <input class="form-control" id="Modal-userRegistration-email" name="Modal-userRegistration-email" type="email" placeholder="">
                        <div class="messages"></div>
                    </div>
                    <div class="form-group">
                        <label for="Modal-userRegistration-confirmEmail">Confirm Email:</label>
                        <input class="form-control" id="Modal-userRegistration-confirmEmail" name="Modal-userRegistration-confirmEmail" type="email" placeholder="">
                        <div class="messages"></div>
                    </div>
                    <div class="form-group">
                        <label for="Modal-userRegistration-firstName">First Name:</label>
                        <input class="form-control" id="Modal-userRegistration-firstName" type="text" placeholder="">
                    </div>
                    <div class="form-group">
                        <label for="Modal-userRegistration-lastName">Last Name:</label>
                        <input class="form-control" id="Modal-userRegistration-lastName" type="text" placeholder="">
                    </div>
                    <div class="modal-footer">
                        <div class="form-group">
                            <button class="btn btn-success" id="Modal-userRegistration-save" type="submit">Save</button>
                            <button class="btn btn-danger" data-dismiss="modal" type="button">Close</button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
<div class="modal text-light" id="Modal-userLogin-modal">
    <div class="modal-dialog">
        <div class="modal-content bg-dark">
            <div class="modal-header">
                <h4 class="modal-title">User Login</h4>
                <button class="close" data-dismiss="modal" type="button">&times;</button>
            </div>
            <form id="Modal-userLogin-form">
                <div class="modal-body">
                    <div class="form-group">
                        <label for="Modal-userLogin-username">Username:</label>
                        <input class="form-control" id="Modal-userLogin-username" name="Modal-userLogin-username" type="text" placeholder="">
                        <div class="messages"></div>
                    </div>
                    <div class="form-group">
                        <label for="Modal-userLogin-password">Password:</label>
                        <input class="form-control" id="Modal-userLogin-password" name="Modal-userLogin-password" type="password" placeholder="">
                        <div class="messages"></div>
                    </div>
                </div>
                <div class="modal-footer">
                    <div class="form-group w-100 d-flex">
                        <button class="btn btn-warning mr-auto" data-dismiss="modal" data-target="#Modal-userPasswordResetRequest-modal" data-toggle="modal" type="button">Reset Password</button>
                        <button class="btn btn-success" id="Modal-userLogin-save" type="submit">Login</button>
                        <button class="btn btn-danger" data-dismiss="modal" type="button">Close</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
<div class="modal text-light" id="Modal-userPasswordResetRequest-modal">
    <div class="modal-dialog">
        <div class="modal-content bg-dark">
            <div class="modal-header">
                <h4 class="modal-title">Request Password Reset</h4>
                <button class="close" data-dismiss="modal" type="button">&times;</button>
            </div>
            <form id="Modal-userPasswordResetRequest-form">
                <div class="modal-body">
                    <div class="form-group">
                        <label for="Modal-userPasswordResetRequest-username">Username:</label>
                        <input class="form-control" id="Modal-userPasswordResetRequest-username" name="Modal-userPasswordResetRequest-username" type="text" placeholder="">
                        <div class="messages"></div>
                    </div>
                </div>
                <div class="modal-footer">
                    <div class="form-group">
                        <button class="btn btn-success" id="Modal-userPasswordResetRequest-save" type="submit">Request Reset Password</button>
                        <button class="btn btn-danger" data-dismiss="modal" type="button">Close</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
<div class="modal text-light" id="Modal-userPasswordReset-modal">
    <div class="modal-dialog">
        <div class="modal-content bg-dark">
            <div class="modal-header">
                <h4 class="modal-title">Password Reset</h4>
                <button class="close" data-dismiss="modal" type="button">&times;</button>
            </div>
            <form id="Modal-userPasswordReset-form">
                <div class="modal-body">
                    <div class="form-group">
                        <label for="Modal-userPasswordReset-password">Password:</label>
                        <input class="form-control" id="Modal-userPasswordReset-password" name="Modal-userPasswordReset-password" type="password" placeholder="">
                        <div class="messages"></div>
                    </div>
                    <div class="form-group">
                        <label for="Modal-userPasswordReset-confirmPassword">Confirm Password:</label>
                        <input class="form-control" id="Modal-userPasswordReset-confirmPassword" name="Modal-userPasswordReset-confirmPassword" type="password" placeholder="">
                        <div class="messages"></div>
                    </div>
                    <div class="modal-footer">
                        <div class="form-group">
                            <button class="btn btn-success" id="Modal-userPasswordReset-save" type="submit">Save</button>
                            <button class="btn btn-danger" data-dismiss="modal" type="button">Close</button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
