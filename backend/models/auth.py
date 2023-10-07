from flask_restx import fields, reqparse
from config import api

# login requires username and password, also require the user type.
# the user type: student, supervisor, partner only
login_model = api.model('login', {
    'type': fields.String(required=True, enum=['student', 'supervisor', 'partner'], description='user type'),
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password', default='Abcd1234!')
})





