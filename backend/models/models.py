from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200), nullable=True)
    qualification = db.Column(db.String(200), nullable=True)
    school_name = db.Column(db.String(200), nullable=True)
    major = db.Column(db.String(200), nullable=True)
    skills = db.Column(db.String(200), nullable=True)
    strength = db.Column(db.String(200), nullable=True)
    resume_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Student %r>' % self.student_id

class Project(db.Model):
    __tablename__ = 'project'
    project_id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.partner_id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    problem_statement = db.Column(db.String(255), nullable=False)
    desired_outcomes = db.Column(db.String(255), nullable=False)
    required_skills = db.Column(db.String(255), nullable=False)
    deliverables = db.Column(db.String(255), nullable=False)
    project_last_updated_at = db.Column(db.DateTime, nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.supervisor_id'))
    supervisor_being_assigned_at = db.Column(db.DateTime)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    student_being_assigned_at = db.Column(db.DateTime)
    status = db.Column(db.String(11), nullable=False)

    def __repr__(self):
        return f"Project(project_id={self.project_id}, partner_id={self.partner_id}, title='{self.title}', " \
               f"description='{self.description}', problem_statement='{self.problem_statement}', " \
               f"desired_outcomes='{self.desired_outcomes}', required_skills='{self.required_skills}', " \
               f"deliverables='{self.deliverables}', project_last_updated_at='{self.project_last_updated_at}', " \
               f"supervisor_id={self.supervisor_id}, supervisor_being_assigned_at='{self.supervisor_being_assigned_at}', " \
               f"student_id={self.student_id}, student_being_assigned_at='{self.student_being_assigned_at}', status='{self.status}')"


class ProjectProgress(db.Model):
    __tablename__ = 'project_progress'

    project_progress_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(255))
    student_last_updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.partner_id'))
    partner_feedback = db.Column(db.String(255))
    partner_last_updated_at = db.Column(db.DateTime)

    project = db.relationship("Project", backref=db.backref("progress", cascade="all, delete-orphan"))
    student = db.relationship("Student")
    partner = db.relationship("Partner")

    def __repr__(self):
        return '<ProjectProgress project_progress_id={}>'.format(self.project_progress_id)