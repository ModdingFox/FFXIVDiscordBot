<?php
    require($_SERVER['DOCUMENT_ROOT'] . "/mySql.php");
    
    function getBio($conn, $guildId)
    {
        $json_result = json_decode('{}');
        #Ignored user has special chars
        $select_sql = 'SELECT distinct bM.discordUserId, bM.channelId, b.bioName, b.bioText, b.bioImage FROM discord.bios b JOIN discord.biosMessages bM ON b.guildId = bM.guildId AND b.discordUserId = bM.discordUserId WHERE b.guildId = ? AND b.discordUserId != "184208290685648897" ORDER BY b.bioName ASC';
        $select_stmt = $conn->prepare($select_sql);
        $select_stmt->bind_param("s", $guildId);
        
        if($select_stmt->execute() === TRUE)
        {
            $result = [];
            $sql_result = $select_stmt->get_result();
            while($row = $sql_result->fetch_assoc())
            {
		$rowData = json_decode('{}');
                $rowData->channelId = $row['channelId'];
                $rowData->bioName = $row['bioName'];
                $rowData->bioText = $row['bioText'];
		$rowData->bioImage = $row['bioImage'];
		array_push($result, $rowData);
	    }
            $json_result->status = 'Success';
            $json_result->result = $result;
        }
        else
        {
            $json_result->status = 'Error';
            $json_result->error = $conn->error;
        }
        
        return $json_result;
    }
    
    $json_result = json_decode('{}');
    if ($conn->connect_error)
    {
        $json_result->status = 'Error';
        $json_result->error = $conn->connect_error;
    }
    else
    {
        if ($_SERVER['REQUEST_METHOD'] === 'GET')
        {
            if ($_GET['method'] === 'getBio')
            {
                 $json_result = getBio($conn, "806921306976419840");
            }
            else
            {
                $json_result->status = 'Error';
                $json_result->error = 'No method for request found';
            }
        }
        else
        {
            $json_result->status = 'Error';
            $json_result->error = 'No http method for request found';
        }
    }
    echo json_encode($json_result);
?>
