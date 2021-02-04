<?php
    require('/var/www/html/redis_Connection.php');
    require('/var/www/html/ldap_Connection.php');
    
    $memberGroupDN = 'cn=Members,ou=Group,' . $ldapdn;
    $banGroupDN = 'cn=Banned,ou=Group,' . $ldapdn;
    
    $usercn = $_COOKIE['cn'];
    $usertoken = $_COOKIE['token'];
    $rediscn = phpiredis_command($redis, 'GET SESSION_' . $usertoken);
    $isLoggedIn = false;

    $userName = null;
    $userGroups = array();

    if($rediscn == $usercn)
    {
        $cn_ldap_search_result = ldap_search($ldapconn, 'ou=People,' . $ldapdn, '(cn=' . $usercn . ')', array('uid'));
        $cn_ldap_search_count = ldap_count_entries($ldapconn, $cn_ldap_search_result);
        if($cn_ldap_search_count == 1)
        {
            $cn_ldap_entry = ldap_get_entries($ldapconn, $cn_ldap_search_result); 
            $userName = $cn_ldap_entry[0]['uid'][0];
            
            $group_ldap_search_result = ldap_search($ldapconn, 'ou=Group,' . $ldapdn, '(member=' . $cn_ldap_entry[0]['dn'] . ')', array('DN'));
            $group_ldap_search_count = ldap_count_entries($ldapconn, $group_ldap_search_result);
            
            if($group_ldap_search_count > 0)
            {
                $group_ldap_entry = ldap_get_entries($ldapconn, $group_ldap_search_result);
                unset($group_ldap_entry['count']);
                foreach ($group_ldap_entry as $currentEntry)
                {
                    if(isset($currentEntry['dn'])) { array_push($userGroups, $currentEntry['dn']); }
                }
            }
            
            if(in_array($banGroupDN, $userGroups)) { $isLoggedIn = false; }
            else { $isLoggedIn = true; }
        }
    }
?>
