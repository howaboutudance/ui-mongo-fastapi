#!/bin/bash
set +x

# create network if needed
podman network create ui-mongo-network

# create mongo server
podman pod create \
    --network=ui-mongo-network \
    -n mongo \
    -p 27017:27017

podman run -dt --pod mongo \
    -v ./scripts/data/mongodb:/data/db:z \
    docker.io/mongo:3

podman pod create \
    --network=ui-mongo-network \
    -n prometheus \
    -p 9090:9090

podman run -dt --pod prometheus \
    docker.io/prom/prometheus