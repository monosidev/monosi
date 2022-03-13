import boto3
import os
import logging

from .base import Destination, DestinationConfiguration


class S3DestinationConfiguration(DestinationConfiguration):
    @classmethod
    def validate(cls, configuration):
        raise NotImplementedError

    @classmethod
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "bucket": { "type": "string" },
                "region": { "type": "string" },
                "aws_access_key": { "type": "string" },
                "aws_secret_key": { "type": "string" },
            },
            "secret": [ "aws_secret_key" ],
        }

    def connection_string(self) -> str:
        raise NotImplementedError

    @property
    def type(self):
        return "s3"

class S3Destination(Destination):
    def create_bucket(self, bucket_name, region=None):
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """

        # Create bucket
        try:
            if region is None:
                s3_client = boto3.client('s3')

                response = s3_client.list_buckets()

                # Output the bucket names
                print('Existing buckets:')
                for bucket in response['Buckets']:
                    print(f'  {bucket["Name"]}')

                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_file(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def _push(self):
        raise NotImplementedError

