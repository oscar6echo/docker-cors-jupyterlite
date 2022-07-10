#!/bin/bash

cd ..

IMG_LOCAL=jlite-cors:local

# docker rmi $IMG_LOCAL
# docker build --no-cache -t $IMG_LOCAL .
# docker build --no-cache --progress=plain -t $IMG_LOCAL .
# docker build --progress=plain -t $IMG_LOCAL .
docker build -t $IMG_LOCAL .

cd scripts || exit
