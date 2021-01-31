from typing import List, Union
import json

from ..models import presigned_url_contract
from ..daos import AwsS3Dao


class AwsS3Service:
    _dao = AwsS3Dao()

    @classmethod
    def get_file(cls, filename: str) -> bytes:
        """
        Gets a file from S3

        :param filename: The name of the file to get
        :return: The file contents as bytes
        """
        return cls._dao.get_file(filename=filename)

    @classmethod
    def copy_file(cls, old_filename: str, new_filename: str) -> None:
        """
        Copies a file in S3

        :param old_filename: The name of the file to move
        :param new_filename: The name of the new file
        """
        cls._dao.copy_file(old_filename=old_filename, new_filename=new_filename)

    @classmethod
    def delete_file(cls, filename: str) -> None:
        """
        Deletes a file in S3

        :param filename: The S3 filename/key
        """
        cls._dao.delete_file(filename=filename)

    @classmethod
    def rename_file(cls, old_filename: str, new_filename: str) -> None:
        """
        Renames/moves a file in S3

        :param old_filename: The name of the file to move
        :param new_filename: The name of the new file
        """
        cls._dao.rename_file(old_filename=old_filename, new_filename=new_filename)

    @classmethod
    def create_file(cls, filename: str, contents: bytes) -> dict:
        """
        Creates a file in S3

        :param filename: The S3 filename/key for the URL
        :param contents: The file contents
        :return: The response object with creation details from S3
        """
        return cls._dao.create_file(filename=filename, contents=contents)

    @classmethod
    def list_files(cls, directory: str = None) -> List[str]:
        """
        Lists files in S3

        :param directory: The S3 directory to list. Defaults to the top level directory.
        :return: A list of filenames in the given directory
        """
        return cls._dao.list_files(directory=directory)

    @classmethod
    def generate_presigned_url(
        cls, filename: str, expiration: int = None
    ) -> presigned_url_contract:
        """
        Generates a presigned URL for a GET request

        :param filename: The S3 filename/key for the URL
        :param expiration: The expiration time for the URL in seconds. Defaults to `cls.DEFAULT_EXPIRATION`.
        :return: A PresignedUrlContract containing the information to GET the file contents in S3
        """
        return cls._dao.generate_presigned_url(filename=filename, expiration=expiration)

    @classmethod
    def generate_presigned_post(
        cls, filename: str, expiration: int = None
    ) -> presigned_url_contract:
        """
        Generates a presigned URL for a POST request

        :param filename: The S3 filename/key for the URL
        :param expiration: The expiration time for the URL in seconds. Defaults to `cls.DEFAULT_EXPIRATION`.
        :return: A PresignedUrlContract containing the information to POST to the filename in S3
        """
        return cls._dao.generate_presigned_post(
            filename=filename, expiration=expiration
        )
