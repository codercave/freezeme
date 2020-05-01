import boto3
import botocore
from freezeme.settings import BUCKET_NAME, REGION


def _create_bucket(settings, client):
    
    response = client.create_bucket(
        Bucket=settings[BUCKET_NAME],
        ACL='private',
        CreateBucketConfiguration={
            'LocationConstraint': settings[REGION],
        }
    )


def save_in_bucket(settings, file, aws_profile):
    session = boto3.Session(profile_name=aws_profile)
    s3 = session.client('s3')
    bucket_name = settings[BUCKET_NAME]

    try:
        head = s3.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError:
        _create_bucket(settings, s3)

    response = s3.put_object(
                    Bucket=bucket_name,
                    Key=file.name,
                    Body=file.read_bytes(),
                    ACL='private',
                    StorageClass='GLACIER'
                )
    print(response)
