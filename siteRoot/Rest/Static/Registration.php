<?php
    require('/var/www/html/Utility/login.php');
    require('/var/www/html/DB_Connection.php');
    
    $json_result = json_decode('{}');
    
    if ($conn->connect_error)
    {
        $json_result->status = 'Error';
        $json_result->error = $conn->connect_error;
    }
    else
    {
        if($isLoggedIn)
        {
            if ($_SERVER['REQUEST_METHOD'] === 'POST')
            {
                $json_payload = json_decode($_POST['JSON'], true);

                if($_POST['Method'] === 'updateRegistration')
                {
                    $delete_sql = 'DELETE FROM ffxivStatic.playerRegistrationStatic WHERE userCN = ?';
                    $delete_stmt = $conn->prepare($delete_sql);
                    
                    $s_userCN = $usercn;
                    
                    $delete_stmt->bind_param("s", $s_userCN);
                    
                    if($delete_stmt->execute() === TRUE)
                    {
                        $insert_sql = 'INSERT INTO ffxivStatic.playerRegistrationStatic (userCN, hasSavageExperience, hasRaidExperience, sunday, monday, tuesday, wednesday, thursday, friday, saturday) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)';
                        $insert_stmt = $conn->prepare($insert_sql);
                        
                        $s_userCN = $usercn;
                        $i_hasSavageExperience = ($json_payload['hasSavageExperience'] == 1)?(1):(0);
                        $i_hasRaidExperience = ($json_payload['hasRaidExperience'] == 1)?(1):(0);
                        $i_playerAvaliabliltySunday = ($json_payload['playerAvaliabliltySunday'] == 1)?(1):(0);
                        $i_playerAvaliabliltyMonday = ($json_payload['playerAvaliabliltyMonday'] == 1)?(1):(0);
                        $i_playerAvaliabliltyTuesday = ($json_payload['playerAvaliabliltyTuesday'] == 1)?(1):(0);
                        $i_playerAvaliabliltyWednesday = ($json_payload['playerAvaliabliltyWednesday'] == 1)?(1):(0);
                        $i_playerAvaliabliltyThursday = ($json_payload['playerAvaliabliltyThursday'] == 1)?(1):(0);
                        $i_playerAvaliabliltyFriday = ($json_payload['playerAvaliabliltyFriday'] == 1)?(1):(0);
                        $i_playerAvaliabliltySaturday = ($json_payload['playerAvaliabliltySaturday'] == 1)?(1):(0);
                        
                        $insert_stmt->bind_param("siiiiiiiii", $s_userCN, $i_hasSavageExperience, $i_hasRaidExperience, $i_playerAvaliabliltySunday, $i_playerAvaliabliltyMonday, $i_playerAvaliabliltyTuesday, $i_playerAvaliabliltyWednesday, $i_playerAvaliabliltyThursday, $i_playerAvaliabliltyFriday, $i_playerAvaliabliltySaturday);
                        
                        if($insert_stmt->execute() === TRUE) { $json_result->status = 'Success'; }
                        else
                        {
                            $json_result->status = 'Error';
                            $json_result->error = $conn->error;
                        }
                    }
                    else
                    {
                        $json_result->status = 'Error';
                        $json_result->error = $conn->error;
                    }
                }
                elseif($_POST['Method'] === 'deleteRegistration')
                {
                    $delete_sql = 'DELETE FROM ffxivStatic.playerRegistrationStatic WHERE userCN = ?';
                    $delete_stmt = $conn->prepare($delete_sql);
                    
                    $s_userCN = $usercn;
                    
                    $delete_stmt->bind_param("s", $s_userCN);
                    
                    if($delete_stmt->execute() === TRUE) { $json_result->status = 'Success'; }
                    else
                    {
                        $json_result->status = 'Error';
                        $json_result->error = $conn->error;
                    }

                }
                elseif($_POST['Method'] === 'viewRegistration')
                {
                    if(isset($json_payload['playeruserCN']))
                    {
                        $select_sql = 'SELECT hasSavageExperience, hasRaidExperience, sunday, monday, tuesday, wednesday, thursday, friday, saturday FROM ffxivStatic.playerRegistrationStatic WHERE userCN = ?';
                        $select_stmt = $conn->prepare($select_sql);
                        
                        $s_userCN = $json_payload['playeruserCN'];
                        
                        $select_stmt->bind_param("s", $s_userCN);
                        
                        if($select_stmt->execute() === TRUE)
                        {
                            $result = json_decode('{}');;
                            $sql_result = $select_stmt->get_result();
                            while($row = $sql_result->fetch_assoc())
                            {
                                $result->hasSavageExperience = $row['hasSavageExperience'];
                                $result->hasRaidExperience = $row['hasRaidExperience'];
                                $result->sunday = $row['sunday'];
                                $result->monday = $row['monday'];
                                $result->tuesday = $row['tuesday'];
                                $result->wednesday = $row['wednesday'];
                                $result->thursday = $row['thursday'];
                                $result->friday = $row['friday'];
                                $result->saturday = $row['saturday'];
                            }
                            $json_result->status = 'Success';
                            $json_result->result = $result;
                        }
                        else
                        {
                            $json_result->status = 'Error';
                            $json_result->error = $conn->error;
                        }
                    }
                }
                else
                {
                    $json_result->status = 'Error';
                    $json_result->error = 'No meathod for request found';
                }
            }
            else
            {
                $json_result->status = 'Error';
                $json_result->error = 'No http meathod for request found';
            }
        }
        else
        {
            $json_result->status = 'Error';
            $json_result->error = 'Cannot access api user not logged in';
        }
    }
    
    echo json_encode($json_result);
?>

