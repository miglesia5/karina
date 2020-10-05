#!/usr/bin/env bash

apt update && apt upgrade

hostnamectl set-hostname klDesign
hostname

nano /etc/hosts
# add ip and hostname
159.89.146.106 klDesign

adduser manuiglesias ##any user

adduser manuiglesias sudo

mkdir .ssh

#computer
ssh-keygen -b 4096

scp ~/.ssh/id_rsa.pub manuiglesias@159.89.146.106:~/.ssh/authorized_keys



#server
ls .ssh

sudo chmod 700 ~/.ssh/
sudo chmod 600 ~/.ssh/*

sudo nano /etc/ssh/sshd_config

sudo systemctl restart sshd

sudo apt install ufw

sudo ufw default allow outgoing

sudo ufw default deny incoming

sudo ufw allow ssh

sudo ufw allow 5000

sudo ufw enable

##Computer
scp -r Desktop/karinalorancastudios manuiglesias@159.89.146.106:~/


## Server

sudo apt install python3-pip

sudo apt install python3-venv

python3 -m venv karinalorancastudios/venv

source venv/bin/activate

pip install -r requirements.txt


sudo touch /etc/config.json

sudo nano /etc/config.json


sudo nano kl_designs/config.py

import os
import json


with open('/etc/config.json') as config_file:
    config = json.load(config_file)


class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SLL = False
    MAIL_USERNAME = config.get('MAIL_USERNAME')
    MAIL_PASSWORD = config.get('MAIL_PASSWORD')


#####################
export FLASK_APP=run.py
flask run --host=0.0.0.0


sudo apt install nginx
pip install gunicorn

sudo rm /etc/nginx/sites-enabled/default

sudo nano /etc/nginx/sites-enabled/kldesign

server {
    listen 80;
    server_name 157.245.190.191;

    location /static {
        alias /home/manuiglesias/karinalorancastudios/kl_designs/static;
    }

    location / {
        proxy_pass http://localhost:8000;
        include /etc/nginx/proxy_params;
        proxy_redirect off;
    }
}


sudo ufw allow http/tcp

sudo ufw delete allow 5000

sudo ufw enable

sudo systemctl restart nginx

gunicorn -w 3 run:app


sudo apt install supervisor


sudo nano /etc/supervisor/conf.d/kl_designs.conf


[program:kl_designs]
directory=/home/manuiglesias/karinalorancastudios
command=/home/manuiglesias/karinalorancastudios/venv/bin/gunicorn -w 3 run:app
user=manuiglesias
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/kl_designs/kl_designs.err.log
stdout_logfile=/var/log/kl_designs/kl_designs.out.log

sudo mkdir -p /var/log/kl_designs

sudo touch /var/log/kl_designs.err.log

sudo touch /var/log/kl_designs.out.log

sudo supervisorctl reload

##########

SET UP DOMAIN NAME

#########

    sudo apt-get update
    sudo apt-get install software-properties-common
    sudo add-apt-repository universe
    sudo add-apt-repository ppa:certbot/certbot
    sudo apt-get update

    sudo apt-get install certbot python3-certbot-nginx

    sudo nano /etc/nginx/sites-enabled/kldesign

    sudo certbot --nginx

    sudo certbot certonly --nginx


sudo certbot renew --dry-run

sudo ufw allow https

sudo crontab -e
30 4 1 * * sudo certbot renew --quiet





# Consider running these two commands separately
# Do a reboot before continuing.
#apt update
#apt upgrade -y

#apt install zsh
#sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install some OS dependencies:
#sudo apt-get install -y -q build-essential git unzip zip nload tree
#sudo apt-get install -y -q python3-pip python3-dev python3-venv
#sudo apt-get install -y -q nginx
# for gzip support in uwsgi
#sudo apt-get install --no-install-recommends -y -q libpcre3-dev libz-dev

# Stop the hackers
#sudo apt install fail2ban -y

#ufw allow 22
#ufw allow 80
#ufw allow 443
#ufw enable

# Basic git setup
#git config --global credential.helper cache
#git config --global credential.helper 'cache --timeout=720000'

# Be sure to put your info here:
#git config --global user.email "you@email.com"
#git config --global user.name "Your name"

# Web KL_designs file structure
#mkdir /KLdesisngs
#chmod 777 /KLdesisngs
#mkdir /KLdesisngs/logs
#mkdir /KLdesisngs/logs/kl_designs
#mkdir /KLdesisngs/logs/kl_designs/kldesigns_log
#cd /KLdesisngs

# Create a virtual env for the KL_designs.
#cd /KLdesisngs
#python3 -m venv venv
#source /KLdesisngs/venv/bin/activate
#pip install --upgrade pip setuptools
#pip install --upgrade httpie glances
#pip install --upgrade uwsgi


# clone the repo:
#cd /apps
#cd /KLdesisngs
# ➜  /KLdesisngs . venv/bin/activate

#git clone https://github.com/miglesia5/KLdesigns2.git app_repo
#git clone https://github.com/talkpython/data-driven-web-KLdesisngs-with-flask app_repo

# Setup the web KL_designs:
#cd cd /KLdesisngs/app_repo/KL_designs2/kl_designs/
#pip install -r requirements.txt

# Copy and enable the daemon
#cp /KLdesisngs/app_repo/kl_designs/server/kl_designs.service /etc/systemd/system/kl_designs.service


#systemctl start kl_designs
#systemctl status kl_designs
#systemctl enable kl_designs

# Setup the public facing server (NGINX)
#apt install nginx

# CAREFUL HERE. If you are using default, maybe skip this
#rm /etc/nginx/sites-enabled/default

#cp /KLdesisngs/app_repo/kl_designs/server/kl_designs.nginx /etc/nginx/sites-enabled/kl_designs.nginx
#update-rc.d nginx enable
#service nginx restart


# Optionally add SSL support via Let's Encrypt:
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04

#add-apt-repository ppa:certbot/certbot
#apt install python-certbot-nginx
#certbot --nginx -d fakekl_designs.talkpython.com
