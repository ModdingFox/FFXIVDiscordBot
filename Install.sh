#!/bin/bash

if [ ! -e Install.sh ];
then
    echo "You must be in the same directory as Install.sh";
    exit;
fi

workingDirectory=$(pwd)

yum install -y epel-release

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

yum install -y python3.x86_64 python3-pip.noarch python3-devel.x86_64 gcc openldap-devel.x86_64
pip-3.9 install discord.py
pip-3.9 install python-dotenv
pip-3.9 install PyMySQL
pip-3.9 install requests
pip-3.9 install python-ldap
pip-3.9 install beautifulsoup4
pip-3.9 install kazoo
pip-3.9 install influxdb

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
