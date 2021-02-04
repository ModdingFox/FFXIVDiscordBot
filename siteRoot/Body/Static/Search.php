<label for="Body-Static_Search-classSelect">Classes:</label>
<select id="Body-Static_Search-classSelect" class="bg-dark text-light" multiple>
    <?php
        require('DB_Connection.php');

        $select_options = 'SELECT id, name FROM ffxivReference.classes';
        $select_options_stmt = $conn->prepare($select_options);
        
        if($select_options_stmt->execute() === TRUE)
        {
            $result = $select_options_stmt->get_result();
            while($row = $result->fetch_assoc())
            {
                echo '<option value="' . $row['id'] . '">' . $row['name'] . '</option>';
            }
        }
    ?>
</select>
<label for="Body-Static_Search-levelSelect">Level:</label>
<select id="Body-Static_Search-levelSelect" class="bg-dark text-light" multiple>
    <?php
        require('DB_Connection.php');

        $select_options = 'SELECT distinct currentLevel FROM ffxivPlayers.characterClasses ORDER BY currentLevel ASC';
        $select_options_stmt = $conn->prepare($select_options);

        if($select_options_stmt->execute() === TRUE)
        {
            $result = $select_options_stmt->get_result();
            while($row = $result->fetch_assoc())
            {
                echo '<option value="' . $row['currentLevel'] . '">' . $row['currentLevel'] . '</option>';
            }
        }
    ?>
</select>
<label for="Body-Static_Search-iLevelSelect">Item Level:</label>
<select id="Body-Static_Search-iLevelSelect" class="bg-dark text-light" multiple>
    <?php
        require('DB_Connection.php');

        $select_options = 'SELECT distinct averageILevel FROM ffxivPlayers.characterClasses ORDER BY averageILevel ASC';
        $select_options_stmt = $conn->prepare($select_options);

        if($select_options_stmt->execute() === TRUE)
        {
            $result = $select_options_stmt->get_result();
            while($row = $result->fetch_assoc())
            {
                echo '<option value="' . $row['averageILevel'] . '">' . $row['averageILevel'] . '</option>';
            }
        }
    ?>
</select>
<label for="Body-Static_Search-hasSavageExperience">Savage Experience</label>
<select id="Body-Static_Search-hasSavageExperience" class="bg-dark text-light" multiple>
    <option value="0">No</option>
    <option value="1">Yes</option>
</select>
<label for="Body-Static_Search-hasRaidExperience">Raid Experience</label>
<select id="Body-Static_Search-hasRaidExperience" class="bg-dark text-light" multiple>
    <option value="0">No</option>
    <option value="1">Yes</option>
</select>
<label for="Body-Static_Search-hasMeldsCheckbox">Melds</label>
<select id="Body-Static_Search-hasMeldsCheckbox" class="bg-dark text-light" multiple>
    <option value="0">No</option>
    <option value="1">Yes</option>
</select>
<label for="Body-Static_Search-daySelect">Avaliability:</label>
<select id="Body-Static_Search-daySelect" class="bg-dark text-light" multiple>
    <option value="0">Sunday</option>
    <option value="1">Monday</option>
    <option value="2">Tuesday</option>
    <option value="3">Wednesday</option>
    <option value="4">Thursday</option>
    <option value="5">Friday</option>
    <option value="6">Saturday</option>
</select>
<button class="btn btn-success" id="Body-Static_Search-search" type="button">Search</button>
<table id="Body-Static_Search-playerTable" class="table table-bordered table-sm bg-dark text-light" cellspacing="0" width="100%">
    <thead>
        <tr>
            <th class="th-sm">characterName</th>
            <th class="th-sm">hasSavageExperience</th>
            <th class="th-sm">hasRaidExperience</th>
            <th class="th-sm">className</th>
            <th class="th-sm">currentLevel</th>
            <th class="th-sm">averageILevel</th>
            <th class="th-sm">hasMeldsCheckbox</th>
            <th class="th-sm">playerAvaliablilty</th>
        </tr>
    </thead>
    <tbody>
    </tbody>
</table>
