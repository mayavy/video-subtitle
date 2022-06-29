"""Configuration file for Amazon Web Services variables and Classes required by the Project."""

import os
import dotenv
from boto3 import Session
from storages.backends.s3boto3 import S3Boto3Storage

dotenv.read_dotenv()

AWS_MEDIA_DIR = 'media/'
AWS_STATIC_DIR = 'static/'

class StaticStorage(S3Boto3Storage):
    """ Class for storing static files on AWS-S3 bucket when collectstatic is called."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = self.location+ AWS_STATIC_DIR
        


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')



AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_DEFAULT_ACL = None

# boto3 AWS session
session = Session(region_name = 'ap-south-1',
        aws_access_key_id= AWS_ACCESS_KEY_ID,
        aws_secret_access_key= AWS_SECRET_ACCESS_KEY)

s3_client = session.client('s3')

def aws_downloader(path:str, filename:str):
    """
    Generates temporary url for filestored in AWS-s3 bucket
    return::str
    """
    temp_url = s3_client.generate_presigned_url(ClientMethod='get_object',
                                                    Params={'Bucket': AWS_STORAGE_BUCKET_NAME,
                                                            'Key':f'{path}{filename}'},
                                                    ExpiresIn=600)
    return temp_url

