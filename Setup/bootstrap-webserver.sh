#!/usr/bin/env bash

# install nginx
apt-get -y install nginx

cp -f /home/vagrant/website/nginx.conf /etc/nginx/nginx.conf
cp -f /home/vagrant/website/default-site /etc/nginx/sites-available/default
cp -f /home/vagrant/website/index.html /usr/share/nginx/html/index.html

service nginx restart
