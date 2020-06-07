from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class S3MediaStorage(S3Boto3Storage):
    endpoint_url = settings.S3_URL
    access_key = settings.S3_ACCESS_KEY
    secret_key = settings.S3_SECRET_KEY
    
class OriginalMediaStorage(S3MediaStorage):
    bucket_name = settings.S3_ORIGINAL_BUCKET_NAME
    file_overwrite = False

class PublicMediaStorage(S3MediaStorage):
    bucket_name = settings.S3_PUBLIC_BUCKET_NAME
    file_overwrite = False

