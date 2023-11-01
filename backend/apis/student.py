from flask import request, abort, jsonify
from flask_restx import Resource, Namespace
from db.models import *
from models.student import *
from db.models import *
from datetime import datetime
from config import app
import os



api = Namespace(
    "studentInfo",
    description="get student, edit student"
)

# @api.route("/student")
# class Student(Resource):
#     def get(self):
#         pass



@api.route('/student_update')
class StudentUpdate(Resource):
    @api.doc(description="Update student information")
    @api.expect(student_update_model)
    @api.response(200, 'update success')
    @api.response(400, 'invalid params')
    def put(self):
        data = request.get_json()

        student = Student.query.filter_by(student_id=data["student_id"]).first()
        if student is None:
            return {"message": "unknown student id"}, 401

        if 'username' in data:
            student.username = data['username']
        if 'first_name' in data:
            student.username = data['first_name']
        if 'last_name' in data:
            student.last_name = data['last_name']
        if 'major' in data:
            student.major = data['major']
        if 'password' in data:
            student.password = data['password']
        if 'school_name' in data:
            student.school_name = data['school_name']
        if 'skills' in data:
            student.skills = data['skills']
        if 'resume_url' in data:
            student.resume_url = data['resume_url']
        if 'strength' in data:
            student.strength = data['strength']
        if 'email' in data:
            student.email = data['email']


        student.updated_at = datetime.now()

        db.session.commit()

        return student.as_dict()

@api.route("/getStudentInfo/<int:student_id>")
class StudentInfo(Resource):
    @api.doc(description="Get student information by ID")
    @api.response(200, 'success')
    @api.response(401, 'unknown student id')
    def get(self, student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if student is None:
            return {"message": "unknown student id"}, 401

        return student.as_dict()


@api.route("/uploadFile")
class FileUpload(Resource):
    @api.doc(description="Upload a file")
    @api.response(200, 'success')
    @api.response(400, 'bad request')
    def post(self):
        if 'file' not in request.files:
            return {"message": "No file selected"}, 400

        file = request.files['file']

        if file.filename == '':
            return {"message": "No file selected"}, 400

        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(f"Uploaded file saved: {filename}")

        return {"message": "File uploaded successfully"}