from config import db
from datetime import datetime
from flask import request


# create a base model with as_dict method
class BaseModel(db.Model):
    __abstract__ = True

    def as_dict(self):
        # ignore password field
        # and return the absolute url for avatar
        base_url = request.url_root

        result = {}
        for column in self.__table__.columns:
            if column.name == 'avatar':
                result["avatar"] = base_url + getattr(self, column.name)
            elif column.name == 'resume_url':
                # can be empty
                if getattr(self, column.name) is None:
                    result["resume_url"] = None
                else:
                    result["resume_url"] = base_url + getattr(self, column.name)
            elif column.name == 'file_url':
                # can be empty
                if getattr(self, column.name) is None:
                    result["file_url"] = None
                else:
                    result["file_url"] = base_url + getattr(self, column.name)
            elif column.name == 'password':
                continue
            else:
                result[column.name] = getattr(self, column.name)

        return result


# 3 tables: student, supervisor, partner
class Student(BaseModel):
    __tablename__ = 'student'
    __table_args__ = {"extend_existing": True}

    student_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String, nullable=False)

    qualification = db.Column(db.String, nullable=False)
    school_name = db.Column(db.String, nullable=False)
    major = db.Column(db.String, nullable=False)
    skills = db.Column(db.String, nullable=False)
    strength = db.Column(db.String, nullable=False)

    resume_url = db.Column(db.String, nullable=True, default=None)


class Supervisor(BaseModel):
    __tablename__ = 'supervisor'
    __table_args__ = {"extend_existing": True}

    supervisor_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String, nullable=False)

    qualification = db.Column(db.String, nullable=False)
    school_name = db.Column(db.String, nullable=False)
    skills = db.Column(db.String, nullable=False)

    resume_url = db.Column(db.String, nullable=True, default=None)


class Partner(BaseModel):
    __tablename__ = 'partner'
    __table_args__ = {"extend_existing": True}

    partner_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String, nullable=False)

    company = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

################################################################

# the partner creates the project
class Project(BaseModel):
    __tablename__ = 'project'
    __table_args__ = {"extend_existing": True}

    # each partner may have multiple project
    project_id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.partner_id'), nullable=False)

    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    # the project detail
    problem_statement = db.Column(db.String, nullable=False)
    desired_outcomes = db.Column(db.String, nullable=False)
    required_skills = db.Column(db.String, nullable=False)
    deliverables = db.Column(db.String, nullable=False)

    # timestamp for project creation
    project_last_updated_at = db.Column(db.DateTime, nullable=False)

    # the partner decides for supervisor id,
    # then the supervisor decides for student id
    # these two values are null at beginning
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.supervisor_id'), nullable=True, default=None)
    supervisor_being_assigned_at = db.Column(db.DateTime, nullable=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=True, default=None)
    student_being_assigned_at = db.Column(db.DateTime, nullable=True)

    # project has a flag: is_open, in_progres, closed
    status = db.Column(db.Enum('is_open', 'in_progress', 'closed'), nullable=False, default='is_open')

# the student express interests, and attach a sentence
class StudentInterestExpress(BaseModel):
    __tablename__ = 'student_interest_express'
    __table_args__ = {"extend_existing": True}

    # each student may have multiple interests to multiple projects
    student_interest_express_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    reason = db.Column(db.String, nullable=False)
    last_updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

# the supervisor also need to express interests to link project with student,
# also attach a sentence
class SupervisorInterestExpress(BaseModel):
    __tablename__ = 'supervisor_interest_express'
    __table_args__ = {"extend_existing": True}

    # each supervisor may have multiple interests to multiple projects
    supervisor_interest_express_id = db.Column(db.Integer, primary_key=True)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.supervisor_id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    reason = db.Column(db.String, nullable=False)
    last_updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

# the student reports for progress for the project,
# recorded with date, and content, and will be commented by the partner only
class ProjectProgress(BaseModel):
    __tablename__ = 'project_progress'
    __table_args__ = {"extend_existing": True}

    # each student may have multiple progress for a project
    project_progress_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)

    # the student can upload some text content, and a file url,
    # url can be null
    content = db.Column(db.String, nullable=False)
    file_url = db.Column(db.String, nullable=True, default=None)
    student_last_updated_at = db.Column(db.DateTime, nullable=False)

    # the partner will provide some comment only
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.partner_id'), nullable=True, default=None)
    partner_feedback = db.Column(db.String, nullable=True, default=None)
    partner_last_updated_at = db.Column(db.DateTime, nullable=True)


# the supervisor can provide feedback at all times
class ProjectSupervisorFeedback(BaseModel):
    __tablename__ = 'project_supervisor_feedback'
    __table_args__ = {"extend_existing": True}

    # each supervisor may have multiple feedback for a project
    project_supervisor_feedback_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.supervisor_id'), nullable=False)

    feedback = db.Column(db.String, nullable=False)
    supervisor_last_updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
