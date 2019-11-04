#!/usr/bin/env bash

# install nginx
apt-get -y install nginx

cp -f /home/vagrant/website/nginx.conf /etc/nginx/nginx.conf
cp -f /home/vagrant/website/default-site /etc/nginx/sites-available/default
cp -f /home/vagrant/website/index.html /usr/share/nginx/html/index.html

echo 'mysql-server mysql-server/root_password password toor' | debconf-set-selections
echo 'mysql-server mysql-server/root_password_again password toor' | debconf-set-selections

apt-get -y install mysql-server

mysql -u root -ptoor < /home/vagrant/website/setup.sql

service nginx restart
