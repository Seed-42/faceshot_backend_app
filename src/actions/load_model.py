import os
import pickle
from datetime import datetime

import mxnet as mx
from mxnet.contrib.onnx.onnx2mx.import_model import import_model

from config.config import APP_PRETRAINED_MODELS_PATH
from utils.gcloud_utils import download_models
# from logs.app import logger

if len(mx.test_utils.list_gpus()) == 0:
    context = mx.cpu()
else:
    context = mx.gpu(0)


def get_model():
    """
    Loads ArcFace Model.
    """

    print(f"Model loading started..")
    start_time = datetime.now()
    model_path = os.path.join(APP_PRETRAINED_MODELS_PATH, "models/base_model/resnet100.onnx")
    image_size = (112, 112)

    # Import ONNX model
    sym, arg_params, aux_params = import_model(model_path)

    # Define and binds parameters to the network
    model = mx.mod.Module(symbol=sym, context=context, label_names=None)
    model.bind(data_shapes=[('data', (1, 3, image_size[0], image_size[1]))])
    model.set_params(arg_params, aux_params)

    print(f"Model loading time: {datetime.now()-start_time} seconds")
    return model


def get_embeddings():
    embeddings_path = os.path.join(APP_PRETRAINED_MODELS_PATH, "models/embeddings/embed.h5py")
    with open(embeddings_path, 'rb') as handle:
        embeddings = pickle.load(handle)
    return embeddings


# Download models from cloud.
download_models()

MODEL = get_model()
EMBEDDINGS = get_embeddings()
