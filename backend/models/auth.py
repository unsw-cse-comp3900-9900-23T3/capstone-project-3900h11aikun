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
    'email': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='password', default='Abcd1234!'),
    'qualification': fields.String(required=True, description='qualification'),
    'school_name': fields.String(required=True, description='school name'),
    'major': fields.String(required=True, description='major'),
    'skills': fields.String(required=True, description='skills'),
    'strength': fields.String(required=True, description='strength')
})




