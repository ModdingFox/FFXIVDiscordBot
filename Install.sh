#!/bin/bash

if [ ! -e Install.sh ];
then
    echo "You must be in the same directory as Install.sh";
    exit;
fi

workingDirectory=$(pwd)

yum install -y httpd

firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --zone=public --add-port=443/tcp --permanent
firewall-cmd --reload

sed -ie 's|index.html|index.php|g' /etc/httpd/conf/httpd.conf && rm -f /etc/httpd/conf/httpd.confe

cat > /etc/httpd/conf.d/80.conf <<EOF
<VirtualHost *:80>
    DocumentRoot "/var/www/clubspectrum.us"
    ServerName clubspectrum.us
    <Directory /var/www/clubspectrum.us>
        Options -Indexes +FollowSymLinks
        AllowOverride All
    </Directory>
RewriteEngine on
RewriteCond %{SERVER_NAME} =clubspectrum.us
RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>
EOF

ln -s $(pwd)/siteRoot /var/www/clubspectrum.us

systemctl enable httpd
systemctl start httpd

yum install -y \
php.x86_64 \
php-cli.x86_64 \
php-common.x86_64 \
php-fpm.x86_64 \
php-json.x86_64 \
php-mysqlnd.x86_64 \
php-pdo.x86_64 \
php-pear.noarch \
php-process.x86_64 \
php-xml.x86_64

#MariaDB Install
yum install -y mariadb-server.x86_64

systemctl enable mariadb
systemctl start mariadb

mysql_secure_installation

mysql -u root -h 127.0.0.1 -p < siteSql.sql

#Grafana Install
cat > /etc/yum.repos.d/grafana.repo <<EOF
[grafana]
name=grafana
baseurl=https://packages.grafana.com/oss/rpm
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://packages.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
EOF

yum -y install grafana fontconfig fontconfig* urw-fonts

systemctl start grafana-server
systemctl enable grafana-server.service

firewall-cmd --zone=public --add-port=3000/tcp --permanent
firewall-cmd --reload

#SSL Cert Install
yum install -y snapd mod_ssl
ln -s /var/lib/snapd/snap /snap
systemctl start snapd
snap install --classic certbot
ln -s /snap/bin/certbot /usr/bin/certbot
certbot --apache

#Logstash and Elasticsearch Install
cat > /etc/yum.repos.d/logstash.repo <<EOF
[logstash-7.x]
name=Elastic repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF

cat > /etc/yum.repos.d/elasticsearch.repo <<EOF
[elasticsearch]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF

yum install -y logstash elasticsearch

systemctl enable elasticsearch
systemctl start elasticsearch

#Logstash Systemd
cat > /usr/lib/systemd/system/logstash-httpd.service <<EOF
[Unit]
Description=logstash(httpd) Service

[Service]
Type=simple
SyslogIdentifier=logstash-httpd
User=root
Group=root
WorkingDirectory=${workingDirectory}
ExecStart=/usr/share/logstash/bin/logstash -f ${workingDirectory}/httpd/logstash-apache.conf
Restart=always
TimeoutSec=60

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable logstash-httpd.service
systemctl start logstash-httpd.service

yum install -y npm

mkdir -p siteRoot/npm
cd siteRoot/npm

npm install popper.js@1.14.7 --save
npm install jquery@3.4.1 --save
npm install datatables.net@1.10.24 --save
npm install bootstrap@4.3.1 --save
npm install parsleyjs@2.9.2 --save
npm install underscore@1.10.2 --save
npm install jquery.cookie@1.4.1 --save

cd -

yum install python3-pip.noarch python36-devel.x86_64 gcc openldap-devel.x86_64
pip-3 install discord
pip-3 install python-dotenv
pip-3 install PyMySQL
pip-3 install requests
pip-3 install python-ldap
pip-3 install beautifulsoup4

cat > /usr/lib/systemd/system/discordBot.service <<EOF
[Unit]
Description=Discord Bot Service

[Service]
Type=simple
SyslogIdentifier=discordBot
User=root
Group=root
WorkingDirectory=${workingDirectory}/discordBot
ExecStart=${workingDirectory}/discordBot/entry.py
Restart=always
TimeoutSec=60

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable discordBot.service
systemctl start discordBot.service
