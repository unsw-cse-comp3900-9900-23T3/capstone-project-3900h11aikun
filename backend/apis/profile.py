from flask import request, abort, jsonify
from flask_restx import Resource, Namespace
from models.profile import *
from db.models import *

api = Namespace(
    "profile",
    description="get profile, edit profile"
)


@api.route("/profile")
class Login(Resource):
    def get(self):
        pass


@api.route("/project")
class Projects(Resource):
    @api.doc(description="Create new project")
    @api.expect(project_create_model)
    @api.response(200, 'create success')
    @api.response(400, 'invalid params')
    @api.response(401, 'only partner can create project')
    def post(self):
        data = request.get_json()

        if Partner.query.filter_by(partner_id=data["partner_id"]).first() is None:
            abort(401, 'unknown partner id')
        new_project = Project(
            partner_id=data['partner_id'],
            title=data['title'],
            description=data['description'],
            problem_statement=data['problem_statement'],
            desired_outcomes=data['desired_outcomes'],
            required_skills=data['required_skills'],
            deliverables=data['deliverables'],
            project_last_updated_at=datetime.now(),
            status='is_open',
        )
        db.session.add(new_project)
        db.session.commit()

        return jsonify(new_project.as_dict())

    @api.doc(description="Update project detail information")
    @api.expect(project_update_model)
    @api.response(200, 'update success')
    @api.response(400, 'invalid params')
    @api.response(401, 'only owner partner of project can update project')
    def put(self):
        data = request.get_json()

        project = Project.query.filter_by(project_id=data["project_id"], partner_id=data["partner_id"]).first()
        if project is None:
            abort(401, 'unknown project id or partner id is not owner')
        if 'title' in data:
            project.title = data['title']
        if 'description' in data:
            project.description = data['description']
        if 'problem_statement' in data:
            project.problem_statement = data['problem_statement']
        if 'desired_outcomes' in data:
            project.desired_outcomes = data['desired_outcomes']
        if 'required_skills' in data:
            project.required_skills = data['required_skills']
        if 'deliverables' in data:
            project.deliverables = data['deliverables']
        project.project_last_updated_at = datetime.now()

        db.session.commit()

        return jsonify(project.as_dict())


@api.route("/project/assign/student")
class ProjectAssignStudent(Resource):
    @api.doc(description="Assign student for project")
    @api.expect(project_assign_student_model)
    @api.response(200, 'assign success')
    @api.response(400, 'invalid params')
    @api.response(401, 'only owner partner of project can update project')
    def post(self):
        data = request.get_json()

        project = Project.query.filter_by(project_id=data["project_id"], partner_id=data["partner_id"]).first()
        if project is None:
            abort(401, 'unknown project id or partner id is not owner')
        student = Student.query.filter_by(student_id=data["student_id"]).first()
        if student is None:
            abort(401, 'unknown student id')

        project.student_id = student.student_id
        project.student_being_assigned_at = datetime.now()

        db.session.commit()

        return jsonify(project.as_dict())


@api.route("/project/assign/supervisor")
class ProjectAssignSupervisor(Resource):
    @api.doc(description="Assign supervisor for project")
    @api.expect(project_assign_supervisor_model)
    @api.response(200, 'assign success')
    @api.response(400, 'invalid params')
    @api.response(401, 'only owner partner of project can update project')
    def post(self):
        data = request.get_json()

        project = Project.query.filter_by(project_id=data["project_id"], partner_id=data["partner_id"]).first()
        if project is None:
            abort(401, 'unknown project id or partner id is not owner')
        supervisor = Supervisor.query.filter_by(supervisor_id=data["supervisor_id"]).first()
        if supervisor is None:
            abort(401, 'unknown supervisor id')

        project.supervisor_id = supervisor.supervisor_id
        project.supervisor_being_assigned_at = datetime.now()

        db.session.commit()

        return jsonify(project.as_dict())

