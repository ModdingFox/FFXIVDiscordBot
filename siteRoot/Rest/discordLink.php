<?php
    require('/var/www/html/Utility/utility.php');
    require('/var/www/html/redis_Connection.php');
    require('/var/www/html/Utility/login.php');
    require('/var/www/html/DB_Connection.php');
    
    $json_result = json_decode('{}');
    $randomUID = uuid();
    
    if ($_SERVER['REQUEST_METHOD'] === 'POST')
    {
        $json_payload = json_decode($_POST['JSON'], true);
        
        if ($_POST['Method'] === 'generateDiscordLinkToken')
        {
            if($isLoggedIn)
            {
                $tokenTTLSeconds = 300;
                
                if(phpiredis_command($redis, 'SET DISCORDLINK_' . $randomUID  . ' ' . $usercn . ' EX ' . $tokenTTLSeconds) == "OK")
                {
                    $json_result->status = 'Success';
                    $json_result->result = $randomUID;
                }
                else
                {
                    $json_result->status = 'Error';
                    $json_result->error = 'Could not set discord link token';
                }
            }
            else
            {
                $json_result->status = 'Error';
                $json_result->error = 'Could not set discord link token user not logged in';
            }
        }
        elseif ($_POST['Method'] === 'registerDiscordLinkToken')
        {
           $discordLinkToken = $json_payload['discordLinkToken'];
           $discordId = $json_payload['discordId'];
           $redisUserCN = phpiredis_command($redis, 'GET DISCORDLINK_' . $discordLinkToken);
           
           if($redisUserCN != "")
           {
                if(phpiredis_command($redis, 'DEL DISCORDLINK_' . $discordLinkToken) == 1)
                {
                    $delete_sql = 'DELETE FROM userAccountData.discordLink WHERE userCN = ?';
                    $delete_stmt = $conn->prepare($delete_sql);
                    
                    $s_userCN = $redisUserCN;
                    
                    $delete_stmt->bind_param("s", $s_userCN);
                    
                    if($delete_stmt->execute() === TRUE)
                    {
                        $insert_sql = 'INSERT INTO userAccountData.discordLink (userCN, discordId) VALUES (?, ?)';
                        $insert_stmt = $conn->prepare($insert_sql);
                        
                        $s_discordId = $discordId;
                    
                        $insert_stmt->bind_param("ss", $s_userCN, $s_discordId);
                    
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
                else
                {
                    $json_result->status = 'Error';
                    $json_result->error = 'Could not remove discord registration token. Please contact admin';
                }
           }
           else
           {
                $json_result->status = 'Error';
                $json_result->error = 'Discord registration token does not exist';
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
    
    echo json_encode($json_result);
?>
