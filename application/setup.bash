#! /bin/bash
sudo ufw enable
sudo ufw allow openssh
sudo apt update
sudo apt install nginx
sudo ufw allow 'Nginx HTTP'
sudo ufw status
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv
mkdir ~/project
