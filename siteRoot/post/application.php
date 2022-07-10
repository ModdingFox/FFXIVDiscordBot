<?php
    require($_SERVER['DOCUMENT_ROOT'] . "/mySql.php");
    
    function insertApplication($conn, $guildId, $question1, $question2, $question3, $question4, $question5, $question6, $question7, $question8, $question9, $question10, $question11)
    {
        $json_result = json_decode('{}');
        #Ignored user has special chars
        $insert_sql = 'INSERT INTO ClubSpectrum.applications (guildId, question1, question2, question3, question4, question5, question6, question7, question8, question9, question10, question11) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)';
        $insert_stmt = $conn->prepare($insert_sql);
	$insert_stmt->bind_param("ssssssssssss", $guildId, $question1, $question2, $question3, $question4, $question5, $question6, $question7, $question8, $question9, $question10, $question11);
	
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
    
    if ($conn->connect_error)
    {
        $json_result->status = 'Error';
        $json_result->error = $conn->connect_error;
    }
    else
    {
        if ($_SERVER['REQUEST_METHOD'] === 'POST')
	{
	    if (
                isset($_POST['question1']) && !empty($_POST['question1']) &&
                isset($_POST['question2']) &&
                isset($_POST['question3']) && !empty($_POST['question3']) &&
		isset($_POST['question4']) &&
		isset($_POST['question5']) && !empty($_POST['question5']) &&
                isset($_POST['question6']) && !empty($_POST['question6']) &&
                isset($_POST['question7']) && !empty($_POST['question7']) &&
                isset($_POST['question8']) && !empty($_POST['question8']) &&
                isset($_POST['question9']) && !empty($_POST['question9']) &&
                isset($_POST['question10']) && !empty($_POST['question10']) &&
		isset($_POST['question11']) && !empty($_POST['question11'])
            )
	    {
                $question5 = join(", ", $_POST['question5']);
		insertApplication($conn, '806921306976419840', $_POST['question1'], $_POST['question2'], $_POST['question3'], $_POST['question4'], $question5, $_POST['question6'], $_POST['question7'], $_POST['question8'], $_POST['question9'], $_POST['question10'], $_POST['question11']);
                header('Location: /');
            }
	    else
	    {
                $json_result->status = 'Error';
		$json_result->error = 'Missing Required Fields';
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
