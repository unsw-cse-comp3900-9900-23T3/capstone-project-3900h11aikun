from flask import request, abort, jsonify
from flask_restx import Resource, Namespace

api = Namespace(
    "auth",
    description="login and logout"
)


@api.route("/login")
class Login(Resource):
    def post(self):
        pass


@api.route("/register")
class Register(Resource):
    def post(self):
        pass




