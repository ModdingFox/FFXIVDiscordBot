#!/bin/bash

#Update and install required components
yum -y update
yum -y install epel-release
yum install http://rpms.remirepo.net/enterprise/remi-release-7.rpm
yum -y groupinstall "X Window system"
yum -y groupinstall xfce
yum -y install \
firefox \
git \
vim \
wget \
httpd \
mod_ssl \
nodejs \
php-masterminds-html5 \
mariadb-server \
redis

yum --enablerepo=remi-php73 install \
php \
php-mysql \
php-xml \
php-json \
php-ldap \
php-phpiredis.x86_64 \
php-PHPMailer.noarch \
phpmyadmin

#Setup phpmyadmin with config file

#Bit of httpd config
sed -ie 's|index.html|index.php|g' /etc/httpd/conf/httpd.conf && rm -f /etc/httpd/conf/httpd.confe

#Enable and start services
systemctl enable httpd
systemctl start httpd

#Open Firewall Ports
firewall-cmd --zone=public --permanent --add-port=80/tcp
firewall-cmd --zone=public --permanent --add-port=443/tcp

#Setup httpd virtual host on port 80
cat > /etc/httpd/conf.d/80.conf <<EOF
<VirtualHost *:80>
    DocumentRoot "/var/www/html"
    ServerName foxtek.us
</VirtualHost>
EOF

systemctl restart httpd

systemctl enable mariadb
systemctl start mariadb

systemctl enable redis
systemctl start redis

#SSL Cert Setup(Lets encrypt)
yum -y install certbot python2-certbot-apache
certbot --apache

#Mariadb Setup
DB_Root_Password=""

mysql_secure_installation <<EOF

Y
$DB_Root_Password
$DB_Root_Password
Y
Y
Y
Y
EOF

php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php --install-dir=/usr/local/bin --filename=composer
ln -s /usr/local/bin/composer /bin/composer
composer require phpmailer/phpmailer
#Need to move the vendor dir to the correct location


#Setup NPM Dependencies
NPM_Installation_Directory="/opt/nmp"
mkdir -p ${NPM_Installation_Directory}
cd ${NPM_Installation_Directory}

Popper_JS_Version="1.14.7"
JQuery_Version="3.4.1"
Bootstrap_Version="4.3.1"

npm install popper.js@${Popper_JS_Version} --save
npm install jquery@${JQuery_Version} --save
npm install datatables.net --save 
npm install bootstrap@${Bootstrap_Version} --save
npm install validate.js@0.13.1 --save
npm install underscore@1.10.2 --save
npm install jquery.cookie@1.4.1 --save

#Move Dist To Appropriate Directories
Site_Target_Directory="/var/www/html/npm"
mkdir -P ${Site_Target_Directory}

ln -s ${NPM_Installation_Directory}/node_modules/bootstrap/dist ${Site_Target_Directory}/bootstrap
ln -s ${NPM_Installation_Directory}/node_modules/jquery/dist ${Site_Target_Directory}/jquery
ln -s ${NPM_Installation_Directory}/node_modules/datatables.net/js ${Site_Target_Directory}/datatables.net
ln -s ${NPM_Installation_Directory}/node_modules/popper.js ${Site_Target_Directory}/popper.js
ln -s ${NPM_Installation_Directory}/node_modules/validate.js ${Site_Target_Directory}/validate.js
ln -s ${NPM_Installation_Directory}/node_modules/underscore ${Site_Target_Directory}/underscore
ln -s ${NPM_Installation_Directory}/node_modules/jquery.cookie ${Site_Target_Directory}/jquery.cookie

#Download aditional boopstrap components
wget -O "${Site_Target_Directory}/bootstrap/css/bootstrap-toggle.min.css" https://gitcdn.github.io/bootstrap-toggle/2.2.2/css/bootstrap-toggle.min.css
wget -O "${Site_Target_Directory}/bootstrap/js/bootstrap-toggle.min.js" https://gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min.js

#Setup below is for uploads to be allowed

#Directory Setup
#mkdir -p /var/www/html/img/Animals
#chown apache:apache /var/www/html/img/Animals
#chmod 755 /var/www/html/img/Animals
#Set Selinux properties
#sed -ie 's|SELINUX=enforcing|SELINUX=disabled|g' /etc/selinux/config
setsebool -P httpd_can_network_connect=1

#Selinux allow file upload
#semanage fcontext -a -t httpd_sys_rw_content_t '/tmp'
#restorecon -Rv '/tmp'
#semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/img/Animals'
#restorecon -Rv '/var/www/html/img/Animals'

