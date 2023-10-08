from flask_restx import fields, reqparse
from config import api

# login requires username and password, also require the user type.
# the user type: student, supervisor, partner only
login_model = api.model('login', {
    'type': fields.String(required=True, enum=['student', 'supervisor', 'partner'], description='user type'),
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password', default='Abcd1234!')
})

# student register:
# unique username, first_name, last_name, unique email,
# password (default Abcd1234!)
# avatar will be assigned randomly by the backend
# qualification, school_name, major, skills, strength
# and upload the file of resume
student_register_model = api.model('student_register', {
    'username': fields.String(required=True, description='unique username'),
    'first_name': fields.String(required=True, description='first name'),
    'last_name': fields.String(required=True, description='last name'),
    'email': fields.String(required=True, description='email', default='aaa@mail.com'),
    'password': fields.String(required=True, description='password', default='Abcd1234!'),
    'qualification': fields.String(required=True, description='qualification', default='qualification'),
    'school_name': fields.String(required=True, description='school name', default='school name'),
    'major': fields.String(required=True, description='major', default='major'),
    'skills': fields.String(required=True, description='skills', default='skills'),
    'strength': fields.String(required=True, description='strength', default='strength'),
})

from werkzeug.datastructures import FileStorage

# username, first_name, last_name, email, password, etc as above
student_register_with_resume_parser = reqparse.RequestParser()
student_register_with_resume_parser.add_argument('username', type=str, required=True, location='form', default='username')
student_register_with_resume_parser.add_argument('first_name', type=str, required=True,  location='form', default='first name')
student_register_with_resume_parser.add_argument('last_name', type=str, required=True,  location='form',default='last name')
student_register_with_resume_parser.add_argument('email', type=str, required=True, location='form', default='email@email.com')
student_register_with_resume_parser.add_argument('password', type=str, required=True, location='form', default='Abcd1234!')
student_register_with_resume_parser.add_argument('qualification', type=str, required=True, location='form', default='qualification')
student_register_with_resume_parser.add_argument('school_name', type=str, required=True, location='form', default='school name')
student_register_with_resume_parser.add_argument('major', type=str, required=True, location='form', default='major')
student_register_with_resume_parser.add_argument('skills', type=str, required=True, location='form', default='skills')
student_register_with_resume_parser.add_argument('strength', type=str, required=True, location='form', default='strength')

# also has a file
student_register_with_resume_parser.add_argument('file', type=FileStorage, location='files', required=True, help='resume file in pdf, doc, docx')



