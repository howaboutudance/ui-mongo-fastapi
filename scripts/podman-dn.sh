#!/bin/bash
set +x

if podman network exists microblogpub-network; then
    podman pod kill mongo
    podman pod rm mongo 
    podman pod kill prometheus
    podman pod rm prometheus
    podman network rm ui-mongo-network
else
    echo "ui-mongo-network does not exists... exiting..."
fi