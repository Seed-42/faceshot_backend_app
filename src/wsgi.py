from flask import Flask, request
from flask_cors import CORS
from flask_restx import Resource

from api import api_blueprint, api
from config.app import APP_HOST, APP_PORT
# from actions.predict import FaceDetector
from utils import utils
from actions.FaceRec import FaceRec

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
                        "student_detected_face_coordinates": {
                            'topleft': [1, 1],
                            'topright': [24, 1],
                            'bottomleft': [24, 24],
                            'bottomright': [1, 24],
                        }
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
        try:
            image_string = request.form.get("image", "")

            # Check if image is present.
            if not image_string:
                raise AttributeError("Missing required attributes in incoming request.")

            # Check if image is base64 type.
            if not isinstance(image_string, str):
                raise ValueError("Image format incorrect.")

            # # Save image.
            # image_path = utils.save_image(image_string)
            # # Get predictions.
            # result = FaceDetector(image_path).detect()
            # bytes_image = utils.convert_image_string_to_bytes(image_string)
            # np_image = utils.convert_image_bytes_to_np_array(bytes_image)

            image_np = utils.convert_image_string_to_nparray(image_string)
            result = FaceRec().runFaceRec(image_np)

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


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
