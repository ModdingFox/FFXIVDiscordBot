#!/bin/bash

if [ ! -e systemdInstall.sh ];
then
    echo "You must be in the same directory as systemdInstall.sh";
    exit;
fi

yum install python3-pip.noarch python3-devel.x86_64
pip-3 install discord
pip-3 install python-dotenv
pip-3 install PyMySQL
pip-3 install requests
pip-3 install python-ldap

workingDirectory=$(pwd)

cat > /usr/lib/systemd/system/discordBot.service <<EOF
[Unit]
Description=Discord Bot Service

[Service]
Type=simple
SyslogIdentifier=discordBot
User=root
Group=root
WorkingDirectory=${workingDirectory}
ExecStart=${workingDirectory}/entry.py
Restart=always
TimeoutSec=60

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable discordBot.service
systemctl start discordBot.service
