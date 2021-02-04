<div class="modal text-light" id="Modal-createPlayerCharacter-modal">
    <div class="modal-dialog">
        <div class="modal-content bg-dark">
            <div class="modal-header">
                <h4 class="modal-title">Add Character</h4>
                <button class="close" data-dismiss="modal" type="button">&times;</button>
            </div>
            <div class="modal-body">
                <label for="Modal-createPlayerCharacter-characterFirstName">First Name:</label>
                <input class="form-control" id="Modal-createPlayerCharacter-characterFirstName" type="text" placeholder="">
                <label for="Modal-createPlayerCharacter-characterLastName">Last Name:</label>
                <input class="form-control" id="Modal-createPlayerCharacter-characterLastName" type="text" placeholder="">
            </div>
            <div class="modal-footer">
                <button class="btn btn-success" data-dismiss="modal" id="Modal-createPlayerCharacter-save" type="button">Save</button>
                <button class="btn btn-danger" data-dismiss="modal" type="button">Close</button>
            </div>
        </div>
    </div>
</div>
<div class="modal text-light" id="Modal-editPlayerCharacter-modal">
    <div class="modal-dialog modal-full">
        <div class="modal-content bg-dark">
            <div class="modal-header">
                <h4 class="modal-title">Edit Character</h4>
                <button class="close" data-dismiss="modal" type="button">&times;</button>
            </div>
            <div class="modal-body">
                <div>
                    <label for="Modal-editPlayerCharacter-selectCharacter">Selected Character:</label>
                    <select id="Modal-editPlayerCharacter-selectCharacter" class="bg-dark text-light"></select>
                </div>
                <form id="Modal-editPlayerCharacter-form">
                    <div>
                        <label for="Modal-editPlayerCharacter-characterFirstName">Character First Name:</label>
                        <input class="form-control" id="Modal-editPlayerCharacter-characterFirstName" type="text" placeholder="">
                        <label for="Modal-editPlayerCharacter-characterLastName">Character Last Name:</label>
                        <input class="form-control" id="Modal-editPlayerCharacter-characterLastName" type="text" placeholder="">
                        
                        <label>Class Information:</label>
                        <div class="card-group">
                            <?php
                                require 'DB_Connection.php';
                                
                                if ($conn->connect_error) {
                                    die("Connection failed: " . $conn->connect_error);
                                }
                                
                                $sql = "SELECT id, name FROM ffxivReference.classes";
                                $result = $conn->query($sql);
                                
                                while($row = mysqli_fetch_array($result)) {
                                    echo '<div class="mx-auto" style="width:250px">';
                                    echo '    <div class="card bg-dark">';
                                    echo '        <div class="card-header" id="Modal-editPlayerCharacter-class' . $row["id"] . 'CardHeading">';
                                    echo '            <label for="Modal-editPlayerCharacter-class' . $row["id"] . 'Checkbox">';
                                    echo '                <input type="checkbox" class="form-check-input" id="Modal-editPlayerCharacter-class' . $row["id"] . 'Checkbox">';
                                    echo                  $row["name"];
                                    echo '            </label>';
                                    echo '        </div>';
                                    echo '        <div id="Modal-editPlayerCharacter-class' . $row["id"] . 'CardModal">';
                                    echo '            <div class="card-Modal form-group ">';
                                    echo '                <label for="Modal-editPlayerCharacter-class' . $row["id"] . 'Level">Level</label>';
                                    echo '                <input class="form-control" id="Modal-editPlayerCharacter-class' . $row["id"] . 'Level" type="text" placeholder="1">';
                                    echo '                <label for="Modal-editPlayerCharacter-class' . $row["id"] . 'AverageILevel">ILevel</label>';
                                    echo '                <input class="form-control" id="Modal-editPlayerCharacter-class' . $row["id"] . 'AverageILevel" type="text" placeholder="1">';
                                    echo '                <input type="checkbox" class="form-check-input" id="Modal-editPlayerCharacter-class' . $row["id"] . 'HasMeldsCheckbox">';
                                    echo '                <label class="form-check-label" for="Modal-editPlayerCharacter-class' . $row["id"] . 'HasMeldsCheckbox">Has melds</label>';
                                    echo '            </div>';
                                    echo '        </div>';
                                    echo '    </div>';
                                    echo '</div>';
                                }
                                
                                $conn->close();
                            ?>
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button class="btn btn-success" id="Modal-editPlayerCharacter-save" type="button">Save</button>
                <button class="btn btn-danger" id="Modal-editPlayerCharacter-delete" type="button">Delete</button>
                <button class="btn btn-danger" data-dismiss="modal" type="button">Close</button>
            </div>
        </div>
    </div>
</div>
