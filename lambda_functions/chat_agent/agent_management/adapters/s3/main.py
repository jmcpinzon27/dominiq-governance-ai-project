import logging

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

from adapters.s3.config import AWSSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BUCKET_NAME = "html-buckets"  # Reemplaza con el nombre real del bucket en GCP

def upload_content_to_storage(content, bucket_name):
    """Upload content to an S3 bucket.

    :param content: Content to upload (string or bytes)
    :param bucket_name: Bucket to upload to
    :param object_name: S3 object name
    :return: True if content was uploaded, else False
    """
    object_name = '/'
    # Create an S3 client
    session = boto3.Session()
    s3_client = session.client('s3')

    try:
        # Upload the content
        logger.info(f"Successfully uploaded content to {bucket_name}/{object_name}")
        return s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=content)
    except NoCredentialsError:
        logger.warning("Credentials not available.")
    except ClientError as e:
        logger.warning(f"Client error: {e}")


def download_file_from_storage(file_name, bucket_name=BUCKET_NAME):
    """Download a file from an S3 bucket by its name.

    This function downloads a file from an S3 bucket using the provided file name.

    Args:
        file_name: Name of the file in S3 to download
        bucket_name: S3 bucket name (defaults to BUCKET_NAME)

    Returns:
        bytes: The file content if download is successful
        None: If download fails
    """
    # Create an S3 client
    session = boto3.Session()
    s3_client = session.client('s3')

    try:
        # Get the file object
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=file_name
        )

        # Read the file content
        file_content = response['Body'].read()

        logger.info(f"Successfully downloaded file {file_name} from {bucket_name}")
        return file_content
    except NoCredentialsError:
        logger.warning("Credentials not available.")
        return None
    except ClientError as e:
        logger.warning(f"Client error: {e}")
        return None


def download_session_data(session_id):
    """Get a file from S3 storage where the filename contains the session_id.

    This function retrieves a file from S3 storage where the filename is in the format {session_id}_file.

    Args:
        session_id: The session ID to use for retrieving the file
        bucket_name: S3 bucket name (defaults to BUCKET_NAME)

    Returns:
        bytes: The file content if found
        None: If no file is found or download fails
    """
    # Create an S3 client
    session = boto3.Session()
    s3_client = session.client('s3')

    try:
        # Download the object from S3
        response = s3_client.get_object(Bucket=AWSSettings().BUCKET_NAME, Key=session_id)
        return response['Body'].read()  # Read the bytes from the response
        
    except (NoCredentialsError, ClientError) as e:
        
        return None


def upload_session_data(file_content, file_name):
    """Upload a file to S3 and generate a pre-signed URL for downloading.

    This function uploads the provided file content to an S3 bucket and returns
    a pre-signed URL that can be used to download the file. The URL will expire
    after the specified expiration time.

    Args:
        file_content: Content to upload (string or bytes)
        file_name: Name of the file in S3
        bucket_name: S3 bucket name (defaults to BUCKET_NAME)
        expiration: URL expiration time in seconds (default: 1 hour)

    Returns:
        str: Pre-signed URL for downloading the file
        None: If upload fails
    """
    # Create an S3 client
    session = boto3.Session()
    s3_client = session.client('s3')

    try:
        s3_client.put_object(Bucket=AWSSettings().BUCKET_NAME, Key=file_name, Body=file_content)
        
    except (NoCredentialsError, ClientError) as e:
        pass        