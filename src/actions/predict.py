# import os
# from mtcnn import MTCNN
# import cv2
# import numpy as np
# from mxnet.contrib.onnx.onnx2mx.import_model import import_model
# import mxnet as mx
# from load_model import MODEL
#
#
# class FaceDetector:
#     def __init__(self, image_path):
#         self._image_path = image_path
#         self._image = self._read_image()
#
#     # def _get_model(self, context, model):
#     #     """
#     #     Loads ArcFace Model.
#     #     """
#     #     image_size = (112, 112)
#     #     # Import ONNX model
#     #     sym, arg_params, aux_params = import_model(model)
#     #     # Define and binds parameters to the network
#     #
#     #     model = mx.mod.Module(symbol=sym, context=context, label_names=None)
#     #     model.bind(data_shapes=[('data', (1, 3, image_size[0], image_size[1]))])
#     #     model.set_params(arg_params, aux_params)
#     #     return model
#
#     def _read_image(self):
#         return cv2.imread(self._image_path)
#
#     def _preprocess_image(self):
#         pass
#
#     def _post_process_results(self):
#         pass
#
#     def _remove_image(self):
#         if os.path.exists(self._image_path):
#             os.remove(self._image_path)
#
#     def _detect_faces(self, detector):
#         """
#         This function detects the faces present in an image.
#         :param: image: A numpy array in which the faces are detected.
#         :return: faces:  A list of faces along with the coordinates of the bounding box.
#         List is empty if no faces are found.
#         [[coordx1, coordy1, coordx2, coordy2], [coordx1, coordy1, coordx2, coordy2]]
#         """
#
#         img = cv2.resize(self._image, (256, 256))
#         faces = [face['box'] for face in detector.detect_faces(img)]
#         return faces
#
#     def detect(self):
#         try:
#             # Preprocess image.
#             self._preprocess_image()
#
#             # Detect faces.
#             result = self._detect_faces()
#
#             return result
#
#         except Exception:
#             raise Exception
#
#         finally:
#             self._remove_image()
