import os
import shutil
import time
import uuid
from threading import Thread

import requests
from flask import Flask, request
from flask_cors import CORS
from flask_restx import Resource

from actions.FaceRec import FaceRec
from api import api_blueprint, api
from utils import utils, gcloud_utils
from config import config

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_blueprint)


@api.route("/reset_embeddings")
class ResetEmbeddings(Resource):
    def post(self):
        try:
            # empty embeddings file.
            utils.reset_embeddings()

            # Backup existing embeddings and upload new embeddings to cloud.
            gcloud_utils.move_existing_embedding_to_backup()
            gcloud_utils.upload_new_embeddings()

            return {
                       "message": "Resetting embeddings complete",
                       "success": "true"
            }, 200

        except Exception as err:
            return {
                       "message": "Error",
                       "success": "false"
                   }, 500


@api.route("/train")
class TrainFaceRec(Resource):
    def post(self):

        try:
            # def do_work(value):

            value = request.get_json()

            # Create a data folder to store tmp files for current request.
            tmp_data_folder_path = os.path.join(config.APP_TEMP_PATH, str(uuid.uuid4()))
            if os.path.exists(tmp_data_folder_path):
                shutil.rmtree(tmp_data_folder_path)
            os.makedirs(tmp_data_folder_path)

            url = value.get("url", "")
            object_id = value.get("id", "")

            if not all([url, id]):
                raise AttributeError("Missing attributes in input request.")

            # Download image from url and load it.
            image_np = utils.download_and_load_image(url, tmp_data_folder_path)

            # Add facial features and save embeddings.
            FaceRec().train(image_np, object_id)

            # Save embeddings
            utils.save_embeddings()

            # Upload new embeddings and add current file to back up folder in GS.
            gcloud_utils.move_existing_embedding_to_backup()
            gcloud_utils.upload_new_embeddings()

            # Send a post to firebase to notify training is done.
            # requests.post()

            # Remove tmp data folder.
            if os.path.exists(tmp_data_folder_path):
                shutil.rmtree(tmp_data_folder_path)

            # thread = Thread(target=do_work, kwargs={'value': request.get_json()})
            # thread.start()

            return {
                "message": "Training complete.",
                "success": "true"
            }, 200

        except Exception as err:
            return {
                "message": "Error",
                "success": "false"
            }, 500


@api.route("/test")
class TestPredict(Resource):
    def post(self):
        try:
            return {
                "result": [
                    {
                        "student_id": "monica@gmail.com",
                        "student_attendance_confidence": 99.0,
                        "file_url": "https://storage.googleapis.com/seed42-faceshot-phase2-output-images/2d81bd1b-d6fb-4fed-81e8-b3eaf8088791/69ce3b5f-da9b-42c3-9ea5-ec40deac7e70.jpeg"
                    },
                ],
                "message": "Face detection complete.",
                "success": "true"
            }, 200
        except Exception as err:
            return {
                "message": "Error",
                "success": "false"
            }, 500


@api.route("/get_prediction")
class Predict(Resource):
    def post(self):

        # Create a data folder to store tmp files for current request.
        tmp_data_folder_path = os.path.join(config.APP_TEMP_PATH, str(uuid.uuid4()))
        if os.path.exists(tmp_data_folder_path):
            shutil.rmtree(tmp_data_folder_path)
        os.makedirs(tmp_data_folder_path)

        try:
            image_string = request.form.get("image", "")

            if not image_string:
                request_json = request.get_json()
                image_string = request_json.get("image", "")

            # Check if image is present.
            if not image_string:
                raise AttributeError("Missing required attributes in incoming request.")

            # Check if image is base64 type.
            if not isinstance(image_string, str):
                raise ValueError("Image format incorrect.")

            # Get image array from base64 string.
            image_np = utils.convert_image_string_to_nparray(image_string)

            # Get identities.
            result = FaceRec(tmp_data_folder_path).runFaceRec(image_np)

            return {
                "result": result,
                "message": "Face detection complete.",
                "success": "true"
            }, 200

        except Exception as err:
            return {
                "message": f"{err}",
                "success": "false"
            }, 500

        finally:
            if os.path.exists(tmp_data_folder_path):
                shutil.rmtree(tmp_data_folder_path)


@api.route("/url/get_prediction")
class PredictByURL(Resource):
    def post(self):

        # Create a data folder to store tmp files for current request.
        tmp_data_folder_path = os.path.join(config.APP_TEMP_PATH, str(uuid.uuid4()))
        if os.path.exists(tmp_data_folder_path):
            shutil.rmtree(tmp_data_folder_path)
        os.makedirs(tmp_data_folder_path)

        try:
            image_url = request.form.get("url", "")

            # Check if image is present.
            if not image_url:
                raise AttributeError("Missing image url in incoming request.")

            # Check if image is base64 type.
            if not isinstance(image_url, str):
                raise ValueError("Image url format incorrect.")

            # Download image from url and load it.
            image_np = utils.download_and_load_image(image_url, tmp_data_folder_path)

            # Get identities.
            result = FaceRec(tmp_data_folder_path).runFaceRec(image_np)

            return {
                "result": result,
                "message": "Face detection complete.",
                "success": "true"
            }, 200

        except Exception as err:
            return {
                "message": f"{err}",
                "success": "false"
            }, 500

        finally:
            if os.path.exists(tmp_data_folder_path):
                shutil.rmtree(tmp_data_folder_path)


if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT)
