from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2
import mxnet as mx
from mtcnn import MTCNN
from skimage import transform as trans
from config.app import APP_PRETRAINED_MODELS_PATH
from sklearn.preprocessing import normalize
import pickle
import numpy as np
import os
from actions.load_model import MODEL

# from mtcnn_detector import MtcnnDetector
# import pandas as pd
# import sys
# from mxnet.contrib.onnx.onnx2mx.import_model import import_model
# from datetime import datetime
# import random
# from time import sleep
# from easydict import EasyDict as edict
# import matplotlib.pyplot as plt
# from glob import glob
# from tqdm.notebook import tqdm
# from scipy import misc
# from sklearn.decomposition import PCA


# data_path = "../Data/all/*"
name_dict = {"joey": 0, "chan": 1, "moni": 2, "rach": 3, "ross":4, "pheo": 5}

detector = MTCNN()


class FaceRec:

    def preprocess(self, img, bbox=None, landmark=None, **kwargs):
        """
        Preprocesses Face images to facilitate embedding.
        """
        M = None
        image_size = []
        str_image_size = kwargs.get('image_size', '')
        # Assert input shape
        if len(str_image_size)>0:
            image_size = [int(x) for x in str_image_size.split(',')]
            if len(image_size)==1:
                image_size = [image_size[0], image_size[0]]
            assert len(image_size)==2
            assert image_size[0]==112
            assert image_size[0]==112 or image_size[1]==96

        # Do alignment using landmark points
        if landmark is not None:
            assert len(image_size)==2
            src = np.array([
              [30.2946, 51.6963],
              [65.5318, 51.5014],
              [48.0252, 71.7366],
              [33.5493, 92.3655],
              [62.7299, 92.2041] ], dtype=np.float32 )
            if image_size[1]==112:
                src[:,0] += 8.0
            dst = landmark.astype(np.float32)
            tform = trans.SimilarityTransform()
            tform.estimate(dst, src)
            M = tform.params[0:2,:]
            assert len(image_size)==2
            warped = cv2.warpAffine(img,M,(image_size[1],image_size[0]), borderValue = 0.0)
            return warped

        # If no landmark points available, do alignment using bounding box. If no bounding box available use center crop
        if M is None:
            if bbox is None:
                det = np.zeros(4, dtype=np.int32)
                det[0] = int(img.shape[1]*0.0625)
                det[1] = int(img.shape[0]*0.0625)
                det[2] = img.shape[1] - det[0]
                det[3] = img.shape[0] - det[1]
            else:
                det = bbox
            margin = kwargs.get('margin', 44)
            bb = np.zeros(4, dtype=np.int32)
            bb[0] = np.maximum(det[0]-margin/2, 0)
            bb[1] = np.maximum(det[1]-margin/2, 0)
            bb[2] = np.minimum(det[2]+margin/2, img.shape[1])
            bb[3] = np.minimum(det[3]+margin/2, img.shape[0])
            ret = img[bb[1]:bb[3],bb[0]:bb[2],:]
            print(ret)
            if len(image_size)>0:
                ret = cv2.resize(ret, (image_size[1], image_size[0]))
            return ret

    def get_feature(self, model, aligned):
        input_blob = np.expand_dims(aligned, axis=0)
        data = mx.nd.array(input_blob)
        db = mx.io.DataBatch(data=(data,))
        model.forward(db, is_train=False)
        embedding = model.get_outputs()[0].asnumpy()
        embedding = normalize(embedding).flatten()
        return embedding

    # def get_input(self, detector, face_img):
    #     # Pass input images through face detector
    #     faces = detector.detect_faces(face_img)
    #     ret = np.array([np.asarray([face['box'][0], face['box'][1], face['box'][2], face['box'][3], face['confidence']])for face in faces]),np.array([np.array([element[0] for element in face['keypoints'].values()] + [element[1] for element in face['keypoints'].values()]) for face in faces])
    #
    #     if ret is None:
    #         return None
    #     bbox, points = ret
    #     if bbox.shape[0]==0:
    #         return None
    #
    #     bbox = bbox[0,0:4]
    #     points = points[0,:].reshape((2,5)).T
    #     # Call preprocess() to generate aligned images
    #     nimg = self.preprocess(face_img, bbox, points, image_size='112,112')
    #     nimg = cv2.cvtColor(nimg, cv2.COLOR_BGR2RGB)
    #     aligned = np.transpose(nimg, (2,0,1))
    #     return aligned

    def max_similarity(self, embeddings, target):
        """
        Finds out the identity with maximum similarity with the target image.

        :param: target: Face Image
        :return: id: The name of the identity.
        :return: confidence: Confidence of the prediction.
        """
        threshold = 0.4
        sim_dict = {}

        for embed_byte in embeddings.keys():
            embed = np.frombuffer(embed_byte, dtype=target.dtype)
            sim_dict[embed_byte] = np.dot(embed, target.T)

        max_similarity_key = max(sim_dict, key=sim_dict.get)
        max_similarity_identity = embeddings[max_similarity_key]
        max_similarity_confidence = sim_dict[max_similarity_key]

        if max_similarity_confidence < threshold:
            return "N/A", max_similarity_confidence
        else:
            return max_similarity_identity, max_similarity_confidence.round(4)

    def _get_embeddings(self):
        embeddings_path = os.path.join(APP_PRETRAINED_MODELS_PATH, "models/embeddings/embed.h5py")
        with open(embeddings_path, 'rb') as handle:
            embeddings = pickle.load(handle)
        return embeddings

    def runFaceRec(self, image):
        id_dict = {v:k for k,v in name_dict.items()}
        id_dict['N/A'] = "N/A"
        detected_identities = []

        faces = detector.detect_faces(image)
        ret = np.array([np.asarray([face['box'][0], face['box'][1], face['box'][2], face['box'][3], face['confidence']])for face in faces]), \
            np.array([np.array([element[0] for element in face['keypoints'].values()] + [element[1] for element in face['keypoints'].values()]) for face in faces])

        if ret:
            for n in range(len(ret[0])):
                bbox = ret[0][n]
                points = ret[1][n]
                if bbox.shape[0] == 0:
                    break
                box_colour = (25*n, 25*n, 25*n)
                bbox = bbox[0:4]
                points = points[:].reshape((2, 5)).T
                nimg = self.preprocess(image, bbox, points, image_size='112,112')
                nimg = cv2.cvtColor(nimg, cv2.COLOR_BGR2RGB)
                aligned = np.transpose(nimg, (2, 0, 1))
                embed = self.get_feature(MODEL, aligned)
                embeddings = self._get_embeddings()
                id, confidence = self.max_similarity(embeddings, embed)
                detected_identities.append(
                    {
                        "student_id": id_dict[id],
                        "student_attendance_confidence": round(float(confidence), 2),
                        "student_detected_face_coordinates": {
                            'topleft': [bbox[0], bbox[1]],
                            'topright': [bbox[2], bbox[1]],
                            'bottomleft': [bbox[0], bbox[3]],
                            'bottomright': [bbox[2], bbox[3]]
                        }
                    },
                )

        return detected_identities
