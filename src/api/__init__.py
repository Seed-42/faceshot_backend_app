from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, title="Faceshot Server", description="", version="1.0")
