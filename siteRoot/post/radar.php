<?php
    require($_SERVER['DOCUMENT_ROOT'] . "/mySql.php");
    
    function insertEntry($conn, $name, $world)
    {
        $json_result = json_decode('{}');
        $insert_sql = 'INSERT INTO ClubSpectrum.radar (name, world, inRangeTime) VALUES (?, ?, NOW())';
        $insert_stmt = $conn->prepare($insert_sql);
	$insert_stmt->bind_param("ss", $name, $world);
	
        if($insert_stmt->execute() === TRUE)
        {
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
    
    function updateEntry($conn, $name, $world)
    {
        $json_result = json_decode('{}');
        $update_sql = 'UPDATE ClubSpectrum.radar SET outOfRangeTime = NOW() WHERE name = ? AND world = ?';
        $update_stmt = $conn->prepare($update_sql);
        $update_stmt->bind_param("ss", $name, $world);
        
        if($update_stmt->execute() === TRUE)
        {
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
    
    if ($conn->connect_error)
    {
        $json_result->status = 'Error';
        $json_result->error = $conn->connect_error;
    }
    else
    {
        if ($_SERVER['REQUEST_METHOD'] === 'POST')
	{
		$json = file_get_contents('php://input');
		$data = json_decode($json);

		$addPlayers = $data->addPlayers;
                $removePlayers = $data->removePlayers;

		foreach($addPlayers as $value)
		{
                    echo $value;
                    $json_result->status = $value . " - ";
	            $json_result = insertEntry($conn, $value, "");
		    if($json_result->status == 'Error')
		    {
                        break;
                    }
                }

		if($json_result->status != 'Error')
                {
                    foreach($removePlayers as $value)
		    {
                        $json_result = updateEntry($conn, $value, "");
                        if($json_result->status == 'Error')
                        {
                            break;
			}
                    }
                }
        }
        else
        {
            $json_result->status = 'Error';
            $json_result->error = 'No http method for request found';
        }
    }
#    echo json_encode($json_result);
?>
