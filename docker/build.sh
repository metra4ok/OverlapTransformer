#!/bin/bash

orange=`tput setaf 3`
reset_color=`tput sgr0`

ARCH=`uname -m`

ROOT_DIR=$(cd ./"`dirname $0`" || exit; pwd)
cd $ROOT_DIR

echo "Building for ${orange}${ARCH}${reset_color}"

docker build ../. \
    -f ${ROOT_DIR}/Dockerfile.${ARCH} \
    --build-arg UID=$(id -u) \
    --build-arg GID=$(id -g) \
    -t overlaptransformer:latest