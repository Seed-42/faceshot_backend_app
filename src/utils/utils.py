import base64
import os
import uuid

from config.app import APP_TEMP_PATH


def save_image(image_string):
    img_bytes = image_string.encode('utf-8')
    img_data = base64.decodebytes(img_bytes)
    file_name = f'{uuid.uuid4()}.jpg'
    image_path = os.path.join(APP_TEMP_PATH, file_name)
    with open(image_path, "wb") as fh:
        fh.write(img_data)
    return image_path
