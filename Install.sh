#!/bin/bash

yum install -y mariadb-server.x86_64

systemctl enable mariadb
systemctl start mariadb

mysql_secure_installation

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
