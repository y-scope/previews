FROM ghcr.io/y-scope/clp/clp-core-dependencies-x86-ubuntu-focal:main

ARG DOCKER_USER=duser
ARG DOCKER_USER_GID=1000
ARG DOCKER_USER_UID=1000

RUN groupadd -g "$DOCKER_USER_GID" "$DOCKER_USER" \
    && useradd -m -b /home/ -s /bin/bash -g "$DOCKER_USER_GID" -u "$DOCKER_USER_UID" "$DOCKER_USER"

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y sudo

RUN echo "$DOCKER_USER ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/"$DOCKER_USER" \
    && chmod 0440 /etc/sudoers.d/"$DOCKER_USER"

COPY files /

RUN chmod a+rx /entrypoint.sh

ENV DOCKER_USER="$DOCKER_USER"

WORKDIR /home/"$DOCKER_USER"

# To install project-specific packages here, add them below
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-venv \
    vim

ENTRYPOINT ["/entrypoint.sh"]
