import base64
import os
import pickle
import urllib.request

import cv2
import numpy as np
from PIL import Image

from actions.load_embeddings import EMBEDDINGS
from config import config


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


def save_embeddings():
    """
    Save embeddings to upload to cloud.
    """

    embeddings_path = os.path.join(config.APP_PRETRAINED_MODELS_PATH, "models/embeddings/embed.h5py")

    # Remove existing embedding file.
    if os.path.exists(embeddings_path):
        os.remove(embeddings_path)

    with open(embeddings_path, 'wb') as handle:
        pickle.dump(EMBEDDINGS, handle, protocol=pickle.HIGHEST_PROTOCOL)


def reset_embeddings():
    """
    Create an empty embeddings file.
    """

    EMBEDDINGS.clear()

    embeddings_path = os.path.join(config.APP_PRETRAINED_MODELS_PATH, "models/embeddings/embed.h5py")

    # Remove existing embedding file.
    if os.path.exists(embeddings_path):
        os.remove(embeddings_path)

    with open(embeddings_path, 'wb') as handle:
        pickle.dump(EMBEDDINGS, handle, protocol=pickle.HIGHEST_PROTOCOL)
