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
    @api.doc(description="List project")
    @api.response(200, 'get success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def get(self):
        data = request.args

        if 'partner_id' in data:
            projects = Project.query.filter_by(partner_id=data['partner_id']).all()
        else:
            projects = Project.query.all()
        res = []
        for project in projects:
            res.append(project.as_dict())

        return jsonify(res)

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


@api.route("/project/interest/student")
class StudentInterest(Resource):
    @api.doc(description="Assign student for project")
    @api.expect(project_apply_student_model)
    @api.response(200, 'apply success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def post(self):
        data = request.get_json()

        if Student.query.filter_by(student_id=data["student_id"]).first() is None:
            abort(401, 'unknown student id')
        if Project.query.filter_by(project_id=data["project_id"]).first() is None:
            abort(401, 'unknown project id')
        new_student_interest = StudentInterestExpress(
            student_id=data["student_id"],
            project_id=data["project_id"],
            reason=data["reason"],
            last_updated_at=datetime.now(),
        )

        db.session.add(new_student_interest)
        db.session.commit()

        return jsonify(new_student_interest.as_dict())

    @api.doc(description="Get student interest express")
    @api.response(200, 'get success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def get(self):
        data = request.args

        session = StudentInterestExpress.query
        if 'project_id' in data:
            session = session.filter_by(project_id=data['project_id'])
        if 'student_id' in data:
            session = session.filter_by(student_id=data['student_id']).all()
        session = session.join(Student, Student.student_id == StudentInterestExpress.student_id)
        session = session.join(Project, Project.project_id == StudentInterestExpress.project_id)
        session = session.add_columns(Student.first_name, Student.last_name, Student.skills,
                                      Student.school_name, Student.qualification, Project.title)

        expresses = session.all()
        res = []
        for express in expresses:
            temp = express[0].as_dict()
            temp['first_name'] = express[1]
            temp['last_name'] = express[2]
            temp['skills'] = express[3]
            temp['school_name'] = express[4]
            temp['qualification'] = express[5]
            temp['title'] = express[6]
            res.append(temp)

        return jsonify(res)


@api.route("/project/interest/supervisor")
class SupervisorInterest(Resource):
    @api.doc(description="Get supervisor interest express")
    @api.response(200, 'get success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def get(self):
        data = request.args

        session = SupervisorInterestExpress.query
        if 'project_id' in data:
            session = session.filter_by(project_id=data['project_id'])
        if 'supervisor_id' in data:
            session = session.filter_by(supervisor_id=data['supervisor_id'])
        session = session.join(Supervisor, Supervisor.supervisor_id == SupervisorInterestExpress.supervisor_id)
        session = session.join(Project, Project.project_id == SupervisorInterestExpress.project_id)
        session = session.add_columns(Supervisor.first_name, Supervisor.last_name, Supervisor.skills,
                                      Supervisor.school_name, Supervisor.qualification, Project.title)

        expresses = session.all()
        res = []
        for express in expresses:
            temp = express[0].as_dict()
            temp['first_name'] = express[1]
            temp['last_name'] = express[2]
            temp['skills'] = express[3]
            temp['school_name'] = express[4]
            temp['qualification'] = express[5]
            temp['title'] = express[6]
            res.append(temp)

        return jsonify(res)

    @api.doc(description="Apply for project")
    @api.expect(project_apply_supervisor_model)
    @api.response(200, 'apply success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def post(self):
        data = request.get_json()

        if Supervisor.query.filter_by(supervisor_id=data["supervisor_id"]).first() is None:
            abort(401, 'unknown supervisor id')
        if Project.query.filter_by(project_id=data["project_id"]).first() is None:
            abort(401, 'unknown project id')
        new_supervisor_interest = SupervisorInterestExpress(
            supervisor_id=data["supervisor_id"],
            project_id=data["project_id"],
            reason=data["reason"],
            last_updated_at=datetime.now(),
        )

        db.session.add(new_supervisor_interest)
        db.session.commit()

        return jsonify(new_supervisor_interest.as_dict())


@api.route("/student")
class Students(Resource):
    @api.doc(description="List students")
    @api.response(200, 'get success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def get(self):
        data = request.args

        session = Student.query
        if 'skills' in data:
            session = session.filter(Student.skills.like('%%%s%%' % data['skills']))
        if 'qualification' in data:
            session = session.filter(Student.qualification.like('%%%s%%' % data['qualification']))
        if 'school_name' in data:
            session = session.filter(Student.school_name.like('%%%s%%' % data['school_name']))
        students = session.all()
        res = []
        for student in students:
            res.append(student.as_dict())

        return jsonify(res)


@api.route("/supervisor")
class Supervisors(Resource):
    @api.doc(description="List supervisors")
    @api.response(200, 'get success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def get(self):
        data = request.args

        session = Supervisor.query
        if 'skills' in data:
            session = session.filter(Supervisor.skills.like('%%%s%%' % data['skills']))
        if 'qualification' in data:
            session = session.filter(Supervisor.qualification.like('%%%s%%' % data['qualification']))
        if 'school_name' in data:
            session = session.filter(Supervisor.school_name.like('%%%s%%' % data['school_name']))
        supervisors = session.all()
        res = []
        for supervisor in supervisors:
            res.append(supervisor.as_dict())

        return jsonify(res)
