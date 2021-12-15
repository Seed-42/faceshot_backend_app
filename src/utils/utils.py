import base64
import cv2
import numpy as np
from PIL import Image
import urllib.request
import os

# from config.config import APP_TEMP_PATH
# import os
# import uuid
# def save_image(image_string):
#     img_bytes = image_string.encode('utf-8')
#     img_data = base64.decodebytes(img_bytes)
#     file_name = f'{uuid.uuid4()}.jpg'
#     image_path = os.path.join(APP_TEMP_PATH, file_name)
#     with open(image_path, "wb") as fh:
#         fh.write(img_data)
#     return image_path


def convert_image_string_to_nparray(image_string):
    image_data = base64.b64decode(image_string)
    im_arr = np.frombuffer(image_data, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img


def convert_nparray_to_image(img_array, img_path):
    im = Image.fromarray(img_array)
    im.save(f"{img_path}")


def download_and_load_image(url, img_dir):
    img_path = os.path.join(img_dir, "input_image.jpeg")
    urllib.request.urlretrieve(url, img_path)
    img = cv2.imread(img_path)
    return img
