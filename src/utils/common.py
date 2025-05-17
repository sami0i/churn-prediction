import os
import io
import joblib
import boto3
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file (e.g., BUCKET_NAME)
load_dotenv()

def save_to_s3(artifact, s3_path: Path):
    """
    Serializes and uploads a Python object to an S3 bucket using joblib.

    Parameters:
    - artifact: Any Python object (e.g., model, encoder, scaler)
    - s3_path: Path object representing the key to use in S3
    """
    name = s3_path.stem  # Used for logging only
    buffer = io.BytesIO()
    joblib.dump(artifact, buffer)
    buffer.seek(0)

    key = s3_path.as_posix() if isinstance(s3_path, Path) else str(s3_path)
    boto3.client("s3").upload_fileobj(buffer, os.getenv("BUCKET_NAME"), key)

    print(f"✅ {name} uploaded to s3://{os.getenv('BUCKET_NAME')}/{key}")


def load_from_s3(s3_path: Path):
    """
    Downloads and deserializes a joblib object from S3.

    Parameters:
    - s3_path: Path object representing the key in the S3 bucket

    Returns:
    - The deserialized Python object
    """
    bucket = os.getenv("BUCKET_NAME")
    if not bucket:
        raise ValueError("❌ Environment variable BUCKET_NAME is not set.")

    buffer = io.BytesIO()
    key = s3_path.as_posix() if isinstance(s3_path, Path) else str(s3_path)
    boto3.client("s3").download_fileobj(bucket, key, buffer)
    buffer.seek(0)

    return joblib.load(buffer)
