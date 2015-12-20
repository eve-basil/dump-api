#!/bin/sh
apt-get install -y python-dev python-mysqldb git tmux fail2ban vim

wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
rm get-pip.py

pip install --force-reinstall --upgrade cython
pip install --force-reinstall --upgrade falcon
pip install -r requirements.txt
