import json
from io import BytesIO
from minio import Minio
from prefect import task
from src.config import MINIO_BUCKET
from src.utils import tomorrow_str

@task
def save_raw_to_minio(city: str, data: dict):
    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False,
    )

    if not client.bucket_exists(MINIO_BUCKET):
        client.make_bucket(MINIO_BUCKET)

    object_name = f"{city}/{tomorrow_str()}.json"
    body = json.dumps(data).encode()

    client.put_object(
        MINIO_BUCKET,
        object_name,
        BytesIO(body),
        len(body),
        content_type="application/json",
    )

    print(f"📥 Saved {object_name} to MinIO")
