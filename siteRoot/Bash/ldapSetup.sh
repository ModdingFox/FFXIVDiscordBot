#!/bin/bash

yum -y install openldap compat-openldap openldap-clients openldap-servers openldap-servers-sql openldap-devel

systemctl start slapd.service
systemctl enable slapd.service

ldapDC=""

ldapPassword=""
passwordHash=$(slappasswd -s ${ldapPassword})

ldifRootPath="/tmp"

#Initialize DB
cat > ${ldifRootPath}/db.ldif <<EOF
dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcSuffix
olcSuffix: ${ldapDC}

dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcRootDN
olcRootDN: cn=ldapadm,${ldapDC}

dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcRootPW
olcRootPW: ${passwordHash}
EOF

ldapmodify -Y EXTERNAL -H ldapi:/// -f ${ldifRootPath}/db.ldif

#Restrict Monitor Access
cat > ${ldifRootPath}/monitor.ldif <<EOF
dn: olcDatabase={1}monitor,cn=config
changetype: modify
replace: olcAccess
olcAccess: {0}to * by dn.base="gidNumber=0+uidNumber=0,cn=peercred,cn=external, cn=auth" read by dn.base="cn=ldapadm,${ldapDC}" read by * none
EOF

ldapmodify -Y EXTERNAL -H ldapi:/// -f ${ldifRootPath}/monitor.ldif

#Security Crap Here YAY SSL
openssl req -new -x509 -nodes -out \
/etc/openldap/certs/openldap.${ldapDC}.cert \
-keyout /etc/openldap/certs/openldap.${ldapDC}.key \
-days 365 << EOF
US
AR
Little Rock
FoxTek

$(hostname -f)
admin@foxtek.us
EOF

chown -R ldap:ldap /etc/openldap/certs

#I dont fucking understand this but flipping these sometimes fixes it
cat > ${ldifRootPath}/certs.ldif <<EOF
dn: cn=config
changetype: modify
replace: olcTLSCertificateFile
olcTLSCertificateFile: /etc/openldap/certs/openldap.${ldapDC}.cert

dn: cn=config
changetype: modify
replace: olcTLSCertificateKeyFile
olcTLSCertificateKeyFile: /etc/openldap/certs/openldap.${ldapDC}.key
EOF

ldapmodify -Y EXTERNAL -H ldapi:/// -f ${ldifRootPath}/certs.ldif

cat > ${ldifRootPath}/certs.ldif <<EOF
dn: cn=config
changetype: modify
replace: olcTLSCertificateKeyFile
olcTLSCertificateKeyFile: /etc/openldap/certs/openldap.${ldapDC}.key

dn: cn=config
changetype: modify
replace: olcTLSCertificateFile
olcTLSCertificateFile: /etc/openldap/certs/openldap.${ldapDC}.cert
EOF

ldapmodify -Y EXTERNAL -H ldapi:/// -f ${ldifRootPath}/certs.ldif

#Setup Berkeley database
cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG
chown -R ldap:ldap /var/lib/ldap

ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/cosine.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/nis.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/inetorgperson.ldif

cat > ${ldifRootPath}/base.ldif <<EOF
dn: ${ldapDC}
objectClass: top
objectClass: domain

dn: cn=ldapadm,${ldapDC}
objectClass: organizationalRole
cn: ldapadm
description: LDAP Manager

dn: ou=People,${ldapDC}
objectClass: organizationalUnit
ou: People

dn: ou=Group,${ldapDC}
objectClass: organizationalUnit
ou: Group
EOF

ldapadd -x -D "cn=ldapadm,${ldapDC}" -f ${ldifRootPath}/base.ldif -w "${ldapPassword}"

cat > ${ldifRootPath}/memberofConfig.ldif <<EOF
dn: cn=module,cn=config
cn: module
objectClass: olcModuleList
olcModuleLoad: memberof
olcModulePath: /usr/lib64/openldap

dn: olcOverlay={0}memberof,olcDatabase={2}hdb,cn=config
objectClass: olcConfig
objectClass: olcMemberOf
objectClass: olcOverlayConfig
objectClass: top
olcOverlay: memberof
olcMemberOfDangling: ignore
olcMemberOfRefInt: TRUE
olcMemberOfGroupOC: groupOfNames
olcMemberOfMemberAD: member
olcMemberOfMemberOfAD: memberOf
EOF

ldapadd -Q -Y EXTERNAL -H ldapi:/// -f ${ldifRootPath}/memberofConfig.ldif

cat > ${ldifRootPath}/refint1.ldif <<EOF
dn: cn=module{0},cn=config
add: olcmoduleload
olcmoduleload: refint
EOF

ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f ${ldifRootPath}/refint1.ldif

cat > ${ldifRootPath}/refint2.ldif <<EOF
dn: olcOverlay={1}refint,olcDatabase={2}hdb,cn=config
objectClass: olcConfig
objectClass: olcOverlayConfig
objectClass: olcRefintConfig
objectClass: top
olcOverlay: {1}refint
olcRefintAttribute: memberof member manager owner
EOF

ldapadd -Q -Y EXTERNAL -H ldapi:/// -f ${ldifRootPath}/refint2.ldif

#Add the admin web UI the version below supports php7
cd /var/www/html
git clone https://github.com/leenooks/phpLDAPadmin.git
cd /var/www/html/phpLDAPadmin/config
mv config.php.example config.php
