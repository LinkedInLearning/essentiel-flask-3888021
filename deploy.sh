#!/bin/bash

#            +---------+             +-------------------+   
#            |         |             |           +------------+  
#  --------> |  NGINX  | ----------> | Gunicorn  |  Portfolio |  
#   http:80  |         |  http:8000  |           |            |
#  <-------- | (proxy) | <---------- |  (wsgi)   |   (flask)  |
#            |         |             |           +------------+
#            +---------+             +-------------------+     
#                                           ^
#                                           |
#                                    +--------------+
#                                    |  Supervisor  |
#                                    | (monitoring) |
#                                    +--------------+

if [ -z "$1" ]; then
    echo "Usage: $0 <email>"
    exit 1
fi

ARG_EMAIL=$1
CHEMIN=$(pwd)
USER=$(stat -c '%U' $CHEMIN)
APP=portfolio
DOMAINE=portfolio.example

echo ~~~ Paquets ~~~

apt-get -y install build-essential libssl-dev libffi-dev\
 python3-pip python3-dev python3-setuptools python3-venv\
 supervisor nginx

echo ~~~ App. flask ~~~

function secret() {
    VAR=$1
    SECRET=$(printf '%s\n' $(openssl rand -base64 32) | sed -e 's/[]\/$*.^[]/\\&/g')

    sed -i "s/^$VAR = .*$/$VAR = '$SECRET'/" $CHEMIN/instance/config.py
}

sudo -u $USER python3 -m venv .venv

chmod +x setup.sh
sudo -u $USER ./setup.sh

sed -i "s/^ADMIN_MAIL = .*$/ADMIN_MAIL = '$ARG_EMAIL'/" $CHEMIN/instance/config.py
secret SECRET_KEY
secret CSRF_SECRET
secret SECURITY_PASSWORD_SALT
secret JWT_SECRET_KEY

MOTDEPASSE=$(openssl rand -base64 12)

sudo -u $USER .venv/bin/flask users change_password $ARG_EMAIL --password $MOTDEPASSE

echo ~~~ Gunicorn ~~~

sudo -u $USER .venv/bin/pip install gunicorn

echo ~~~ Supervisor ~~~~

mkdir -p /var/log/$APP
tee /etc/supervisor/conf.d/$APP.conf > /dev/null <<EOT
[program:$APP]
command=$CHEMIN/.venv/bin/gunicorn --bind 127.0.0.1:8000 'app:create_app()' 
directory=$CHEMIN
autostart=true
autorestart=true
user=$USER
stderr_logfile=/var/log/$APP/err.log
stdout_logfile=/var/log/$APP/out.log
EOT
service supervisor start

echo ~~~ Nginx ~~~

tee /etc/nginx/sites-available/$APP > /dev/null <<EOT
server {
    listen 80;
    server_name $DOMAINE www.$DOMAINE;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOT
ln -s /etc/nginx/sites-available/$APP /etc/nginx/sites-enabled

service nginx restart

echo ~~~ Admin : $ARG_EMAIL / $MOTDEPASSE ~~~
