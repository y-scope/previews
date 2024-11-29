#!/usr/bin/env python3

import boto3
import argparse
import sys
from urllib.parse import quote
import subprocess
from dataclasses import dataclass
from botocore.client import ClientError
import os


@dataclass
class SearchArgs:
    query: str
    bucket: str

def get_credentials():
    session = boto3.Session()
    credentials = session.get_credentials()
    frozen_credentials = credentials.get_frozen_credentials()
    return frozen_credentials.access_key, frozen_credentials.secret_key

def run_clp(args: SearchArgs):
    base_cmd = [
        "./clp-s",
        "s", "<url>", args.query,
        "--input-source", "s3",
        "--archive-id", "<id>"
    ]

    access_key, secret_key = get_credentials()
    env = os.environ.copy()
    env["AWS_ACCESS_KEY_ID"] = access_key
    env["AWS_SECRET_ACCESS_KEY"] = secret_key

    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(args.bucket)
    location = boto3.client("s3").get_bucket_location(Bucket=args.bucket)["LocationConstraint"]

    for obj in bucket.objects.all():
        url = (
            f"https://{args.bucket}.s3.{location}.amazonaws.com/"
            f"""{quote(obj.key, safe="~()*!.'")}"""
        )
        cmd = base_cmd
        cmd[2] = url
        cmd[-1] = obj.key
        proc = subprocess.Popen(cmd, env=env)
        proc.communicate()
        if proc.returncode != 0:
            print(
                f"Exited with non-zero status {proc.returncode} while searching object {obj.key}",
                file=sys.stderr
            )

    return 0
    
def validate_args(parsed_args):
    try:
        s3_resource = boto3.resource("s3")
        s3_resource.meta.client.head_bucket(Bucket=parsed_args.bucket)
    except ClientError as e:
        raise ValueError(
            f"Could not access bucket {parsed_args.bucket}. Encountered exception: {str(e)}."
        )

    return SearchArgs(
        query=parsed_args.query,
        bucket=parsed_args.bucket
    )

def main(argv):
    args_parser = argparse.ArgumentParser(
        description="Executes a search query against all archives in an S3 bucket."
    )

    args_parser.add_argument(
        "query",
        type=str,
        help="KQL query to run against the compressed archives."
    )

    args_parser.add_argument(
        "--bucket",
        type=str,
        required=True,
        help="S3 bucket containing the compressed archives."
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
