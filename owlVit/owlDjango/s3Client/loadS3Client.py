import boto3


ACCESS_KEY = ''
SECRET_KEY = ''

bucket_details = {
    "bucket": "",
    "images": "images/",
    "labels": "labels/",
    "bucket_url": "",
    "baseFolder": "test/"
  }


s3_client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

def get_client():
    return s3_client

def get_bucket_details():
    return bucket_details


