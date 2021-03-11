#!/bin/bash

if [ ! -e Install.sh ];
then
    echo "You must be in the same directory as Install.sh";
    exit;
fi

workingDirectory=$(pwd)

#MariaDB Install
yum install -y mariadb-server.x86_64

systemctl enable mariadb
systemctl start mariadb

mysql_secure_installation

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

