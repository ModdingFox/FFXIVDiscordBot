<?php
    $ldaphost='127.0.0.1';
    $ldapconn=ldap_connect($ldaphost);

    $User='';
    $ldapdn='';
    $ldappass='';

    ldap_set_option($ldapconn, LDAP_OPT_PROTOCOL_VERSION, 3);
    ldap_set_option($ldapconn, LDAP_OPT_REFERRALS, 0);

    $ldapbind = NULL;

    if ($ldapconn)
    {
        $ldapbind = ldap_bind($ldapconn, 'cn=' . $User . ',' . $ldapdn, $ldappass);
    }

#    function closeLdapConnection($var) { ldap_close($var); }
#    register_shutdown_function('closeLdapConnection', $ldapconn);
?>
