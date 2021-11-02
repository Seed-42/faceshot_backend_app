import os
from datetime import datetime
from pathlib import Path

from google.cloud import storage
from google.oauth2 import service_account

from config import app
# from logs.app import logger

import json


def download_models():
    print("Downloading models from cloud..")
    start_time = datetime.now()

    # Get credentials.
    credentials_dict = json.loads(app.GS_CREDENTIALS)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)

    # Connect to cloud storage.
    client = storage.Client(project=credentials_dict.get("project_id", ""), credentials=credentials)

    # Fetch bucket.
    bucket = client.get_bucket(bucket_or_name=credentials_dict.get("bucket", ""))

    # Fetch objects.
    blobs = bucket.list_blobs(prefix='')
    for blob in blobs:
        if blob.name.endswith("/"):
            continue
        file_split = blob.name.split("/")
        directory = os.path.join(app.APP_PRETRAINED_MODELS_PATH, "/".join(file_split[0:-1]))
        file_name = file_split[-1]
        Path(directory).mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(os.path.join(directory, file_name))

    print(f"Models downloaded. Time taken: {datetime.now() - start_time} seconds")
