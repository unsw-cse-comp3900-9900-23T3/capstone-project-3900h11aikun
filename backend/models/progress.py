from flask_restx import fields, reqparse
from config import api
from werkzeug.datastructures import FileStorage

# the progress can trigger the upload of a file
progress_file_parser = reqparse.RequestParser()
progress_file_parser.add_argument(
    'file', type=FileStorage, location='files', required=True,
    help='file in any format, such as pdf, doc, docx, zip, tar, jpg, etc')


# a new progress
# status choose from 'to do', 'in progress', 'done'
new_progress_model = api.model('new_progress', {
    'project_id': fields.Integer(required=True, description='project id'),
    'student_id': fields.Integer(required=True, description='student id'),
    'content': fields.String(required=True, description='progress content in text'),
    'deadline': fields.DateTime(required=False, description='deadline of the progress (not required)'),
    'sprint_objective': fields.String(required=True, description='sprint objective'),
    'user_story': fields.String(required=True, description='user story'),
    'status': fields.String(enum=['to do', 'in progress', 'done'], required=True, default="done", description='status of the progress'),
})


# edit a progress
edit_progress_model = api.model('edit_progress', {
    'content': fields.String(required=True, description='progress content in text'),
    'deadline': fields.DateTime(required=False, description='deadline of the progress (not required)'),
    'sprint_objective': fields.String(required=True, description='sprint objective'),
    'user_story': fields.String(required=True, description='user story'),
    'status': fields.String(enum=['to do', 'in progress', 'done'], required=True, default="done", description='status of the progress'),
})


# partner add a feedback to a progress
new_partner_feedback_model = api.model('new_partner_feedback', {
    "partner_id": fields.Integer(required=True, description='partner id'),
    "partner_feedback": fields.String(required=True, description='feedback content in text'),
    "partner_mark": fields.Integer(required=True, description='partner mark'),
})


