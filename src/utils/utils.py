import base64
import io
import os
import uuid

import numpy as np
from PIL import Image

from config.config import APP_TEMP_PATH


def save_image(image_string):
    img_bytes = image_string.encode('utf-8')
    img_data = base64.decodebytes(img_bytes)
    file_name = f'{uuid.uuid4()}.jpg'
    image_path = os.path.join(APP_TEMP_PATH, file_name)
    with open(image_path, "wb") as fh:
        fh.write(img_data)
    return image_path


def convert_image_string_to_nparray(image_string):
    base64_decoded = base64.b64decode(image_string)
    image = Image.open(io.BytesIO(base64_decoded))
    image_np = np.array(image)
    return image_np


def convert_nparray_to_image(img_array, img_path):
    im = Image.fromarray(img_array)
    im.save(f"{img_path}")
