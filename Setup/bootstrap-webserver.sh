#!/usr/bin/env bash

# install nginx
apt-get -y install nginx

cp -f /home/vagrant/website/nginx.conf /etc/nginx/nginx.conf
cp -f /home/vagrant/website/default-site /etc/nginx/sites-available/ScoreboardServer
rm -rf /var/www/html
cp -rf /home/vagrant/website/html /var/www/

ln -sf /etc/nginx/sites-available/ScoreboardServer /etc/nginx/sites-enabled/
unlink /etc/nginx/sites-enabled/default

echo 'mysql-server mysql-server/root_password password toor' | debconf-set-selections
echo 'mysql-server mysql-server/root_password_again password toor' | debconf-set-selections

apt-get -y install mysql-server

mysql -u root -ptoor < /home/vagrant/website/setup.sql


apt-get -y install software-properties-common
add-apt-repository ppa:ondrej/php
apt-get update
apt install php7.3-fpm php7.3-common php7.3-mysql php7.3-xml php7.3-xmlrpc php7.3-curl php7.3-gd php7.3-imagick php7.3-cli php7.3-dev php7.3-imap php7.3-mbstring php7.3-opcache php7.3-soap php7.3-zip unzip -y
update-alternatives --set php /usr/bin/php7.3

nginx -s reload
systemctl reload nginx

#create certificates
cd /home/vagrant/
mkdir httpsCert
cd httpsCert

openssl genrsa -out privatekey.pem
openssl req -new -x509 -key privatekey.pem -out publickey.cer -days 365 -subj "/C=PT/ST=Lisbon/L=Oeiras/O=IST_SIRS2019/OU=Proj/CN=scoreboardWeb/emailAddress=mail@mail.mail"
openssl x509 -x509toreq -days 365 -in publickey.cer -signkey privatekey.pem -out ca.req
openssl x509 -req -days 365 -in ca.req -signkey privatekey.pem -out server.crt
chmod 400 privatekey.pem


cd /home/vagrant/
mkdir customCert
cd customCert
openssl genrsa -out privatekey.pem
openssl req -new -x509 -key privatekey.pem -out publickey.cer -days 365 -subj "/C=PT/ST=Lisbon/L=Oeiras/O=IST_SIRS2019/OU=Proj/CN=scoreboardCustom/emailAddress=mail@mail.mail"
openssl x509 -x509toreq -days 365 -in publickey.cer -signkey privatekey.pem -out ca.req
openssl x509 -req -days 365 -in ca.req -signkey privatekey.pem -out server.crt