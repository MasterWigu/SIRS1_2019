#!/usr/bin/env bash

apt-get update
apt-get -y install dictionaries-common
apt-get -y install xfce4
apt-get -y install xfce-desktop
apt-get -y install firefox
apt-get -y install python3
apt-get -y install python3-pip
apt-get -y install python3-dev libffi-dev build-essential virtualenvwrapper
pip3 install virtualenvwrapper
export WORKON_HOME="/opt/virtual_env/"

cp -f /home/vagrant/client/interfaces_client.yaml /etc/netplan/60-gateway.yaml
netplan apply

echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
source "/usr/local/bin/virtualenvwrapper.sh"
source /home/vagrant/.bashrc
su vagrant
source "/usr/local/bin/virtualenvwrapper.sh"
source /home/vagrant/.bashrc


cp -f /home/vagrant/client/xprofile /home/vagrant/.xprofile
