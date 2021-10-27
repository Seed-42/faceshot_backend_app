from flask import Flask, request, jsonify
from flask_restx import Resource, Api
# from flask_restx import Resource, Api
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from config.app import APP_HOST, APP_PORT
from api import api_blueprint, api


app = Flask(__name__)
CORS(app)
app.register_blueprint(api_blueprint)
# app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


@api.route("/get_prediction")
class Predict(Resource):
    def post(self):
        try:
            return {
                "result": [
                    {
                        "student_id": "N3gAFHY4Cxew1bgXWnVUa2MYPuR2",
                        "student_attendance_status": True,
                        # "student_deltected_photo": <base64image> This is returned when student_attendance_status is true
                    },
                    {
                        "student_id": "FI2Q5DEgUhUWXd6A6w7wy8dc2Kx1",
                        "student_attendance_status": False
                    },
                ],
                "message": "Success",
            }, 200
        except Exception as err:
            return {
                "message": "Error",
            }, 500


# @api.route("/", methods=["GET", "POST"])
# def get_prediction():
#     if request.method == "POST":
#         # file = request.files.get('file')
#         # if file is None or file.filename == "":
#         #     return jsonify({"error": "no file"})
#         try:
#             return {
#                 "result": [
#                     {
#                         "name": "Ram",
#                         "status": "absent"
#                     },
#                     {
#                         "name": "Jerin",
#                         "status": "present"
#                     },
#                     {
#                         "name": "Praharsh",
#                         "status": "absent"
#                     },
#                     {
#                         "name": "Prithvi",
#                         "status": "present"
#                     },
#                     {
#                         "name": "Abhishek",
#                         "status": "absent"
#                     }
#                 ],
#                 "message": "Success",
#             }, 200
#         except Exception as e:
#             return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
