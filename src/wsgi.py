import os
import shutil
import time
import uuid
from threading import Thread

from flask import Flask, request
from flask_cors import CORS
from flask_restx import Resource

from actions.FaceRec import FaceRec
from actions.train import TrainFaceRecognizer
from api import api_blueprint, api
from utils import utils
from config import config

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_blueprint)


@api.route("/train")
class TrainFaceRec(Resource):
    def post(self):

        try:
            def do_work(value):
                time.sleep(value)
                TrainFaceRecognizer().train()

            thread = Thread(target=do_work, kwargs={'value': request.args.get('value', 60)})
            thread.start()

            return {
                "message": "Train Accepted.",
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
                        "student_id": "1a2a34s5d23f4d",
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
