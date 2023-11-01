from flask_restx import fields, reqparse
from config import api
from werkzeug.datastructures import FileStorage


project_get_model = api.model('project_get', {
    'partner_id': fields.Integer(required=False, description='partner id of project owner'),
    'project_id': fields.Integer(required=False, description='project id'),
})

# project create requires project id, partner id and the detail information of project
project_create_model = api.model('project_create', {
    'partner_id': fields.Integer(required=True, description='partner id of project owner'),
    'title': fields.String(required=True, description='title of project'),
    'description': fields.String(required=True, description='description of project'),
    'problem_statement': fields.String(required=True, description='problem statement of project'),
    'desired_outcomes': fields.String(required=True, description='desired outcomes of project'),
    'required_skills': fields.String(required=True, description='required skills of project'),
    'deliverables': fields.String(required=True, description='deliverables of project'),
})


# project update requires project id and partner id of the project owner
# only the owner can update project information
project_update_model = api.model('project_update', {
    'project_id': fields.Integer(required=True, description='project id'),
    'partner_id': fields.Integer(required=True, description='partner id of project owner'),
    'title': fields.String(required=False, description='title of project'),
    'description': fields.String(required=False, description='description of project'),
    'problem_statement': fields.String(required=False, description='problem statement of project'),
    'desired_outcomes': fields.String(required=False, description='desired outcomes of project'),
    'required_skills': fields.String(required=False, description='required skills of project'),
    'deliverables': fields.String(required=False, description='deliverables of project'),
    'status': fields.String(required=False, description='status of project'),
})


# project assign student requires project id, partner id of the project owner and student id to be assigned
project_assign_student_model = api.model('project assign student', {
    'project_id': fields.Integer(required=True, description='project id'),
    'partner_id': fields.Integer(required=True, description='partner id of project owner'),
    'student_id': fields.Integer(required=True, description='student id to be assigned'),
})


# project assign supervisor requires project id, partner id of the project owner and supervisor id to be assigned
project_assign_supervisor_model = api.model('project assign supervisor', {
    'project_id': fields.Integer(required=True, description='project id'),
    'partner_id': fields.Integer(required=True, description='partner id of project owner'),
    'supervisor_id': fields.Integer(required=True, description='supervisor id to be assigned'),
})


# project apply student requires project id, partner id of the project owner and student id to be assigned
project_apply_student_model = api.model('student_apply_project', {
    'project_id': fields.Integer(required=True, description='project id'),
    'student_id': fields.Integer(required=True, description='student id'),
    'reason': fields.String(required=False, description='apply reason'),
})

project_cancel_apply_student_model = api.model('student_cancel_apply_project', {
    'project_id': fields.Integer(required=True, description='project id'),
    'student_id': fields.Integer(required=True, description='student id'),
})

# project apply supervisor requires project id, partner id of the project owner and supervisor id to be assigned
project_apply_supervisor_model = api.model('project_assign_student', {
    'project_id': fields.Integer(required=True, description='project id'),
    'supervisor_id': fields.Integer(required=True, description='supervisor id'),
    'reason': fields.String(required=False, description='apply reason'),
})

project_cancel_apply_supervisor_model = api.model('supervisor_cancel_apply_project', {
    'project_id': fields.Integer(required=True, description='project id'),
    'supervisor_id': fields.Integer(required=True, description='supervisor id'),
})

student_update_model = api.model('student update', {
    'student_id': fields.Integer(required=True, description='student id'),
    'username': fields.String(required=False, description='username'),
    'first_name': fields.String(required=False, description='first_name'),
    'last_name': fields.String(required=False, description='last_name'),
    'email': fields.String(required=False, description='email'),
    'avatar': fields.String(required=False, description='avatar'),
    'qualification': fields.String(required=False, description='qualification'),
    'school_name': fields.String(required=False, description='school name'),
    'major': fields.String(required=False, description='major'),
    'skills': fields.String(required=False, description='skills'),
    'strength': fields.String(required=False, description='strength'),
    'resume_url': fields.String(required=False, description='resume_url'),
})

supervisor_update_model = api.model('supervisor update', {
    'supervisor_id': fields.Integer(required=True, description='supervisor id'),
    'username': fields.String(required=False, description='username'),
    'first_name': fields.String(required=False, description='first_name'),
    'last_name': fields.String(required=False, description='last_name'),
    'email': fields.String(required=False, description='email'),
    'avatar': fields.String(required=False, description='avatar'),
    'qualification': fields.String(required=False, description='qualification'),
    'school_name': fields.String(required=False, description='school name'),
    'skills': fields.String(required=False, description='skills'),
    'resume_url': fields.String(required=False, description='resume_url'),
})

partner_update_model = api.model('partner update', {
    'partner_id': fields.Integer(required=True, description='partner id'),
    'first_name': fields.String(required=False, description='first name'),
    'last_name': fields.String(required=False, description='last name'),
    'email': fields.String(required=False, description='email'),
    'company': fields.String(required=False, description='company'),
})
