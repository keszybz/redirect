#!/bin/bash
export CAROOT="$(dirname $0)/ssl"
mkdir -p "$CAROOT"
mkcert -install
mkcert openai.com "*.openai.com" localhost 127.0.0.1 ::1

