import boto3
import os
from botocore.exceptions import ClientError

def put_object(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket using put_object
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    
    # Read file content
    with open(file_name, 'rb') as file:
        file_content = file.read()
    
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=file_content)
    except ClientError as e:
        print(f"Error uploading file: {e}")
        return False
    return True

def get_object(bucket, object_name, file_name):
    """Download a file from an S3 bucket using get_object
    :param bucket: Bucket to download from
    :param object_name: S3 object name to download
    :param file_name: Local file name to save the downloaded file
    :return: True if file was downloaded, else False
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.get_object(Bucket=bucket, Key=object_name)
        content = response['Body'].read()
        with open(file_name, 'wb') as file:
            file.write(content)
    except ClientError as e:
        print(f"Error downloading file: {e}")
        return False
    return True

# Example usage
bucket_name = 'cmnd-blinx-config-data-embeddings'
file_to_upload = 'test.txt'
s3_object_name = 'test.txt'

# Upload
if put_object(file_to_upload, bucket_name, s3_object_name):
    print(f"Successfully uploaded {file_to_upload} to {bucket_name}/{s3_object_name}")

# Download
download_path = 'file.txt'
if get_object(bucket_name, s3_object_name, download_path):
    print(f"Successfully downloaded {bucket_name}/{s3_object_name} to {download_path}")