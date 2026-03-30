import boto3
import uuid
from dotenv import load_dotenv
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

load_dotenv()

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def upload_to_cloud(image_bytes, file_extension="png"):
    """Uploads image bytes to S3 and returns the public URL"""
    try:
        file_name = f"uploads/{uuid.uuid4()}.{file_extension}"

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=image_bytes,
            ACL='public-read'
        )

        url = f"https://{BUCKET_NAME}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{file_name}"

        return url

    except Exception as e:
        print(f"Upload Error: {str(e)}")
        return None
