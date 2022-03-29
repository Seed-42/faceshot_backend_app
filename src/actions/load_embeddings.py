import pickle
import os
from config import config


def get_embeddings():
    embeddings_path = os.path.join(config.APP_PRETRAINED_MODELS_PATH, "models/embeddings/embed.h5py")
    with open(embeddings_path, 'rb') as handle:
        embeddings = pickle.load(handle)
    return embeddings


EMBEDDINGS = get_embeddings()
