from flask import request, abort, jsonify
from flask_restx import Resource, Namespace
from db.models import *
from models.auth import *

api = Namespace(
    "auth",
    description="login and logout"
)


@api.route("/login")
class Login(Resource):
    @api.doc(description="Login require: username, type, password. All passwords are Abcd1234! by default database")
    @api.expect(login_model)
    @api.response(200, 'success login, will return the user profile')
    @api.response(400, 'invalid username, password or type')
    @api.response(401, 'valid inputs, but the user is not found, so login fail')
    def post(self):
        data = request.get_json()
        result_user = None

        if data["type"] == 'student':
            # filter by username and password
            result_user = Student.query.filter_by(username=data["username"], password=data["password"]).first()
        elif data["type"] == 'supervisor':
            result_user = Supervisor.query.filter_by(username=data["username"], password=data["password"]).first()
        else:
            result_user = Partner.query.filter_by(username=data["username"], password=data["password"]).first()

        if result_user is None:
            abort(401, "username or password is incorrect")
        else:
            result_data = result_user.as_dict()
            result_data["type"] = data["type"]
            return jsonify(result_data)


@api.route("/register")
class Register(Resource):
    def post(self):
        pass




