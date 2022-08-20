#!/bin/bash

set +x

if command -v "podman"; then
    source scripts/podman-dn.sh
else
    docker-compose dn
fi