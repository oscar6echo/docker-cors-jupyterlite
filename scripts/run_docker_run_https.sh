#!/bin/bash

IMG_LOCAL=jlite-cors:local

docker run \
    -p 8443:8443 \
    --name cors-https \
    --rm \
    --init \
    -e PROXY_HOST=my-proxy-host \
    -e PROXY_PORT=my-proxy-port \
    -e CORS_ORIGINS=https://jupyterlite.readthedocs.io \
    $IMG_LOCAL serve-dev-https



