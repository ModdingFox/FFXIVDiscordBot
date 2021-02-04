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
                
                if ($_POST['Method'] === 'createPlayerCharacter')
                {
                    if(isset($json_payload['Modal-createPlayerCharacter-characterFirstName']) && isset($json_payload['Modal-createPlayerCharacter-characterLastName']))
                    {
                        $insert_sql = 'INSERT INTO ffxivPlayers.playerCharacters (userCN, characterFirstName, characterLastName) VALUES (?, ?, ?); ';
                        $insert_stmt = $conn->prepare($insert_sql);
                        
                        $s_userCN = $usercn;
                        $s_characterFirstName = $json_payload['Modal-createPlayerCharacter-characterFirstName'];
                        $s_characterLastName = $json_payload['Modal-createPlayerCharacter-characterLastName'];
                        
                        $insert_stmt->bind_param("sss", $s_userCN, $s_characterFirstName, $s_characterLastName);
                        
                        if($insert_stmt->execute() === TRUE)
                        {
                            $json_result->status = 'Success';
                            $json_result->result = $insert_stmt->insert_id;
                        }
                        else
                        {
                            $json_result->status = 'Error';
                            $json_result->error = $conn->error;
                        }
                    }
                    else
                    {
                        $json_result->status = 'Error';
                        $json_result->error = 'Missing Paramaters';
                    }
                }
                elseif ($_POST['Method'] === 'retrievePlayerCharactersByUserCN')
                {
                    if(isset($json_payload['playeruserCN']))
                    {
                        $select_sql = 'SELECT id, characterFirstName, characterLastName FROM ffxivPlayers.playerCharacters WHERE userCN = ?';
                        $select_stmt = $conn->prepare($select_sql);
                        
                        $s_userCN = $json_payload['playeruserCN'];
                        
                        $select_stmt->bind_param("s", $s_userCN);
                        
                        if($select_stmt->execute() === TRUE)
                        {
                            $result = [];
                            $sql_result = $select_stmt->get_result();
                            while($row = $sql_result->fetch_assoc())
                            {
                                $rowData = json_decode('{}');
                                $rowData->id = $row['id'];
                                $rowData->characterFirstName = $row['characterFirstName'];
                                $rowData->characterLastName = $row['characterLastName'];
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
                    }
                    else
                    {
                        $json_result->status = 'Error';
                        $json_result->error = 'Missing Paramaters';
                    }
                }
                elseif ($_POST['Method'] === 'retrievePlayerCharacterClassesByUserCNAndCharacterId')
                {
                    if(isset($json_payload['playeruserCN']) && isset($json_payload['playerCharacterId']))
                    {
                        $select_sql = 'SELECT cC.id, cC.classId, cC.currentLevel, cC.averageILevel, cC.hasMeldsCheckbox FROM ffxivPlayers.characterClasses cC JOIN ffxivPlayers.playerCharacters pC ON cC.playerCharacterId = pC.id WHERE pC.userCN = ? AND pC.id = ?';
                        $select_stmt = $conn->prepare($select_sql);
                        
                        $s_userCN = $json_payload['playeruserCN'];
                        $i_playerCharacterId = $json_payload['playerCharacterId'];
                        
                        $select_stmt->bind_param("si", $s_userCN, $i_playerCharacterId);
                        
                        if($select_stmt->execute() === TRUE)
                        {
                            $result = [];
                            $sql_result = $select_stmt->get_result();
                            while($row = $sql_result->fetch_assoc())
                            {
                                $rowData = json_decode('{}');
                                $rowData->id = $row['id'];
                                $rowData->classId = $row['classId'];
                                $rowData->currentLevel = $row['currentLevel'];
                                $rowData->averageILevel = $row['averageILevel'];
                                $rowData->hasMeldsCheckbox = $row['hasMeldsCheckbox'];
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
                    }
                    else
                    {
                        $json_result->status = 'Error';
                        $json_result->error = 'Missing Paramaters';
                    }
                }
                elseif ($_POST['Method'] === 'updatePlayerCharacterByUserCNAndCharacterId')
                {
                    if(isset($json_payload['playerCharacterId']) && isset($json_payload['characterFirstName']) && isset($json_payload['characterLastName']))
                    {
                        $update_sql = 'UPDATE ffxivPlayers.playerCharacters SET characterFirstName = ?, characterLastName = ? WHERE userCN = ? AND id = ?';
                        $update_stmt = $conn->prepare($update_sql);
                        
                        $s_userCN = $usercn;
                        $i_playerCharacterId = $json_payload['playerCharacterId'];
                        $s_characterFirstName = $json_payload['characterFirstName'];
                        $s_characterLastName = $json_payload['characterLastName'];
                        
                        $update_stmt->bind_param("sssi", $s_characterFirstName, $s_characterLastName, $s_userCN, $i_playerCharacterId);
                        
                        if($update_stmt->execute() === TRUE) { $json_result->status = 'Success'; }
                        else
                        {
                            $json_result->status = 'Error';
                            $json_result->error = $conn->error;
                        }
                    }
                    else
                    {
                        $json_result->status = 'Error';
                        $json_result->error = 'Missing Paramaters';
                    }
                }
                elseif ($_POST['Method'] === 'deletePlayerCharacterByUserCNAndCharacterId')
                {
                    if(isset($json_payload['playerCharacterId']))
                    {
                        $delete_sql = 'DELETE FROM ffxivPlayers.playerCharacters WHERE userCN = ? AND id = ?';
                        $delete_stmt = $conn->prepare($delete_sql);
                        
                        $s_userCN = $usercn;
                        $i_playerCharacterId = $json_payload['playerCharacterId'];
                        
                        $delete_stmt->bind_param("si", $s_userCN, $i_playerCharacterId);
                        
                        if($delete_stmt->execute() === TRUE) { $json_result->status = 'Success'; }
                        else
                        {
                            $json_result->status = 'Error';
                            $json_result->error = $conn->error;
                        }
                    }
                    else
                    {
                        $json_result->status = 'Error';
                        $json_result->error = 'Missing Paramaters';
                    }
                }
                elseif ($_POST['Method'] === 'updateCharacterClassesByUserCNAndCharacterId')
                {
                    if(isset($json_payload['playerCharacterId']))
                    {
                        $select_sql = 'SELECT id FROM ffxivPlayers.playerCharacters WHERE userCN = ?';
                        $select_stmt = $conn->prepare($select_sql);
                        
                        $s_userCN = $usercn;
                        
                        $select_stmt->bind_param("s", $s_userCN);
                        
                        $playerCharacterIds = [];
                        
                        if($select_stmt->execute() === TRUE)
                        {
                            $select_result = $select_stmt->get_result();
                            while($row = $select_result->fetch_assoc()) { array_push($playerCharacterIds, $row['id']); }
                        }
                        else
                        {
                            $json_result->status = 'Error';
                            $json_result->error = $conn->error;
                        }
                        
                        if(in_array($json_payload['playerCharacterId'], $playerCharacterIds))
                        {
                            $select_sql = 'SELECT classId FROM ffxivPlayers.characterClasses WHERE playerCharacterId = ?';
                            $select_stmt = $conn->prepare($select_sql);
                            
                            $i_playerCharacterId = $json_payload['playerCharacterId'];
                            
                            $select_stmt->bind_param("s", $i_playerCharacterId);
                            
                            if($select_stmt->execute() === TRUE)
                            {
                                $existingPlayerClasses = [];
                                $select_result = $select_stmt->get_result();
                                while($row = $select_result->fetch_assoc()) { array_push($existingPlayerClasses, $row['classId']); }
                                
                                $select_sql = 'SELECT id FROM ffxivReference.classes';
                                $select_stmt = $conn->prepare($select_sql);
                                
                                if($select_stmt->execute() === TRUE)
                                {
                                    $hasErrored = FALSE;
                                    $select_result = $select_stmt->get_result();
                                    while($row = $select_result->fetch_assoc())
                                    {
                                        $i_currentClassId = $row['id'];
                                        if(isset($json_payload['Modal-editPlayerCharacter-class' . $i_currentClassId . 'Checkbox']) && isset($json_payload['Modal-editPlayerCharacter-class' . $i_currentClassId . 'Level']) && isset($json_payload['Modal-editPlayerCharacter-class' . $i_currentClassId . 'AverageILevel']) && isset($json_payload['Modal-editPlayerCharacter-class' . $i_currentClassId . 'HasMeldsCheckbox']))
                                        {
                                            $i_playerCharacterId = $json_payload['playerCharacterId'];
                                            $i_classLevel = $json_payload['Modal-editPlayerCharacter-class' . $i_currentClassId . 'Level'];
                                            $i_classAverageILevel = $json_payload['Modal-editPlayerCharacter-class' . $i_currentClassId . 'AverageILevel'];
                                            $i_classHasMeldsCheckbox = $json_payload['Modal-editPlayerCharacter-class' . $i_currentClassId . 'HasMeldsCheckbox'];
                                            
                                            if(in_array($i_currentClassId, $existingPlayerClasses))
                                            {
                                                if($json_payload['Modal-editPlayerCharacter-class' . $i_currentClassId . 'Checkbox'] == 1)
                                                {
                                                    $update_sql = 'UPDATE ffxivPlayers.characterClasses cC JOIN ffxivPlayers.playerCharacters pC ON pC.id = cC.playerCharacterId SET cC.currentLevel = ?, cC.averageILevel = ?, cC.hasMeldsCheckbox = ? WHERE pC.id = ? AND cC.classId = ?';
                                                    $update_stmt = $conn->prepare($update_sql);
                                                    $update_stmt->bind_param("iiiii", $i_classLevel, $i_classAverageILevel, $i_classHasMeldsCheckbox, $i_playerCharacterId, $i_currentClassId);
                                                    
                                                    if($update_stmt->execute() === FALSE)
                                                    {
                                                        $json_result->status = 'Error';
                                                        $json_result->error = $conn->error;
                                                        $hasErrored = TRUE;
                                                        break;
                                                    }
                                                }
                                                else
                                                {
                                                    $delete_sql = 'DELETE FROM ffxivPlayers.characterClasses WHERE playerCharacterId = ? AND classId = ?';
                                                    $delete_stmt = $conn->prepare($delete_sql);
                                                    $delete_stmt->bind_param("ii", $i_playerCharacterId, $i_currentClassId);
                                                    
                                                    if($delete_stmt->execute() === FALSE)
                                                    {
                                                        $json_result->status = 'Error';
                                                        $json_result->error = $conn->error;
                                                        $hasErrored = TRUE;
                                                        break;
                                                    }
                                                }
                                            }
                                            else
                                            {
                                                if($json_payload['Modal-editPlayerCharacter-class' . $i_currentClassId . 'Checkbox'] == 1)
                                                {
                                                    $insert_sql = 'INSERT INTO ffxivPlayers.characterClasses (playerCharacterId, classId, currentLevel, averageILevel, hasMeldsCheckbox) VALUES (?, ?, ?, ?, ?)';
                                                    $insert_stmt = $conn->prepare($insert_sql);
                                                    $insert_stmt->bind_param("iiiii", $i_playerCharacterId, $i_currentClassId, $i_classLevel, $i_classAverageILevel, $i_classHasMeldsCheckbox);
                                                    
                                                    if($insert_stmt->execute() === FALSE)
                                                    {
                                                        $json_result->status = 'Error';
                                                        $json_result->error = $conn->error;
                                                        $hasErrored = TRUE;
                                                        break;
                                                    }
                                                }
                                            }
                                        }
                                        else
                                        {
                                            $json_result->status = 'Error';
                                            $json_result->error = "Missing a class from the payload";
                                            $hasErrored = TRUE;
                                            break;
                                        }
                                    }
                                    
                                    if($hasErrored === FALSE) { $json_result->status = 'Success'; }
                                }
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
                        $json_result->error = 'Missing Paramaters';
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
