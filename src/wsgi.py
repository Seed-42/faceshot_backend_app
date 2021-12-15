from flask import Flask, request
from flask_cors import CORS
from flask_restx import Resource

from api import api_blueprint, api
from config import config
# from actions.predict import FaceDetector
from utils import utils
from actions.FaceRec import FaceRec
import os
import uuid
import shutil

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_blueprint)


@api.route("/test")
class TestPredict(Resource):
    def post(self):
        try:
            return {
                "result": [
                    {
                        "student_id": "1a2a34s5d23f4d",
                        "student_attendance_confidence": 99.0,
                        "file_url": "https://storage.googleapis.com/seed42-faceshot-output-images/ae10d9db-0ba1-494f-821f-cca7049efa6c/qb69UR7bW5RdcPMUKfnm3wbUP4A3.jpeg"
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

            image_np = utils.convert_image_string_to_nparray(image_string)
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
