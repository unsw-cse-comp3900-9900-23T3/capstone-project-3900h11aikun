from flask import request, abort, jsonify
from flask_restx import Resource, Namespace

api = Namespace(
    "profile",
    description="get profile, edit profile"
)


@api.route("/profile")
class Login(Resource):
    def get(self):
        pass
