#!/usr/bin/env bash

# Exit on error and treat unset variables as errors
set -e
set -u

if [ "$UID" != 0 ] ; then
    set -- sudo -u "$DOCKER_USER" "${@}"
fi

exec "$@"
