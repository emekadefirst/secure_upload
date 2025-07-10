import urllib3
import os
from minio import Minio
import mimetypes
from env import S3_ACCESS_KEY, S3_BUCKET, S3_ENDPOINT, S3_SECRET_KEY


urllib3.disable_warnings()

endpoint = S3_ENDPOINT.replace("https://", "").replace("http://", "").split("/")[0]
bucket_name = S3_BUCKET.lower()
region = "eu-north-1" 


client = Minio(
    endpoint,
    access_key=S3_ACCESS_KEY,
    secret_key=S3_SECRET_KEY,
    secure=True
)


class MediaService:
    BUCKET_INITIALIZED = False

    @staticmethod
    def ensure_bucket():
        """Ensure bucket exists — only applies to MinIO, not AWS S3."""
        if not MediaService.BUCKET_INITIALIZED:
            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)
            MediaService.BUCKET_INITIALIZED = True

    @staticmethod
    def upload(file: bytes):
        try:
            MediaService.ensure_bucket()

            object_name = f"public/{file.filename}"
            content_type = mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
            file.file.seek(0, os.SEEK_END)
            file_size = file.file.tell()
            file.file.seek(0)
            client.put_object(
                bucket_name,
                object_name,
                data=file.file,
                length=file_size,
                content_type=content_type,
                metadata={"Content-Disposition": "inline"},
            )
            return f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"

        except Exception as e:
            raise ValueError(f"Upload failed: {str(e)}")