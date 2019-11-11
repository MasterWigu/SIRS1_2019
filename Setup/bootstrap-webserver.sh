#!/usr/bin/env bash

# install nginx
apt-get -y install nginx

cp -f /home/vagrant/website/nginx.conf /etc/nginx/nginx.conf
cp -f /home/vagrant/website/default-site /etc/nginx/sites-available/default
cp -rf /home/vagrant/website/html /usr/share/nginx/

echo 'mysql-server mysql-server/root_password password toor' | debconf-set-selections
echo 'mysql-server mysql-server/root_password_again password toor' | debconf-set-selections

apt-get -y install mysql-server

mysql -u root -ptoor < /home/vagrant/website/setup.sql


apt-get -y install software-properties-common
add-apt-repository ppa:ondrej/php
apt-get update
apt-get -y install php7.3
apt-get -y install php-pear php7.3-curl php7.3-dev php7.3-gd php7.3-mbstring php7.3-zip php7.3-mysql php7.3-xml
update-alternatives --set php /usr/bin/php7.3


#create certificates
cd /home/vagrant
mkdir httpsCert
cd httpsCert

openssl genrsa -out privatekey.pem 2048 -noout
openssl req -new -x509 -key privatekey.pem -out publickey.cer -days 365 -subj "/C=PT/ST=Lisbon/L=Oeiras/O=IST_SIRS2019/OU=Proj/CN=scoreboardWeb/emailAddress=mail@mail.mail"
openssl x509 -x509toreq -days 365 -in publickey.cer -signkey privatekey.pem -out ca.req
openssl x509 -req -days 365 -in ca.req -signkey privatekey.pem -out server.crt

cd ..
mkdir customCert
cd customCert
openssl genrsa -out privatekey.pem 2048 -noout
openssl req -new -x509 -key privatekey.pem -out publickey.cer -days 365 -subj "/C=PT/ST=Lisbon/L=Oeiras/O=IST_SIRS2019/OU=Proj/CN=scoreboardCustom/emailAddress=mail@mail.mail"
openssl x509 -x509toreq -days 365 -in publickey.cer -signkey privatekey.pem -out ca.req
openssl x509 -req -days 365 -in ca.req -signkey privatekey.pem -out server.crt

service nginx restart
