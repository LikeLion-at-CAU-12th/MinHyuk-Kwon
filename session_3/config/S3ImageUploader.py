from config import settings
import boto3
import uuid

class S3ImageUploader:
    def __init__(self, file):
        self.file = file

    def upload(self):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        i = str(uuid.uuid4())
        response = s3_client.upload_fileobj(self.file, settings.AWS_STORAGE_BUCKET_NAME, i)
        return f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{i}'