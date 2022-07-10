<?php
    require($_SERVER['DOCUMENT_ROOT'] . "/mySql.php");
    
    function getApplication($conn, $applicationId)
    {
	$json_result = json_decode('{}');
        
        $select_sql = 'SELECT question1, question2, question3, question4, question5, question6, question7, question8, question9, question10, question11 FROM ClubSpectrum.applications WHERE id = ?';
	$select_stmt = $conn->prepare($select_sql);
	$select_stmt->bind_param("s", $applicationId);
        
        if($select_stmt->execute() === TRUE)
        {
            $result = json_decode('{}');
            $sql_result = $select_stmt->get_result();
            while($row = $sql_result->fetch_assoc())
            {
                $rowData = json_decode('{}');
                $rowData->question1 = $row['question1'];
                $rowData->question2 = $row['question2'];
                $rowData->question3 = $row['question3'];
                $rowData->question4 = $row['question4'];
                $rowData->question5 = $row['question5'];
                $rowData->question6 = $row['question6'];
                $rowData->question7 = $row['question7'];
                $rowData->question8 = $row['question8'];
                $rowData->question9 = $row['question9'];
                $rowData->question10 = $row['question10'];
                $rowData->question11 = $row['question11'];
                $result = $rowData;
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
            if ($_GET['method'] === 'getApplication' && isset($_GET['applicationId']) && ! empty($_GET['applicationId']))
	    {
                 $json_result = getApplication($conn, $_GET['applicationId']);
	    }
            else
            {
                $json_result->status = 'Error';
                $json_result->error = 'Invalid Method';
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
