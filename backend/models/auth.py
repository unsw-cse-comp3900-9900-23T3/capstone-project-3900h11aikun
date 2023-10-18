from flask_restx import fields, reqparse
from config import api
from werkzeug.datastructures import FileStorage

# login requires username and password, also require the user type.
# the user type: student, supervisor, partner only
login_model = api.model('login', {
    'type': fields.String(required=True, enum=['student', 'supervisor', 'partner'], description='user type'),
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password', default='Abcd1234!')
})

login_model_with_email = api.model('login_with_email', {
    'type': fields.String(required=True, enum=['student', 'supervisor', 'partner'], description='user type'),
    'email': fields.String(required=True, description='email', default="danny-johnson@student.edu.au"),
    'password': fields.String(required=True, description='password', default='Abcd1234!')
})

# register: requires username, password, email, type
# and require unique username and password across every user type
register_model = api.model('register', {
    'username': fields.String(required=True, description='unique username', default='username'),
    'password': fields.String(required=True, description='password', default='Abcd1234!'),
    'email': fields.String(required=True, description='email', default='user@email.com'),
    'type': fields.String(required=True, enum=['student', 'supervisor', 'partner'], description='user type')
})


# validate the token in the Authorization header only
# this is a sample of how to use the token
token_parser = reqparse.RequestParser()
token_parser.add_argument('Authorization', location='headers', required=True, help='put-the-token-here!!!')


