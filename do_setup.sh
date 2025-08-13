#!/bin/bash

cd $(dirname $0)

./create_ssl_setup.sh

cp ./chatgpt-guard.service /etc/systemd/system/
cp ./chatgpt-guard.socket /etc/systemd/system/
cp ./chatgpt-guard-ssl.servit /etc/systemd/system/
cp ./chatgpt-guard-ssl.sockt /etc/systemd/system/

systemctl daemon-reload

systemctl enable chatgpt-guard.socket chatgpt-guard-ssl.socket
systemctl restart chatgpt-guard.service chatgpt-guard-ssl.service

if ! grep -q openai.com /etc/hosts; then
    cat >>/etc/hosts <<EOF
127.0.0.1 openai.com
127.0.0.1 chatgpt.com
127.0.0.1 chat.openai.com
127.0.0.1 auth.openai.com
EOF
fi
