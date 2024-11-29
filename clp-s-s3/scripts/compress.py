#!/usr/bin/env python3

import boto3
import argparse
import sys
from urllib.parse import urlparse
from pathlib import Path
import subprocess
from dataclasses import dataclass
from botocore.client import ClientError
import json
import os


@dataclass
class CompressionArgs:
    path: str
    is_url: bool
    bucket: str
    timestamp_key: str

def get_credentials():
    session = boto3.Session()
    credentials = session.get_credentials()
    frozen_credentials = credentials.get_frozen_credentials()
    return frozen_credentials.access_key, frozen_credentials.secret_key


def run_clp(args: CompressionArgs):
    cmd = [
        "./clp-s",
        "c",
        "working_dir",
        args.path,
        "--single-file-archive",
        "--print-archive-stats",
        "--timestamp-key", args.timestamp_key
    ]

    cmd.append("--input-source")
    if args.is_url:
        cmd.append("s3")
    else:
        cmd.append("filesystem")

    access_key, secret_key = get_credentials()
    env = os.environ.copy()
    env["AWS_ACCESS_KEY_ID"] = access_key
    env["AWS_SECRET_ACCESS_KEY"] = secret_key

    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(args.bucket)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)

    while True:
        line = process.stdout.readline()
        if not line:
            break

        stats = json.loads(line.decode('ascii'))
        id = stats["id"]
        archive_path = Path("working_dir") / id
        with open(str(archive_path), 'rb') as data:
            bucket.upload_fileobj(data, id)
        archive_path.unlink()

    rc = process.wait()
    if 0 != rc:
        print(f"Failed compression, return_code={str(rc)}", file=sys.stderr)
        return rc
    return 0

def validate_path(path: str):
    try:
        local_path = Path(path)
        if local_path.exists():
            return False
    except Exception:
        pass

    try:
        parsed_url = urlparse(path)
        if parsed_url.scheme not in ["http", "https"]:
            raise ValueError(
                f"Provided URL must be http or https, but was of type {parsed_url.scheme}."
            )
        return True
    except Exception:
        raise
    
def validate_args(parsed_args):
    is_url = validate_path(parsed_args.path)

    try:
        s3_resource = boto3.resource("s3")
        s3_resource.meta.client.head_bucket(Bucket=parsed_args.destination_bucket)
    except ClientError as e:
        raise ValueError(
            f"Could not access bucket {parsed_args.destination_bucket}."
            f" Encountered exception: {str(e)}."
        )

    return CompressionArgs(
        path=parsed_args.path,
        is_url=is_url,
        bucket=parsed_args.destination_bucket,
        timestamp_key=parsed_args.timestamp_key
    )

def main(argv):
    args_parser = argparse.ArgumentParser(
        description=(
            "Compresses a single file from S3 or the local filesystem and stores it in an existing"
            " S3 bucket."
        )
    )

    args_parser.add_argument(
        "path",
        type=str,
        help="S3 object URL or local filesystem path for the file to be compressed."
    )

    args_parser.add_argument(
        "--destination-bucket",
        type=str,
        required=True,
        help="Existing S3 bucket that compressed archives should be uploaded to."
    )

    args_parser.add_argument(
        "--timestamp-key",
        type=str,
        required=True,
        help="Key name of the authoritative timestamp field for the file being compressed."
    )

    parsed_args = args_parser.parse_args(argv[1:])
    try:
        validated_args = validate_args(parsed_args)
    except Exception as e:
        print(f"Invalid arguments: {str(e)}", file=sys.stderr)
        return -1

    return run_clp(validated_args)

if "__main__" == __name__:
    sys.exit(main(sys.argv))
