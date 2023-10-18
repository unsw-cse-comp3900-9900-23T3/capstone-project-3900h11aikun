from flask import request, abort, jsonify
from flask_restx import Resource, Namespace
from db.models import *
from models.auth import *
import re
import os
import random
import base64
from .util import *
from config import app
import time


# define the api
api = Namespace(
    "auth",
    description="login, register"
)


# a combination of login with either username or email,
# and choose to return token of not
def login(username=None, email=None, password=None, type=None, return_token=False):
    if email is None:
        # use username and password
        if type == "student":
            result_user = Student.query.filter_by(username=username, password=password).first()
        elif type == "supervisor":
            result_user = Supervisor.query.filter_by(username=username, password=password).first()
        else:
            result_user = Partner.query.filter_by(username=username, password=password).first()
    else:
        # use email and password
        if type =="student":
            result_user = Student.query.filter_by(email=email, password=password).first()
        elif type == "supervisor":
            result_user = Supervisor.query.filter_by(email=email, password=password).first()
        else:
            result_user = Partner.query.filter_by(email=email, password=password).first()

    if result_user is None:
        return None

    # convert to a dict
    result_data = result_user.as_dict()

    if return_token:
        # generate the token with jwt
        if type == "student":
            token = generate_token(result_user.student_id, type)
        elif type == "supervisor":
            token = generate_token(result_user.supervisor_id, type)
        else:
            token = generate_token(result_user.partner_id, type)

        result_data["token"] = token
        result_data["type"] = type

    return result_data



# assign a random avatar from the db folder, and save the relative path to the database
# when return result to the frontend, it will be converted to absolute path,
# such as http://127.0.0.1:9998/db/raw_data/avatars/18.jpg
def get_random_avatar():
    avatar_list = os.listdir("db/raw_data/avatars")
    avatar = random.choice(avatar_list)
    avatar_relative_path = os.path.join("db/raw_data/avatars", avatar)

    # replace \\ to /
    avatar_relative_path = avatar_relative_path.replace("\\", "/")
    return avatar_relative_path


@api.route("/login")
class Login(Resource):
    @api.doc(description="Login with username, type, password. All passwords are Abcd1234! by default database")
    @api.expect(login_model)
    @api.response(200, 'success login, will return the user profile')
    @api.response(400, 'invalid username, password or type')
    @api.response(401, 'valid inputs, but the user is not found, so login fail')
    def post(self):
        """login with username + type + password"""
        data = request.get_json()
        result_data = login(username=data["username"], password=data["password"], type=data["type"], return_token=False)
        if result_data is None:
            abort(401, "username or password is incorrect")
        else:
            return jsonify(result_data)


@api.route("/login_with_email")
class LoginWithEmail(Resource):
    @api.doc(description="Login with email + type + password. All passwords are Abcd1234! by default database")
    @api.expect(login_model_with_email)
    @api.response(200, 'success login, will return the user profile')
    @api.response(400, 'invalid username, password or type')
    @api.response(401, 'valid inputs, but the user is not found, so login fail')
    def post(self):
        """login with email + type + password"""
        data = request.get_json()
        result_data = login(email=data["email"], password=data["password"], type=data["type"], return_token=False)
        if result_data is None:
            abort(401, "email or password is incorrect")
        else:
            return jsonify(result_data)


@api.route("/login_with_username_and_return_token")
class LoginWithUsernameAndReturnToken(Resource):
    @api.doc(description="Login with username + type + password. And return token with profile")
    @api.expect(login_model)
    @api.response(200, 'success login, will return the user profile + token')
    @api.response(400, 'invalid username, password or type')
    @api.response(401, 'valid inputs, but the user is not found, so login fail')
    def post(self):
        """login with username + type + password, return profile + token"""
        data = request.get_json()
        result_data = login(username=data["username"], password=data["password"], type=data["type"], return_token=True)
        if result_data is None:
            abort(401, "username or password is incorrect")
        else:
            return jsonify(result_data)


@api.route("/login_with_email_and_return_token")
class LoginWithEmailAndReturnToken(Resource):
    @api.doc(description="Login with email + type + password. And return the token with profile")
    @api.expect(login_model_with_email)
    @api.response(200, 'success login, will return the user profile + token')
    @api.response(400, 'invalid username, password or type')
    @api.response(401, 'valid inputs, but the user is not found, so login fail')
    def post(self):
        """login with email + type + password, return profile + token"""
        data = request.get_json()
        result_data = login(email=data["email"], password=data["password"], type=data["type"], return_token=True)
        if result_data is None:
            abort(401, "email or password is incorrect")
        else:
            return jsonify(result_data)


@api.route("/validate_token")
class ValidateToken(Resource):
    @api.doc(description="Validate the token, if valid, return the user profile, if not valid, return 401")
    @api.expect(token_parser)
    @api.response(200, 'success validate, will return the user profile')
    @api.response(401, 'invalid token')
    def get(self):
        """a route to show how the token works"""
        args = token_parser.parse_args()
        token = args["Authorization"]

        # decode the token, and get the user data in a dictionary !!!
        user_data = decode_token_and_get_user_object(token)
        if user_data is None:
            abort(401, "invalid token")
        else:
            return user_data


@api.route("/register")
class Register(Resource):
    @api.doc(description="Register require: username, email, password, type")
    @api.expect(register_model)
    @api.response(200, 'success register, will return the user profile')
    @api.response(400, 'invalid inputs / username or email is duplicate')
    def post(self):
        data = request.get_json()

        # check if the username exists anywhere
        result_student = Student.query.filter_by(username=data["username"]).first()
        result_supervisor = Supervisor.query.filter_by(username=data["username"]).first()
        result_partner = Partner.query.filter_by(username=data["username"]).first()
        if result_student or result_supervisor or result_partner:
            abort(400, "username is duplicate")

        # check if the email exists anywhere
        result_student = Student.query.filter_by(email=data["email"]).first()
        result_supervisor = Supervisor.query.filter_by(email=data["email"]).first()
        result_partner = Partner.query.filter_by(email=data["email"]).first()
        if result_student or result_supervisor or result_partner:
            abort(400, "email is duplicate")

        # check if the password is valid and email valid
        if len(data["password"]) < 8:
            abort(400, "password needs to be at least 8 characters long")

        # get avatar
        avatar_relative_path = get_random_avatar()

        # use the type to register
        if data["type"] == 'student':
            new_student = Student(
                username=data["username"],
                first_name='',
                last_name='',
                email=data["email"],
                password=data["password"],
                avatar=avatar_relative_path,
                qualification='',
                school_name='',
                major='',
                skills='',
                strength='',
                resume_url=''
            )

            db.session.add(new_student)
            db.session.commit()
            return jsonify(new_student.as_dict())

        elif data["type"] == 'partner':
            new_partner = Partner(
                username=data["username"],
                first_name='',
                last_name='',
                email=data["email"],
                password=data["password"],
                avatar=avatar_relative_path,
                company='',
                position='',
                description=''
            )

            db.session.add(new_partner)
            db.session.commit()
            return jsonify(new_partner.as_dict())

        else:
            # supervisor
            new_supervisor = Supervisor(
                username=data["username"],
                first_name='',
                last_name='',
                email=data["email"],
                password=data["password"],
                avatar=avatar_relative_path,
                qualification='',
                school_name='',
                skills=''
            )

            db.session.add(new_supervisor)
            db.session.commit()
            return jsonify(new_supervisor.as_dict())
