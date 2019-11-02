#!/usr/bin/env bash

# install nginx
apt-get -y install dictionaries-common
apt-get -y install xfce4
apt-get -y install firefox



echo 'mysql-server mysql-server/root_password password toor' | debconf-set-selections
echo 'mysql-server mysql-server/root_password_again password toor' | debconf-set-selections

apt-get -y install mysql-server

startxfce4&