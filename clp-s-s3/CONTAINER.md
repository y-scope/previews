This directory contains a template for building and running a container that
mimics your user and mounts your home directory in the container. This allows
you to use the container as a clean environment, potentially per project where
the only thing that persists between containers is your home directory.

This README is meant to give you just enough information to use the template;
you can find more details on using Docker online.

# Setup

* Copy the template directory and give it a relevant name.
* Modify `Dockerfile` to add any packages you want to have *persistently*
  installed in the container.
* Modify `container-name` to give your container a relevant name.
* To build the container image, run:

  ```shell
  ./build.sh
  ```

Note that every time you change `Dockerfile`, you will need to rebuild the
container image.

You can see a list of all your container images by running
`docker image ls $USER*`.

# Running

* To start the container:

  ```shell
  ./run.sh
  ```

* To detach from the container (leaving it running): CTRL + p, CTRL + q

* To reattach to the container: source attach.sh

* To stop (and delete) the container, simply exit the shell.

By default, `run.sh` will run the container in such a way that when you exit
the container, it will automatically delete it. If this undesirable, feel free
to change `run.sh` as necessary.

# Deleting

```shell
./delete.sh
```
