<?php
    require($_SERVER['DOCUMENT_ROOT'] . "/mySql.php");
    
    function insertApplication($conn, $question1, $question2, $question3, $question4, $question5, $question6, $question7, $question8, $question9, $question10, $question11, $question12, $question13)
    {
        $json_result = json_decode('{}');
        #Ignored user has special chars
        $insert_sql = 'INSERT INTO ClubSpectrum.applications (question1, question2, question3, question4, question5, question6, question7, question8, question9, question10, question11, question12, question13) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)';
        $insert_stmt = $conn->prepare($insert_sql);
	$insert_stmt->bind_param("sssssssssssss", $question1, $question2, $question3, $question4, $question5, $question6, $question7, $question8, $question9, $question10, $question11, $question12, $question13);
	
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
                isset($_POST['question2']) && !empty($_POST['question2']) &&
                isset($_POST['question3']) && !empty($_POST['question3']) &&
                isset($_POST['question4']) &&
                isset($_POST['question5']) && !empty($_POST['question5']) &&
                isset($_POST['question6']) &&
                isset($_POST['question8']) && !empty($_POST['question8']) &&
                isset($_POST['question9']) && !empty($_POST['question9']) &&
                isset($_POST['question10']) && !empty($_POST['question10']) &&
                isset($_POST['question11']) && !empty($_POST['question11']) &&
                isset($_POST['question12']) && !empty($_POST['question12']) &&
		isset($_POST['question13']) && !empty($_POST['question13'])
            )
	    {
       	        if (isset($_POST['question7Check1']) || isset($_POST['question7Check2']) || isset($_POST['question7Check3']) || isset($_POST['question7Check4']) || isset($_POST['question7Check5']) || isset($_POST['question7Check6']))
		{
		    $question7Array = [];
		    if (isset($_POST['question7Check1'])){ array_push($question7Array, "Dancer"); }
		    if (isset($_POST['question7Check2'])){ array_push($question7Array, "Courtesan"); }
		    if (isset($_POST['question7Check3'])){ array_push($question7Array, "Bartender"); }
		    if (isset($_POST['question7Check4'])){ array_push($question7Array, "Host/Hostess"); }
		    if (isset($_POST['question7Check5'])){ array_push($question7Array, "Bard"); }
		    if (isset($_POST['question7Check6'])){ array_push($question7Array, "Security"); }
		    $question7 = join(", ", $question7Array);
		    insertApplication($conn, $_POST['question1'], $_POST['question2'], $_POST['question3'], $_POST['question4'], $_POST['question5'], $_POST['question6'], $question7, $_POST['question8'], $_POST['question9'], $_POST['question10'], $_POST['question11'], $_POST['question12'], $_POST['question13']);
		    header('Location: /');
		}
		else
		{
		    $json_result->status = 'Error';
                    $json_result->error = 'No checked boxes in question 7';
		}
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
