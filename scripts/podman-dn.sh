#!/bin/bash
set +x

NETWORK_NAME=ui-mongo-network

if podman network exists ${NETWORK_NAME}; then
    podman pod kill mongo
    podman pod rm mongo 
    podman pod kill prometheus
    podman pod rm prometheus
    podman network rm ${NETWORK_NAME}
else
    echo "${NETWORK_NAME} does not exists... exiting..."
fi