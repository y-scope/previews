This package contains everything you should need to preview `clp-s` with S3.

The steps below walk you through basic setup and usage.

# Setup

* Install [Docker]
  * If you're not running as root, ensure `docker` can be run
    [without superuser privileges][non-root-docker].
* Build and entering the docker container using the following commands.

  ```shell
  ./build.sh
  ./run.sh
  ```

  `run.sh` will mount your home directory inside the Docker container. For more information about
  the Docker setup feel free to read `CONTAINER.md`.

* Once inside the container, navigate to the directory containing this README.
* Run the following commands to set up a Python virtual environment.

  ```shell
  cd scripts
  ./setup.sh
  . venv/bin/activate
  ```

  This will create a virtual environment in the `venv` directory and install the necessary
  dependencies for the `search.py` and `compress.py` scripts.

  * If you ever want to leave the venv, run `deactivate`.

* [Set up your AWS credentials][aws-creds] (this may not be necessary if you're running on an EC2
  instance with an IAM role that allows S3 access).

  * These credentials are required for the `search.py` and `compress.py` scripts to function
    correctly.

# Compressing

`compress.py` is designed to compress files either from S3 or the local filesystem and write
archives into an existing S3 bucket.

> [!NOTE]  
> `compress.py` and `search.py` expect you to have the ListBuckets permission for this existing S3
  bucket.

For example, you could run the following command to compress the file `test.log` and write the
resulting archives to the bucket `test-destination`. The `--timestamp-key` parameter specifies which
field is the authoritative timestamp for the dataset you are trying to ingest.

> [!NOTE]
> `compress.py` only accepts S3 Object URLs and local filesystem paths.

```shell
./compress.py https://test.s3.us-east-2.amazonaws.com/test.log \
  --destination-bucket test-destination \
  --timestamp-key '@timestamp'
```

# Searching

`search.py` is designed to execute a [KQL] query against all archives present in a given S3 bucket.
The search results are returned on stdout and any errors from the script are logged to stderr.

> [!NOTE]
> `search.py` only performs single-threaded search.

For example, the following command executes the query `hostname: abc-def` against all archives in
the bucket `test-destination` and redirects the results to the file `results.txt`.

```shell
./search.py 'hostname: abc-def' --bucket test-destination 1> results.txt
```

[aws-creds]: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
[Docker]: https://docs.docker.com/engine/install/
[KQL]: https://docs.yscope.com/clp/main/user-guide/reference-json-search-syntax.html
[non-root-docker]: https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
