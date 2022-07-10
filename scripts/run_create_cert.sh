#!/bin/bash

mkdir -p ../certs

cd ../certs || exit

mkcert -install

mkcert \
    -cert-file tls-localhost.crt \
    -key-file tls-localhost.key \
    localhost \
    127.0.0.1 \
    ::1

cd ../scripts || exit
