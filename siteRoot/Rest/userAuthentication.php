<?php
    require('/var/www/html/Utility/utility.php');
    require('/var/www/html/ldap_Connection.php');
    require('/var/www/html/redis_Connection.php');
    require('/var/www/html/Utility/login.php');
    require('/var/www/html/email.php');
    
    $json_result = json_decode('{}');
    $randomUID = uuid();
    
    if ($_SERVER['REQUEST_METHOD'] === 'POST')
    {
        $json_payload = json_decode($_POST['JSON'], true);
        
        if ($_POST['Method'] === 'userRegistration')
        {
            $NewUserInfo['cn'] = $randomUID;
            $NewUserInfo['uid'] = $json_payload['Modal-userRegistration-username'];
            $NewUserInfo['displayName'] = $NewUserInfo['uid'];
            $NewUserInfo['userPassword'] = sprintf('{CRYPT}%s',crypt($json_payload['Modal-userRegistration-password'],'$6$'.random_salt(8)));
            $NewUserInfo['mail'] = $json_payload['Modal-userRegistration-email'];
            
            $userDN = 'uid=' . $NewUserInfo['uid'] . ',ou=People,' . $ldapdn;
            
            $NewUserInfo['objectclass'][0] = "top";
            $NewUserInfo['objectclass'][1] = "person";
            $NewUserInfo['objectclass'][2] = "inetOrgPerson";
            
            if(strlen($json_payload['Modal-userRegistration-firstName']) == 0) {   }
            else { $NewUserInfo['givenName'] = $json_payload['Modal-userRegistration-firstName']; }
            
            if(strlen($json_payload['Modal-userRegistration-lastName']) == 0) { $NewUserInfo['sn'] = $NewUserInfo['displayName']; }
            else { $NewUserInfo['sn'] = $json_payload['Modal-userRegistration-lastName']; }
            
            $uid_ldap_search_result = ldap_search($ldapconn, 'ou=People,' . $ldapdn, '(uid=' . $NewUserInfo['uid'] . ')');
            $uid_ldap_search_count = ldap_count_entries($ldapconn, $uid_ldap_search_result);
            
            $mail_ldap_search_result = ldap_search($ldapconn, 'ou=People,' . $ldapdn, '(mail=' . $NewUserInfo['mail'] . ')');
            $mail_ldap_search_count = ldap_count_entries($ldapconn, $mail_ldap_search_result);
            
            if($uid_ldap_search_count == 0)
            {
                if($mail_ldap_search_count == 0)
                {
                    if(ldap_add($ldapconn, $userDN, $NewUserInfo))
                    {
                        $message = "Please visit the following link to activate your account. https://foxtek.us/Rest/userAuthentication.php?Method=userActivate&cn=" . $NewUserInfo['cn'];
                        $json_result = sendEmail($json_payload['Modal-userRegistration-email'], "Account Registration", "<p>" . $message . "</p>", $message);
                    }
                    else
                    {
                        $json_result->status = 'Error';
                        $json_result->error = 'Could not create user. Please contact your system admin';
                    }
                }
                else
                {
                    $json_result->status = 'Error';
                    $json_result->error = 'The email address is already in use';
                }
            }
            else
            {
                $json_result->status = 'Error';
                $json_result->error = 'The username is already taken';
            }
        }
        elseif ($_POST['Method'] === 'userLogin')
        {
            $tokenTTLSeconds = 21600;
            
            $userInfo['uid'] = $json_payload['Modal-userLogin-username'];
            $userDN = 'uid=' . $userInfo['uid'] . ',ou=People,' . $ldapdn;
            
            $uid_ldap_search_result = ldap_search($ldapconn, 'ou=People,' . $ldapdn, '(uid=' . $userInfo['uid'] . ')', array('cn'));
            $uid_ldap_search_count = ldap_count_entries($ldapconn, $uid_ldap_search_result);
            $ldap_entry = ldap_get_entries($ldapconn, $uid_ldap_search_result);
            
            if($uid_ldap_search_count == 1 && $ldapbind = ldap_bind($ldapconn, $userDN, $json_payload['Modal-userLogin-password']))
            {
                $member_group_ldap_search_result = ldap_search($ldapconn, 'ou=People,' . $ldapdn, '(&(cn=' . $ldap_entry[0]['cn'][0] . ')(memberof=' . $memberGroupDN . '))');
                $member_group_ldap_search_count = ldap_count_entries($ldapconn, $member_group_ldap_search_result);
                
                $ban_group_ldap_search_result = ldap_search($ldapconn, 'ou=People,' . $ldapdn, '(&(cn=' . $ldap_entry[0]['cn'][0] . ')(memberof=' . $banGroupDN . '))');
                $ban_group_ldap_search_count = ldap_count_entries($ldapconn, $ban_group_ldap_search_result);

                if($member_group_ldap_search_count == 1)
                {
                    if($ban_group_ldap_search_count == 1)
                    {
                        $json_result->status = 'Error';
                        $json_result->error = 'User account is banned. Please contact admin for more information.';
                    }
                    else
                    {
                        if(phpiredis_command($redis, 'SET SESSION_' . $randomUID  . ' ' . $ldap_entry[0]['cn'][0] . ' EX ' . $tokenTTLSeconds) == "OK")
                        {
                            setcookie("cn", $ldap_entry[0]['cn'][0], time()+$tokenTTLSeconds, "/");
                            setcookie("token", $randomUID, time()+$tokenTTLSeconds, "/");
                            
                            $json_result->status = 'Success';
                        }
                        else
                        {
                            $json_result->status = 'Error';
                            $json_result->error = 'Could not set session token';
                        }
                    }
                }
                else
                {
                    $json_result->status = 'Warning';
                    $json_result->warning = 'Please check your email for an activation link';
                }
            }
            else
            {
                $json_result->status = 'Error';
                $json_result->error = 'Bad user/password combination';
            }
        }
        elseif ($_POST['Method'] === 'userPasswordResetTokenRequest')
        {
            $tokenTTLSeconds = 600;
            
            $userInfo['uid'] = $json_payload['Modal-userPasswordResetRequest-username'];
            $userDN = 'uid=' . $userInfo['uid'] . ',ou=People,' . $ldapdn;
            
            $uid_ldap_search_result = ldap_search($ldapconn, 'ou=People,' . $ldapdn, '(uid=' . $userInfo['uid'] . ')');
            $uid_ldap_search_count = ldap_count_entries($ldapconn, $uid_ldap_search_result);
            $ldap_entry = ldap_get_entries($ldapconn, $uid_ldap_search_result);
            
            if($uid_ldap_search_count == 1)
            {
                if(phpiredis_command($redis, 'SET RESET_' . $randomUID  . ' ' . $ldap_entry[0]['cn'][0] . ' EX ' . $tokenTTLSeconds) == "OK")
                {
                    $message = "Use the following link to reset your password. https://foxtek.us?resetToken=" . $randomUID . " The link is valid for 10 minutes from when the reset is requested. If you did not request this reset contact admin.";
                    $json_result = sendEmail($ldap_entry[0]['mail'][0], "Password Reset Request", "<p>" . $message . "</p>", $message);
                }
                else
                {
                    $json_result->status = 'Error';
                    $json_result->error = 'Could not set session token';
                }
            }
            else
            {
                $json_result->status = 'Error';
                $json_result->error = 'Could not find user for password reset';
            }
        }
        elseif ($_POST['Method'] === 'userPasswordReset' && isset($_GET['resetToken']))
        {
            $resetToken = $_GET['resetToken'];
            $redisUserCN = phpiredis_command($redis, 'GET RESET_' . $resetToken);
            $UpdateUserInfo['userPassword'] = sprintf('{CRYPT}%s',crypt($json_payload['Modal-userPasswordReset-password'],'$6$'.random_salt(8)));
            
            if($redisUserCN != '')
            {
                $cn_ldap_search_result = ldap_search($ldapconn, 'ou=People,' . $ldapdn, '(cn=' . $redisUserCN . ')');
                $cn_ldap_search_count = ldap_count_entries($ldapconn, $cn_ldap_search_result);
                $ldap_entry = ldap_get_entries($ldapconn, $cn_ldap_search_result);
                
                if($cn_ldap_search_count == 1)
                {
                    $resetUserDN = $ldap_entry[0]['dn'];
                    
                    if(phpiredis_command($redis, 'DEL RESET_' . $resetToken) == 1)
                    {
                        if(ldap_mod_replace($ldapconn, $resetUserDN, $UpdateUserInfo)) { $json_result->status = 'Success'; }
                        else
                        {
                            $json_result->status = 'Error';
                            $json_result->error = 'Could not reset password';
                        }
                    }
                    else
                    {
                        $json_result->status = 'Error';
                        $json_result->error = 'Could not clear reset token';
                    }
                }
                else
                {
                    $json_result->status = 'Error';
                    $json_result->error = 'Could not find user for password reset';
                }
            }
            else
            {
                $json_result->status = 'Error';
                $json_result->error = 'Reset token is invalid/expired';
            }
        }
        elseif ($_POST['Method'] === 'userLogout')
        {
            if($isLoggedIn)
            {
                if(phpiredis_command($redis, 'GET SESSION_' . $usertoken) == $usercn)
                {
                    if(phpiredis_command($redis, 'DEL SESSION_' . $usertoken) == 1) { $json_result->status = 'Success'; }
                    else
                    {
                        $json_result->status = 'Error';
                        $json_result->error = 'Could not remove user session. Please contact admin';
                    }
                }
                else
                {
#                    This is here only to explain the situation. This should not be enabled in the real world
#                    $json_result->status = 'Error';
#                    $json_result->error = 'Cannot invalidate token belonging to another user';
                }
            }
            else
            {
                $json_result->status = 'Error';
                $json_result->error = 'Could not remove user session user not logged in';
            }
        }
        else
        {
            $json_result->status = 'Error';
            $json_result->error = 'No meathod for request found';
        }
    }
    elseif ($_SERVER['REQUEST_METHOD'] === 'GET')
    {
        if ($_GET['Method'] === 'userActivate' && isset($_GET['cn']))
        {
            $cn_ldap_search_result = ldap_search($ldapconn, 'ou=People,' . $ldapdn, '(cn=' . $_GET['cn'] . ')');
            $cn_ldap_search_count = ldap_count_entries($ldapconn, $cn_ldap_search_result);
            
            if($cn_ldap_search_count == 1)
            {
                $ldap_entry = ldap_get_entries($ldapconn, $cn_ldap_search_result);
                $UserGroupInfo['member'] = $ldap_entry[0]['dn'];
                if(ldap_mod_add($ldapconn, $memberGroupDN, $UserGroupInfo))
                {
                    $json_result->status = 'Success';
                    header('Location: /');
                }
                else
                {
                    $json_result->status = 'Error';
                    $json_result->error = 'Could not add user to ' . $memberGroupDN;
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
    
    echo json_encode($json_result);
?>
