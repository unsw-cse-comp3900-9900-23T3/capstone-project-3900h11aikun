from flask import request, abort, jsonify
from flask_restx import Resource, Namespace
from db.models import *
from models.student import *
from db.models import *
from datetime import datetime
from config import app
import os
import time
from .util import *


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

        if 'first_name' in data:
            student.first_name = data['first_name']
        if 'last_name' in data:
            student.last_name = data['last_name']
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


# @api.route("/uploadFile")
# class FileUpload(Resource):
#     @api.doc(description="Upload a file")
#     @api.response(200, 'success')
#     @api.response(400, 'bad request')
#     def post(self):
#         if 'file' not in request.files:
#             return {"message": "No file selected"}, 400

#         file = request.files['file']

#         if file.filename == '':
#             return {"message": "No file selected"}, 400

#         filename = file.filename
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         print(f"Uploaded file saved: {filename}")

#         return {"message": "File uploaded successfully"}


student_resume_note = """
Student can upload resume here.
The resume file is wrapped in the FormData.
File can only be .pdf, .docx. .doc only.
File size cannot be larger than 20MB.

On the frontend, create an input.
And when input change, get the file and wrap into a FormData !!!
"""

@api.route("/student_upload_resume/<int:student_id>")
class StudentRegisterWithResumeFile(Resource):
    @api.doc(description=student_resume_note)
    @api.response(200, 'success upload, will return that resume url on the server database')
    @api.response(400, 'invalid inputs, please see the detail error message')
    @api.expect(student_resume_parser)
    def post(self, student_id):
        # check if this student id exist
        student = Student.query.get(student_id)
        if student is None:
            abort(400, 'unknown student id {}'.format(student_id))

        # check this file exist
        if 'file' not in request.files:
            abort(400, 'require to submit a file')

        file = request.files['file']

        # require to match from the end of the file.filename: pdf, docx, doc
        if not file.filename.lower().endswith(('.pdf', '.docx', '.doc')):
            abort(400, 'require to submit a pdf, docx or doc file')

        # file cannot be too large, larger than 20MB will be rejected
        if len(file.read()) > 20 * 1024 * 1024:
            abort(400, 'file size cannot be larger than 20MB')

        # reset the file pointer to beginning
        file.seek(0)

        # no need to hash, simply add a timestamp at the beginning
        # and replace \\ to /
        new_filename = "{}-{}".format(int(time.time()), file.filename)
        new_full_filename = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        new_full_filename = new_full_filename.replace("\\", "/")

        # save the file
        file.save(new_full_filename)

        # update the resume_url
        student.resume_url = new_full_filename
        db.session.commit()

        # return the resume_url for that student id
        base_url = request.url_root
        response = {
            "resume_url": base_url + new_full_filename,
            "student_id": student_id
        }

        return jsonify(response)
