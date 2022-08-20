#!/bin/bash

set +x

if command -v "podman"; then
    source scripts/podman-up.sh
else
   docker-compose -f scripts/docker-compose.yml up 
fi