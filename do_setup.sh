#!/bin/bash

cd $(dirname $0)

./create_ssl_setup.sh

systemctl link ./chatgpt-guard.service
systemctl link ./chatgpt-guard.socket
systemctl link ./chatgpt-guard-ssl.service
systemctl link ./chatgpt-guard-ssl.socket

systemctl enable --now chatgpt-guard.socket chatgpt-guard-ssl.socket
