import uuid
from pathlib import Path
import boto3
from app.core.config import settings

LOCAL_UPLOADS = Path("uploads")
LOCAL_UPLOADS.mkdir(exist_ok=True)


def upload_file(file_bytes: bytes, filename: str) -> str:
    ext = Path(filename).suffix
    key = f"reports/{uuid.uuid4()}{ext}"

    if settings.s3_bucket_name and settings.aws_access_key_id:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )
        s3.put_object(Bucket=settings.s3_bucket_name, Key=key, Body=file_bytes)
        return f"https://{settings.s3_bucket_name}.s3.amazonaws.com/{key}"

    local_path = LOCAL_UPLOADS / key.replace("/", "_")
    local_path.write_bytes(file_bytes)
    return str(local_path)
