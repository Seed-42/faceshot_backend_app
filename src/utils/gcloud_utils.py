import json
import os
from datetime import datetime
from pathlib import Path

from google.cloud import storage
from google.oauth2 import service_account

from config import config


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

    print(f"Models downloaded. Time taken: {datetime.now() - start_time} seconds.")


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


def upload_new_embeddings():
    """
    Function to upload the new embeddings to GS cloud.
    """

    print("Uploading latest embeddings to cloud..")
    start_time = datetime.now()

    # Get credentials.
    credentials_dict = json.loads(config.GS_CREDENTIALS)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)

    client = storage.Client(project=credentials_dict.get("project_id", ""), credentials=credentials)

    path_to_file = os.path.join(config.APP_PRETRAINED_MODELS_PATH, "models/embeddings/embed.h5py")

    bucket = client.get_bucket(bucket_or_name=config.GS_MODELS_BUCKET_NAME)
    blob = bucket.blob("models/embeddings/embed.h5py")
    blob.upload_from_filename(path_to_file)
    blob.make_public()

    print(f"Upload complete. Time taken: {datetime.now() - start_time} seconds.")
    return blob.public_url


def move_existing_embedding_to_backup():
    """
    Function to move the current embeddings to a backup folder in the cloud.
    """

    print("Backing up embeddings in cloud..")
    start_time = datetime.now()

    # Get credentials.
    credentials_dict = json.loads(config.GS_CREDENTIALS)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)

    # Connect to cloud storage.
    client = storage.Client(project=credentials_dict.get("project_id", ""), credentials=credentials)

    source_bucket = client.get_bucket(config.GS_MODELS_BUCKET_NAME)
    source_blob = source_bucket.blob("models/embeddings/embed.h5py")
    destination_bucket = client.get_bucket(config.GS_EMBEDDINGS_BACKUP_BUCKET_NAME)
    destination_blob = f"{datetime.now().strftime('%Y%m%d-%H:%M:%S')}/embed.h5py"

    # copy to new destination
    new_blob = source_bucket.copy_blob(source_blob, destination_bucket, destination_blob)

    # delete in old destination
    source_blob.delete()

    print(f'File moved from {config.GS_MODELS_BUCKET_NAME}/models/embeddings/embed.h5py to {destination_blob}')
    print(f"Back up complete. Time taken: {datetime.now() - start_time} seconds")
