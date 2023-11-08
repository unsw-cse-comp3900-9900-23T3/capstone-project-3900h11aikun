from flask_restx import fields, reqparse
from config import api


project_list_params_model = api.model('ProjectListParams', {
    'title': fields.String(description='Title of the project (optional)'),
    'page': fields.Integer(description='Page number (optional, default=1)'),
    'limit': fields.Integer(description='Number of projects per page (optional, default=10)')
})


project_update_model = api.model('project_update', {
    'project_id': fields.Integer(required=True, description='ID of the project to be updated'),
    'title': fields.String(description='Updated title of the project'),
    'description': fields.String(description='Updated description of the project'),
    'problem_statement': fields.String(description='Updated problem statement of the project'),
    'desired_outcomes': fields.String(description='Updated desired outcomes of the project'),
    'required_skills': fields.String(description='Updated required skills of the project'),
    'deliverables': fields.String(description='Updated deliverables of the project'),
    'project_last_updated_at': fields.DateTime(description='Updated last updated timestamp of the project'),
    'supervisor_id': fields.Integer(description='Updated supervisor ID assigned to the project'),
    'supervisor_being_assigned_at': fields.DateTime(description='Updated timestamp when the supervisor was assigned to the project'),
    'student_id': fields.Integer(description='Updated student ID assigned to the project'),
    'student_being_assigned_at': fields.DateTime(description='Updated timestamp when the student was assigned to the project'),
    'status': fields.String(required=False, description='status of project', default="is_open", enum=["is_open", "in_progress", "closed"])
})
