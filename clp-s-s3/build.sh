#!/usr/bin/env bash

# Exit on any error and treat unset variables as errors
set -e
set -u

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
container_name=$USER-$(cat "$script_dir"/container-name)

: "${UID:=0}"
: "${GID:=${UID}}"

docker build \
    --build-arg DOCKER_USER="$USER" \
    --build-arg DOCKER_USER_UID="$UID" \
    --build-arg DOCKER_USER_GID="$GID" \
    -t "$container_name" \
    "$script_dir" \
    --file "$script_dir"/Dockerfile
