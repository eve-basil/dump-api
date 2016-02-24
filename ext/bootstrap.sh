#!/bin/sh
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

apt-get update
apt-get install -y python-dev python-mysqldb libyaml-dev tmux vim

wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
rm get-pip.py

pip install --force-reinstall --upgrade cython
pip install --force-reinstall --upgrade falcon
pip install --force-reinstall --upgrade pyyaml
pip install --force-reinstall --upgrade hiredis

if [ -f "requirements.txt" ]
then
    pip install -r requirements.txt
else
    echo "You need to install the contents of requirements.txt. Could not find the file."
fi