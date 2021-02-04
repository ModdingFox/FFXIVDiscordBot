<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

    require('../ldap_Connection.php');
    $ldapbind = ldap_bind($ldapconn, 'cn=' . $User . ',' . $ldapdn, $ldappass);
    if ($ldapbind) { echo 'LDAP bind success'; }
    else { echo 'LDAP bind failure'; }

    $groupDN = 'cn=Members,ou=Group,dc=foxtek,dc=us';
                $group_ldap_search_result = ldap_search($ldapconn, 'ou=People,' . $ldapdn, '(&(cn=' . "a481fcae-3bac-48cd-b3f3-2066a06468de" . ')(memberof=' . $groupDN . '))');
                $group_ldap_search_count = ldap_count_entries($ldapconn, $group_ldap_search_result);
                echo $group_ldap_search_count;

?>
