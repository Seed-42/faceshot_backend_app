import os
from datetime import datetime

import mxnet as mx
from mxnet.contrib.onnx.onnx2mx.import_model import import_model

from config import config

from utils import gcloud_utils

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
    model_path = os.path.join(config.APP_PRETRAINED_MODELS_PATH, "models/base_model/resnet100.onnx")
    image_size = (112, 112)

    # Import ONNX model
    sym, arg_params, aux_params = import_model(model_path)

    # Define and binds parameters to the network
    model = mx.mod.Module(symbol=sym, context=context, label_names=None)
    model.bind(data_shapes=[('data', (1, 3, image_size[0], image_size[1]))])
    model.set_params(arg_params, aux_params)

    print(f"Model loading time: {datetime.now()-start_time} seconds")
    return model


# Download models from cloud.
gcloud_utils.download_models()

MODEL = get_model()
