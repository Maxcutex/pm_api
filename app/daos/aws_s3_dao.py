from typing import List
import boto3
from botocore.client import Config
import os

from ..utils import Logs
from ..models import presigned_url_contract


LOGGER = Logs.logger("AwsS3Dao")
REGION = os.environ.get("AWS_REGION", None)


class AwsS3Dao:
    DEFAULT_BUCKET = os.environ.get(
        "AWS_BUCKET", "webspoons"
    )  # or get from environment vari
    DEFAULT_EXPIRATION = 20 * 60  # 20 minutes
    _client = boto3.client(
        "s3", config=Config(region_name=REGION, signature_version="s3v4")
    )

    @classmethod
    def get_file(cls, filename: str, bucket: str = None) -> bytes:
        """
        Gets a file from S3

        :param filename: The name of the file to get
        :param bucket: The name of the S3 bucket the file is located in. Defaults to `cls.DEFAULT_BUCKET`.
        :return: The contents of the given filename as bytes
        """
        if bucket is None:
            bucket = cls.DEFAULT_BUCKET

        result = cls._client.get_object(Bucket=bucket, Key=filename)
        content = result["Body"].read()
        return content

    @classmethod
    def copy_file(
        cls, old_filename: str, new_filename: str, bucket: str = None
    ) -> None:
        """
        Copies a file in S3

        :param old_filename: The name of the file to move
        :param new_filename: The name of the new file
        :param bucket: The name of the S3 bucket the file is located in. Defaults to `cls.DEFAULT_BUCKET`.
        """
        if bucket is None:
            bucket = cls.DEFAULT_BUCKET

        copy_source = {"Bucket": bucket, "Key": old_filename}
        cls._client.copy(Bucket=bucket, CopySource=copy_source, Key=new_filename)

    @classmethod
    def delete_file(cls, filename: str, bucket: str = None) -> None:
        """
        Deletes a file in S3

        :param filename: The S3 filename/key
        :param bucket: The name of the S3 bucket the file is located in. Defaults to `cls.DEFAULT_BUCKET`.
        """
        if bucket is None:
            bucket = cls.DEFAULT_BUCKET

        cls._client.delete_object(Bucket=bucket, Key=filename)

    @classmethod
    def rename_file(
        cls, old_filename: str, new_filename: str, bucket: str = None
    ) -> None:
        """
        Renames/moves a file in S3

        :param old_filename: The name of the file to move
        :param new_filename: The name of the new file
        :param bucket: The name of the S3 bucket the file is located in. Defaults to `cls.DEFAULT_BUCKET`.
        """
        if bucket is None:
            bucket = cls.DEFAULT_BUCKET

        cls.copy_file(
            old_filename=old_filename, new_filename=new_filename, bucket=bucket
        )
        cls.delete_file(filename=old_filename, bucket=bucket)

    @classmethod
    def create_file(cls, filename: str, contents: bytes, bucket: str = None) -> dict:
        """
        Creates a file in S3

        :param filename: The S3 filename/key for the URL
        :param contents: The file contents
        :param bucket: The name of the S3 bucket the file is located in. Defaults to `cls.DEFAULT_BUCKET`.
        :return: The response object with creation details from S3
        """
        if bucket is None:
            bucket = cls.DEFAULT_BUCKET

        return cls._client.put_object(Bucket=bucket, Key=filename, Body=contents)

    @classmethod
    def list_files(cls, directory: str = None, bucket: str = None) -> List[str]:
        """
        Lists the files in an S3 bucket path

        :param directory: The S3 directory to list. Defaults to the top level directory.
        :param bucket: The name of the S3 bucket the file is located in. Defaults to `cls.DEFAULT_BUCKET`.
        """
        if bucket is None:
            bucket = cls.DEFAULT_BUCKET

        # Removing leading directory / if it exists because S3 doesn't use that but typical filesystems do
        if directory and directory.startswith("/"):
            directory = directory[1:]
        objects = cls._client.list_objects(Bucket=bucket, Prefix=directory)
        results = [obj["Key"] for obj in objects.get("Contents", [])]
        return results

    @classmethod
    def generate_presigned_url(
        cls, filename: str, expiration: int = None, bucket: str = None
    ) -> presigned_url_contract:
        """
        Generates a presigned URL for a GET request.

        :param filename: The S3 filename/key for the URL
        :param expiration: The expiration time for the URL in seconds. Defaults to `cls.DEFAULT_EXPIRATION`.
        :param bucket: The name of the S3 bucket the file is located in. Defaults to `cls.DEFAULT_BUCKET`.
        """
        if bucket is None:
            bucket = cls.DEFAULT_BUCKET

        if expiration is None:
            expiration = cls.DEFAULT_EXPIRATION

        url = cls._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": filename},
            ExpiresIn=expiration,
            HttpMethod="GET",
        )
        # `url` is just a string with the auth headers appended as URL parameters
        if not url:
            LOGGER.error("Could not generate pre-signed URL; no response received")
            raise ValueError("Could not generate URL; access denied")

        url_info = {"url": url, "fields": {}}
        presigned_url = presigned_url_contract(
            url=url_info["url"], headers=url_info["fields"]
        )
        return presigned_url

    @classmethod
    def generate_presigned_post(
        cls, filename: str, expiration: int = None, bucket: str = None
    ) -> presigned_url_contract:
        """
        Generates a presigned URL for a POST request.

        :param filename: The S3 filename/key for the URL
        :param expiration: The expiration time for the URL in seconds. Defaults to `cls.DEFAULT_EXPIRATION`.
        :param bucket: The name of the S3 bucket the file is located in. Defaults to `cls.DEFAULT_BUCKET`.
        """
        if bucket is None:
            bucket = cls.DEFAULT_BUCKET

        if expiration is None:
            expiration = cls.DEFAULT_EXPIRATION

        url_info = cls._client.generate_presigned_post(
            bucket, filename, ExpiresIn=expiration
        )
        # Example response: {'url': 'https://sarcos.s3.amazonaws.com/', 'fields': {'key': 'xo/logs/serial1234/statistics/statistics-1595598296..301438', 'x-amz-algorithm': 'AWS4-HMAC-SHA256', 'x-amz-credential': 'AKIA45VDPUWC72AIHTCL/20200724/us-east-2/s3/aws4_reuquest', 'x-amz-date': '20200724T134457Z', 'policy': 'eyJleHBpcmF0aW9uIjogIjIwMjAtMDgtMDdUMTE6MDQ6NTdaIiwgImNvbmRpdGlvbnMiiOiBbeyJidWNrZXQiOiAic2FyY29zIn0sIHsia2V5IjogIi94by9sb2dzL3NlcmlhbDEyMzQvc3RhdGlzdGljcy9zdGF0aXN0aWNzLTE1OTU1OTgyOTYuMzAMxNDM4In0sIHsieC1hbXotYWxnb3JpdGhtIjogIkFXUzQtSE1BQy1TSEEyNTYifSwgeyJ4LWFtei1jcmVkZW50aWFsIjogIkFLSUE0NVZEUFVXQzcyQUlIVENwMLzIwMjAwNzI0L3VzLWVhc3QtMi9zMy9hd3M0X3JlcXVlc3QifSwgeyJ4LWFtei1kYXRlIjogIjIwMjAwNzI0VDEzNDQ1N1oifV19', 'x-amz-signature2': '428d8d87c3cbfca909a5dc463b59fbca62ab1000cfd322b3463a972870d6913f'}}

        if not url_info:
            LOGGER.error("Could not generate pre-signed URL; no response received")
            raise ValueError("Could not generate URL; access denied")

        presigned_url = presigned_url_contract(
            url=url_info["url"], headers=url_info["fields"]
        )
        return presigned_url
