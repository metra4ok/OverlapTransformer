#!/bin/bash

if [ $# != 1 ]; then
    echo "Usage:
          bash start.sh [DATASETS_DIR]
         "
    exit 1
fi

get_real_path(){
  if [ "${1:0:1}" == "/" ]; then
    echo "$1"
  else
    realpath -m "$PWD"/"$1"
  fi
}

DATASETS_DIR=$(get_real_path "$1")

if [ ! -d $DATASETS_DIR ]
then
    echo "error: DATASETS_DIR=$DATASETS_DIR is not a directory."
exit 1
fi

ROOT_DIR=$(cd ./"`dirname $0`" || exit; pwd)
cd $ROOT_DIR

orange=`tput setaf 3`
reset_color=`tput sgr0`

export ARCH=`uname -m`

echo "Running on ${orange}${ARCH}${reset_color}"

if [ "$ARCH" == "x86_64" ] 
then
    ARGS="--ipc host --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all"
elif [ "$ARCH" == "aarch64" ] 
then
    ARGS="--runtime nvidia"
else
    echo "Arch ${ARCH} not supported"
    exit
fi

CONTAINER_NAME="${USER}_overlaptransformer"

xhost +
    docker run -it -d --rm \
        $ARGS \
        --privileged \
        --name $CONTAINER_NAME \
        --net host \
        --env="DISPLAY=$DISPLAY" \
        --env="QT_X11_NO_MITSHM=1" \
        -v $XAUTH:/root/.Xauthority \
        -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
        -v $ROOT_DIR/../:/home/docker_overlaptransformer/OverlapTransformer:rw \
        -v $DATASETS_DIR:/home/docker_overlaptransformer/Datasets:rw \
        overlaptransformer:latest
xhost -

docker exec --user root \
    $CONTAINER_NAME bash -c "/etc/init.d/ssh start"