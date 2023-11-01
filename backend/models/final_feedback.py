from flask_restx import fields, reqparse
from config import api

# a supervisor feedback
supervisor_feedback_model = api.model('new_feedback', {
    'project_id': fields.Integer(required=True, description='project id'),
    'supervisor_id': fields.Integer(required=True, description='supervisor id'),
    'feedback': fields.String(required=True, description='feedback content in text'),
})
