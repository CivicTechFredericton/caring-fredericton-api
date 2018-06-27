import boto3
from core import errors

import logging

logger = logging.getLogger(__name__)


def upload_file(bucket_name, file_path, content, content_type, acl=''):
    """
    Uploads smaller files (under 15MB) to an S3 bucket
    :param bucket_name: The name of the S3 bucket
    :param file_path: The path to the file to be uploaded which maps to the lookup key
    :param content: The file contents
    :param content_type: The type of file being uploaded
    :param acl: The ACL (access control lists) value for the visibility of the file in the bucket;
    default is authenticated_read
    """
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)

        if not acl:
            acl = 'authenticated-read'

        bucket.put_object(
            Key=file_path,
            Body=content,
            ACL=acl,
            ContentType=content_type
        )
    except Exception:
        logger.exception('Error uploading file to S3')
        raise errors.S3Error()


def get_bucket_contents(bucket_name, prefix='', suffix=''):
    """
    Generate the keys in an S3 bucket
    :param bucket_name: The name of the S3 bucket
    :param prefix: Filter for keys that start with this prefix (optional)
    :param suffix: Filter for keys that end with this suffix (optional)
    :return A generator object that can be used to iterate over
    """
    for obj in get_matching_s3_objects(bucket_name, prefix, suffix):
        yield obj['Key']


def get_matching_s3_objects(bucket_name, prefix='', suffix=''):
    """
    Generate objects in an S3 bucket
    :param bucket_name: The name of the S3 bucket
    :param prefix: Filter for keys that start with this prefix (optional)
    :param suffix: Filter for keys that end with this suffix (optional)
    :return A generator object that can be used to iterate over
    """
    s3 = boto3.client('s3')
    kwargs = {'Bucket': bucket_name}

    # If the prefix is a single string (not a tuple of strings), apply the filter
    if isinstance(prefix, str):
        kwargs['Prefix'] = prefix

    while True:
        resp = s3.list_objects_v2(**kwargs)

        try:
            contents = resp['Contents']
        except KeyError:
            logger.exception('Error reading from the S3 bucket %s', bucket_name)
            raise errors.S3Error()

        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix) and key.endswith(suffix):
                yield obj

        # Pass the continuation token if there are more than 1000 keys
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break


def generate_redirect_url(bucket_name, file_path, private_url_expiration):
    """
    Generates a redirection link for the file stored in S3
    :param bucket_name: The name of the bucket
    :param file_path: The key of the file
    :param private_url_expiration: The URL expiration
    :return The generated URL providing temporary access to the file
    """
    try:
        s3_client = boto3.client('s3')

        return s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                "Bucket": bucket_name,
                "Key": file_path
            },
            ExpiresIn=private_url_expiration
        )
    except Exception:
        logger.exception('Error generating private S3 URL')
        raise errors.S3Error()

