#!/bin/bash

CONTAINER_NAME="${USER}_overlaptransformer"

docker exec --user "docker_overlaptransformer" -it ${CONTAINER_NAME} \
    /bin/bash -c "cd /home/docker_overlaptransformer; echo ${CONTAINER_NAME} container; echo ; /bin/bash"