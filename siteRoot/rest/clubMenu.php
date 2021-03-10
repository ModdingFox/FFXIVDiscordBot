<?php
    require($_SERVER['DOCUMENT_ROOT'] . "/mySql.php");
    
    function getMenuItems($conn, $guildId, $menuType)
    {
	$json_result = json_decode('{}');
        
        $select_sql = 'SELECT menuItem, itemCost FROM discord.menuItems WHERE guildId = ? AND menuType = ? ORDER BY menuItem ASC';
	$select_stmt = $conn->prepare($select_sql);
	$select_stmt->bind_param("ss", $guildId, $menuType);
        
        if($select_stmt->execute() === TRUE)
        {
            $result = [];
            $sql_result = $select_stmt->get_result();
            while($row = $sql_result->fetch_assoc())
            {
                $rowData = json_decode('{}');
                $rowData->menuItem = $row['menuItem'];
                $rowData->itemCost = $row['itemCost'];
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
            if ($_GET['method'] === 'foodMenu')
	    {
                 $json_result = getMenuItems($conn, "806921306976419840", "foodMenu");
	    }
            elseif ($_GET['method'] === 'drinkMenu')
            {
                $json_result = getMenuItems($conn, "806921306976419840", "drinkMenu");
	    }
            elseif ($_GET['method'] === 'drinkSpecialMenu')
            {
                 $json_result = getMenuItems($conn, "806921306976419840", "drinkSpecialMenu");
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
