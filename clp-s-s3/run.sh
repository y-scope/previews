#!/usr/bin/env bash

# Exit on any error and treat unset variables as errors
set -e
set -u

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
container_name=$USER-$(cat "$script_dir/container-name")

docker run \
    --rm \
    -it \
    --network host \
    --name "$container_name" \
    --env UID="$(id -u)" \
    --env GID="$(id -g)" \
    --mount "type=bind,src=$(readlink -f ~),dst=$(readlink -f ~)" \
    "$container_name" \
    /bin/bash -l
