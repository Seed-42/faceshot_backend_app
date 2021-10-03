from flask import Flask
from flask_restx import Resource, Api

from config.app import APP_HOST, APP_PORT


app = Flask(__name__)
api = Api(app)


@api.route("/predict")
class Predict(Resource):
    def post(self):
        # Todo: Link prediction.
        return {
            "result": {
                "ram": "absent",
                "jerin": "present",
                "praharsh": "absent",
                "prithvi": "present",
                "abhishek": "absent",
            },
            "message": "Success",
        }, 200


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
