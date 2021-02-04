<div class="modal text-light" id="Modal-accountSettings-modal">
    <div class="modal-dialog">
        <div class="modal-content bg-dark">
            <div class="modal-header">
                <h4 class="modal-title">User Settings</h4>
                <button class="close" data-dismiss="modal" type="button">&times;</button>
            </div>
            <div class="modal-body">
                <form id="Modal-accountSettings-basicInfoForm">    
                    <div class="form-group">
                        <label for="Modal-accountSettings-username">Username:</label>
                        <input class="form-control" id="Modal-accountSettings-username" name="Modal-accountSettings-username" type="text" placeholder="">
                        <div class="messages"></div>
                    </div>
                    <div class="form-group">
                        <label for="Modal-accountSettings-email">Email:</label>
                        <input class="form-control" id="Modal-accountSettings-email" name="Modal-accountSettings-email" type="email" placeholder="">
                        <div class="messages"></div>
                    </div>
                    <div class="form-group">
                        <label for="Modal-accountSettings-firstName">First Name:</label>
                        <input class="form-control" id="Modal-accountSettings-firstName" type="text" placeholder="">
                    </div>
                    <div class="form-group">
                        <label for="Modal-accountSettings-lastName">Last Name:</label>
                        <input class="form-control" id="Modal-accountSettings-lastName" type="text" placeholder="">
                    </div>
                    <div class="form-group">
                        <label for="Modal-accountSettings-mobilePhoneNumber">Mobile Phone#:</label>
                        <input class="form-control" id="Modal-accountSettings-mobilePhoneNumber" type="text" placeholder="">
                    </div>
                    <div class="form-group">
                        <button class="btn btn-success" id="Modal-accountSettings_basicInfoSave" type="submit">Update Info</button>
                    </div>
                </form>
                <form id="Modal-accountSettings-passwordForm">
                    <div class="form-group">
                        <label for="Modal-accountSettings-password">Password:</label>
                        <input class="form-control" id="Modal-accountSettings-password" name="Modal-accountSettings-password" type="password" placeholder="">
                        <div class="messages"></div>
                    </div>
                    <div class="form-group">
                        <label for="Modal-accountSettings-confirmPassword">Confirm Password:</label>
                        <input class="form-control" id="Modal-accountSettings-confirmPassword" name="Modal-accountSettings-confirmPassword" type="password" placeholder="">
                        <div class="messages"></div>
                    </div>
                    <div class="form-group">
                        <button class="btn btn-success" id="Modal-accountSettings-passowrdSave" type="submit">Update Password</button>
                    </div>
                </form>
                <form id="Modal-accountSettings-profileImageForm">
                    <div class="form-group">
                        <label for="Modal-accountSettings-profileImage">Profile Image:</label>
                        <input type="file" id="Modal-accountSettings-profileImage">
                    </div>
                    <div class="form-group">
                        <button class="btn btn-success" id="Modal-accountSettings-profileImageSave" type="submit">Update Profile Image</button>
                    </div>
                </form>
                <div>
                    <label for="Modal-accountSettings-discordLinkCode">Discord Link Code:</label>
                    <p id="Modal-accountSettings-discordLinkCode">Click "Request Discord Link Code" take the generated command/code and paste it into discord</p>
                    <button class="btn btn-success" id="Modal-accountSettings-discordLinkCodeRequest" type="button">Request Discord Link Code</button>
                </div>
                <div class="modal-footer">
                    <div class="form-group">
                        <button class="btn btn-danger" data-dismiss="modal" type="button">Close</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

