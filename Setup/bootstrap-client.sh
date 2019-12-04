#!/usr/bin/env bash

apt-get -y install dictionaries-common
apt-get -y install xfce4
apt-get -y install firefox
apt-get -y install python3
apt-get -y install python3-pip
apt-get -y install python3-dev libffi-dev build-essential virtualenvwrapper
pip3 install virtualenvwrapper
source "/usr/bin/virtualenvwrapper.sh"
export WORKON_HOME="/opt/virtual_env/"
mkvirtualenv --python=$(which python3) angr && python3 -m pip install angr
