from flask import request, abort, jsonify
from flask_restx import Resource, Namespace
from db.models import *
from models.auth import *
import re
import os
import random
import base64

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


@api.route("/student_register_without_resume_file")
class Register(Resource):
    @api.doc(description="student register, all fields are required, but no file is upload, so resume_url will be None")
    @api.response(200, 'success register, will return the user profile')
    @api.response(400, 'invalid inputs / username or email is duplicate')
    @api.expect(student_register_model)
    def post(self):
        # get the data from the request
        data = request.get_json()

        # check if any attribtues are empty
        for key, value in data.items():
            if value == "":
                abort(400, "empty value at {}".format(key))

        # check if the username is unique
        is_username_duplicate = Student.query.filter_by(username=data["username"]).first()
        if is_username_duplicate is not None:
            abort(400, "username is duplicate")

        # check if the email is unique
        is_email_duplicate = Student.query.filter_by(email=data["email"]).first()
        if is_email_duplicate is not None:
            abort(400, "email is duplicate")

        # password needs to be 8 characters long, one uppercase, one lowercase, one number
        if len(data["password"]) < 8:
            abort(400, "password needs to be at least 8 characters long")

        # password pattern: ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$
        # and allow special characters
        password_pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
        if not password_pattern.match(data["password"]):
            abort(400, "password needs to contain at least one uppercase, one lowercase and one number")

        # the email should be a valid email
        email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        if not email_pattern.match(data["email"]):
            abort(400, "invalid email")

        # assign a random avatar from the db folder, and save the full path to the database
        # avatar_list = os.listdir("db/raw_data/avatars")
        # avatar = random.choice(avatar_list)
        # avatar_relative_path = os.path.join("db/raw_data/avatars", avatar)
        base_dir = "db"
        raw_data_dir = "raw_data"
        avatars_dir = "avatars"
        avatar_list = os.listdir(os.path.join(base_dir, raw_data_dir, avatars_dir))
        avatar = random.choice(avatar_list)
        avatar_relative_path = os.path.join(base_dir, raw_data_dir, avatars_dir, avatar)

        # replace \\ to /
        avatar_relative_path = avatar_relative_path.replace("\\", "/")

        # create a new student, without resume upload
        new_student = Student(
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            avatar=avatar_relative_path,
            qualification=data["qualification"],
            school_name=data["school_name"],
            major=data["major"],
            skills=data["skills"],
            strength=data["strength"],
            resume_url=None
        )

        db.session.add(new_student)
        db.session.commit()

        # return this student to the frontend
        return jsonify(new_student.as_dict())
