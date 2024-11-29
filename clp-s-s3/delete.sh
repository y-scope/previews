#!/usr/bin/env bash

# Exit on any error and treat unset variables as errors
set -e
set -u

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
container_name=$USER-$(cat "$script_dir/container-name")

docker image rm "$container_name"
