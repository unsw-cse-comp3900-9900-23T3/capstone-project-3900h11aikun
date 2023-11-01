from flask import request, abort, jsonify
from flask_restx import Resource, Namespace
from models.profile import *
from db.models import *

api = Namespace(
    "profile",
    description="get profile, edit profile"
)


@api.route("/project")
class Projects(Resource):
    @api.doc(description="List project",
             params={'project_id': 'id of project', 'partner_id': 'partner id of project owner'})
    @api.response(200, 'get success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def get(self):
        data = request.args

        if 'project_id' in data:
            projects = Project.query.filter_by(project_id=data['project_id']).all()
        elif 'partner_id' in data:
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
    @api.doc(description="Student apply for project")
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
            reason="",
            last_updated_at=datetime.now(),
        )
        if 'reason' in data:
            new_student_interest.reason = data['reason']

        db.session.add(new_student_interest)
        db.session.commit()

        return jsonify(new_student_interest.as_dict())

    @api.doc(description="Get student interest express",
             params={"project_id": "id of project", "student_id": "id of student"}, )
    @api.response(200, 'get success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def get(self):
        data = request.args

        session = StudentInterestExpress.query
        if 'project_id' in data:
            session = session.filter_by(project_id=data['project_id'])
        if 'student_id' in data:
            session = session.filter_by(student_id=data['student_id'])
        session = session.join(Student, Student.student_id == StudentInterestExpress.student_id)
        session = session.join(Project, Project.project_id == StudentInterestExpress.project_id)
        session = session.add_columns(Student.first_name, Student.last_name, Student.skills,
                                      Student.school_name, Student.qualification, Project.title, Student.resume_url)

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
            temp['resume_url'] = express[7]
            res.append(temp)

        return jsonify(res)

    @api.doc(description="Student cancel apply for project")
    @api.expect(project_cancel_apply_student_model)
    @api.response(200, 'apply success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def delete(self):
        data = request.get_json()

        item = StudentInterestExpress.query.filter_by(project_id=data["project_id"],
                                                      student_id=data["student_id"]).first()
        if item is None:
            abort(401, 'project_id or student_id incorrect')
        db.session().delete(item)
        db.session.commit()
        return 200, "delete success"


@api.route("/project/interest/supervisor")
class SupervisorInterest(Resource):
    @api.doc(description="Get supervisor interest express",
             params={"project_id": "id of project", "supervisor_id": "id of supervisor"}, )
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
            reason="",
            last_updated_at=datetime.now(),
        )
        if 'reason' in data:
            new_supervisor_interest.reason = data['reason']

        db.session.add(new_supervisor_interest)
        db.session.commit()

        return jsonify(new_supervisor_interest.as_dict())

    @api.doc(description="Supervisor cancel apply for project")
    @api.expect(project_cancel_apply_supervisor_model)
    @api.response(200, 'apply success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def delete(self):
        data = request.get_json()

        item = SupervisorInterestExpress.query.filter_by(project_id=data["project_id"],
                                                         supervisor_id=data["supervisor_id"]).first()
        if item is None:
            abort(401, 'project_id or supervisor_id incorrect')
        db.session().delete(item)
        db.session.commit()
        return 200, "delete success"


@api.route("/student")
class Students(Resource):
    @api.doc(description="List students",
             params={"student_id": "student id",
                     "skills": "skills of student",
                     "qualification": "qualification of student",
                     "school_name": "school name of student"})
    @api.response(200, 'get success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def get(self):
        data = request.args

        session = Student.query
        if 'student_id' in data:
            session = session.filter(Student.student_id == data['student_id'])
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

    @api.doc(description="Update student detail information")
    @api.expect(student_update_model)
    @api.response(200, 'update success')
    @api.response(400, 'invalid params')
    @api.response(401, 'student id not found')
    def put(self):
        data = request.get_json()

        student = Student.query.filter_by(student_id=data["student_id"]).first()
        if student is None:
            abort(401, 'unknown student id')
        if 'username' in data:
            student.username = data['username']
        if 'first_name' in data:
            student.first_name = data['first_name']
        if 'last_name' in data:
            student.last_name = data['last_name']
        if 'email' in data:
            student.email = data['email']
        if 'avatar' in data:
            student.avatar = data['avatar']
        if 'qualification' in data:
            student.qualification = data['qualification']
        if 'school_name' in data:
            student.school_name = data['school_name']
        if 'major' in data:
            student.major = data['major']
        if 'skills' in data:
            student.skills = data['skills']
        if 'strength' in data:
            student.strength = data['strength']
        if 'resume_url' in data:
            student.resume_url = data['resume_url']
        db.session.commit()

        return jsonify(student.as_dict())


@api.route("/supervisor")
class Supervisors(Resource):
    @api.doc(description="List supervisors",
             params={"supervisor_id": "supervisor id",
                     "skills": "skills of supervisor",
                     "qualification": "qualification of supervisor",
                     "school_name": "school name of supervisor"})
    @api.response(200, 'get success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def get(self):
        data = request.args

        session = Supervisor.query
        if 'supervisor_id' in data:
            session = session.filter(Supervisor.supervisor_id == data['supervisor_id'])
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

    @api.doc(description="Update supervisor detail information")
    @api.expect(supervisor_update_model)
    @api.response(200, 'update success')
    @api.response(400, 'invalid params')
    @api.response(401, 'supervisor id not found')
    def put(self):
        data = request.get_json()

        supervisor = Supervisor.query.filter_by(supervisor_id=data["supervisor_id"]).first()
        if supervisor is None:
            abort(401, 'unknown supervisor id')
        if 'username' in data:
            supervisor.username = data['username']
        if 'first_name' in data:
            supervisor.first_name = data['first_name']
        if 'last_name' in data:
            supervisor.last_name = data['last_name']
        if 'email' in data:
            supervisor.email = data['email']
        if 'avatar' in data:
            supervisor.avatar = data['avatar']
        if 'qualification' in data:
            supervisor.qualification = data['qualification']
        if 'school_name' in data:
            supervisor.school_name = data['school_name']
        if 'skills' in data:
            supervisor.skills = data['skills']
        if 'resume_url' in data:
            supervisor.resume_url = data['resume_url']
        db.session.commit()

        return jsonify(supervisor.as_dict())


@api.route("/partner")
class Partners(Resource):
    @api.doc(description="List partners",
             params={"partner_id": "partner id"})
    @api.response(200, 'get success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def get(self):
        data = request.args

        session = Partner.query
        if 'partner_id' in data:
            session = session.filter(Partner.partner_id == data['partner_id'])
        partners = session.all()
        res = []
        for partner in partners:
            res.append(partner.as_dict())

        return jsonify(res)

    @api.doc(description="Update partner detail information")
    @api.expect(partner_update_model)
    @api.response(200, 'update success')
    @api.response(400, 'invalid params')
    @api.response(401, 'partner id not found')
    def put(self):
        data = request.get_json()

        partner = Partner.query.filter_by(partner_id=data["partner_id"]).first()
        if partner is None:
            abort(401, 'unknown partner id')
        if 'company' in data:
            partner.company = data['company']
        if 'position' in data:
            partner.position = data['position']
        if 'description' in data:
            partner.description = data['description']
        db.session.commit()

        return jsonify(partner.as_dict())


# skills must split by ','
def skill_matched(skill1, skill2):
    skills1 = skill1.split(', ')
    skills2 = skill2.split(', ')
    for s1 in skills1:
        s1 = s1.strip().strip('.')
        for s2 in skills2:
            s2 = s2.strip().strip('.')
            if s1 == s2:
                return True
    return False


@api.route("/recommend")
class RecommendProject(Resource):
    @api.doc(description="Get recommend project for student or supervisor",
             params={"student_id": "student id",
                     "supervisor_id": "supervisor id"})
    @api.response(200, 'get success')
    @api.response(400, 'invalid params')
    @api.response(401, '')
    def get(self):
        data = request.args

        if ('student_id' not in data) and ('supervisor_id' not in data):
            abort(401, 'student id or supervisor id not found')
        item = Student()
        if 'student_id' in data:
            item = Student.query.filter_by(student_id=data["student_id"]).first()
        else:
            item = Supervisor.query.filter_by(supervisor_id=data["supervisor_id"]).first()

        if item is None:
            abort(401, 'student id or supervisor id not found')

        skills = item.skills

        projects = Project.query.all()
        res = []
        for project in projects:
            if project.required_skills:
                if skill_matched(skills, project.required_skills):
                    res.append(project.as_dict())
        return jsonify(res)
