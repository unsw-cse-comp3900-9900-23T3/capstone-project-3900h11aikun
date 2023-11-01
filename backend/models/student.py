from flask_restx import fields, reqparse
from config import api
from werkzeug.datastructures import FileStorage


student_update_model = api.model('student_update', {
    'student_id': fields.Integer(required=True, description='ID of the student to be updated'),
    'username': fields.String(description='Updated username of the student'),
    'first_name': fields.String(description='Updated first name of the student'),
    'last_name': fields.String(description='Updated last name of the student'),
    'email': fields.String(description='Updated email address of the student'),
    'password': fields.String(description='Updated password of the student'),
    'avatar': fields.String(description='Updated avatar URL of the student'),
    'qualification': fields.String(description='Updated qualification of the student'),
    'school_name': fields.String(description='Updated school name of the student'),
    'major': fields.String(description='Updated major of the student'),
    'skills': fields.String(description='Updated skills of the student'),
    'strength': fields.String(description='Updated strength of the student'),
    'resume_url': fields.String(description='Updated resume URL of the student'),
})

# the student can upload a file of resume
student_resume_parser = reqparse.RequestParser()
student_resume_parser.add_argument('file', type=FileStorage, location='files', required=True, help='resume file in pdf, doc, docx')

