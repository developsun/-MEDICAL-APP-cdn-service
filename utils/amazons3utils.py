import os
from pathlib import Path
from decouple import config
import boto3
import logging
from botocore.exceptions import ClientError


BASE_DIR = Path(__file__).resolve().parent
BUCKET_NAME = config('AWS_BUCKET_NAME')
AWS_S3_CREDS = {
    "aws_access_key_id": config('AWS_ACCESS_KEY_ID'),
    "aws_secret_access_key": config('AWS_SECRET_ACCESS_KEY'),
}
s3_client = boto3.client('s3', **AWS_S3_CREDS, region_name='ap-south-1')


def upload_to_s3_bucket(object_name=None):

    try:
        s3_client.upload_file(
            object_name,
            BUCKET_NAME,
            object_name,
            ExtraArgs={'ACL': 'public-read'}
        )
        os.remove(object_name)

    except ClientError as e:
        logging.error(e)
        return False

    return True


def create_presigned_url(object_name, expiration=3600):

    # Generate a presigned URL for the S3 object
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': BUCKET_NAME,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response