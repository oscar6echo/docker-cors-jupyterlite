#!/bin/bash

cd ../src || exit

uvicorn main:app \
    --host 0.0.0.0 \
    --port 8086 \
    --ssl-certfile ../certs/tls-localhost.crt \
    --ssl-keyfile ../certs/tls-localhost.key \
    --reload
