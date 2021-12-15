import os
from datetime import datetime
from pathlib import Path

from google.cloud import storage
from google.oauth2 import service_account

from config import config
# from logs.app import logger

import json


def download_models():
    print("Downloading models from cloud..")
    start_time = datetime.now()

    # Get credentials.
    credentials_dict = json.loads(config.GS_CREDENTIALS)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)

    # Connect to cloud storage.
    client = storage.Client(project=credentials_dict.get("project_id", ""), credentials=credentials)

    # Fetch bucket.
    bucket = client.get_bucket(bucket_or_name=config.GS_MODELS_BUCKET_NAME)

    # Fetch objects.
    blobs = bucket.list_blobs(prefix='')
    for blob in blobs:
        if blob.name.endswith("/"):
            continue
        file_split = blob.name.split("/")
        directory = os.path.join(config.APP_PRETRAINED_MODELS_PATH, "/".join(file_split[0:-1]))
        file_name = file_split[-1]
        Path(directory).mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(os.path.join(directory, file_name))

    print(f"Models downloaded. Time taken: {datetime.now() - start_time} seconds")


def upload_image(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    # Get credentials.
    credentials_dict = json.loads(config.GS_CREDENTIALS)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)

    client = storage.Client(project=credentials_dict.get("project_id", ""), credentials=credentials)

    bucket = client.get_bucket(bucket_or_name=config.GS_IMAGES_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    blob.make_public()
    return blob.public_url
