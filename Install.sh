#!/bin/bash

if [ ! -e Install.sh ];
then
    echo "You must be in the same directory as Install.sh";
    exit;
fi

workingDirectory=$(pwd)

yum install -y httpd epel-release

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

systemctl restart httpd

cd -

cat <<EOF | sudo tee /etc/yum.repos.d/influxdb.repo
[influxdb]
name = InfluxDB Repository - RHEL \$releasever
baseurl = https://repos.influxdata.com/rhel/\$releasever/\$basearch/stable
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdb.key
EOF
yum install -y influxdb.x86_64
systemctl enable influxdb
systemctl start influxdb

yum install -y python39.x86_64 python39-pip.noarch python39-devel.x86_64 gcc openldap-devel.x86_64
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

#Zookeeper Install
yum install -y java-1.8.0-openjdk.x86_64
cd /opt
wget -o apache-zookeeper.tar.gz https://archive.apache.org/dist/zookeeper/zookeeper-3.8.0/apache-zookeeper-3.8.0-bin.tar.gz
tar -xf apache-zookeeper-*.tar.gz
rm -f apache-zookeeper.tar.gz
mv apache-zookeeper-* apache-zookeeper
cd /opt/apache-zookeeper
mkdir data
egrep -v "^dataDir|^#" conf/zoo_sample.cfg | grep . > conf/zoo.cfg
echo "dataDir=/opt/apache-zookeeper/data" >> conf/zoo.cfg
mv conf/zoo_sample.cfg conf/zoo.cfg
adduser -M -r -s /sbin/nologin zookeeper
chown -R zookeeper:zookeeper /opt/apache-zookeeper

cat > /usr/lib/systemd/system/zookeeper.service <<EOF
[Unit]
Description=Zookeeker Service

[Service]
Type=forking
SyslogIdentifier=zookeeper
User=zookeeper
Group=zookeeper
WorkingDirectory=/opt/apache-zookeeper
ExecStart=/opt/apache-zookeeper/bin/zkServer.sh start
ExecStop=/opt/apache-zookeeper/bin/zkServer.sh stop
PIDFile=/opt/apache-zookeeper/data/zookeeper_server.pid
Restart=always
TimeoutSec=60

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl start zookeeper
systemctl enable zookeeper

yum install -y cppunit-devel.x86_64 --enablerepo powertools
yum install -y javapackages-tools.noarch --enablerepo appstream
yum install -y maven.noarch
mkdir -p /opt/zkBuild
cd /opt/zkBuild
wget -O apache-zookeeper.tar.gz https://archive.apache.org/dist/zookeeper/zookeeper-3.8.0/apache-zookeeper-3.8.0.tar.gz
tar -xf apache-zookeeper.tar.gz
rm -f apache-zookeeper.tar.gz
mv apache-zookeeper-* apache-zookeeper
chown -R root:root apache-zookeeper
cd apache-zookeeper
mvn compile
cd zookeeper-client/zookeeper-client-c
autoreconf -if
./configure --prefix=/usr/
make
make install
libtool --finish /usr/local/lib

yum install -y php-devel
git clone https://github.com/php-zookeeper/php-zookeeper.git
phpize
./configure --with-libzookeeper-dir=/usr
make
make install
echo "extension=zookeeper.so" > /etc/php.d/20-zookeeper.ini

cat > /usr/lib/systemd/system/radarMaintenanceProcess.service <<EOF
[Unit]
Description=Radar Maintenance Process Service

[Service]
Type=oneshot
SyslogIdentifier=radarMaintenanceProcess
User=root
Group=root
WorkingDirectory=${workingDirectory}/python
ExecStart=${workingDirectory}/python/radarMaintenanceProcess.py

[Install]
WantedBy=multi-user.target
EOF

cat > /usr/lib/systemd/system/radarMaintenanceProcess.timer <<EOF
[Unit]
Description=Radar Maintenance Process Timer
Requires=radarMaintenanceProcess.service

[Timer]
Unit=radarMaintenanceProcess.service
OnCalendar=*-*-* *:*:00,30

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable radarMaintenanceProcess.timer
systemctl start radarMaintenanceProcess.timer

