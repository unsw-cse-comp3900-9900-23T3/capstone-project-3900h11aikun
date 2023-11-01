from flask import request, abort, jsonify
from flask_restx import Resource, Namespace
from db.models import *
from models.project import *
from db.models import *
from config import app
import os
from sqlalchemy import or_


api = Namespace(
    "project",
    description="get project, edit project"
)



@api.route('/project/<int:student_id>/projects')
class ProjectsByStudent(Resource):
    @api.doc(description="Get project By student detail")
    @api.response(200, 'Success')
    @api.response(404, 'Project not found')
    def get(self, student_id):

        
        student = Student.query.get(student_id)

        if student is None:
            return {'message': 'Student not found'}, 404

        
        skills = student.skills.split(',')

        
        matched_projects = Project.query.filter(
            or_(*[Project.required_skills.like(f"%{skill}%") for skill in skills])).all()

        
        projects = []
        for project in matched_projects:
            projects.append({
                'project_id': project.project_id,
                'title': project.title,
                'description': project.description,
            })

        return {
            'student_id': student.student_id,
            'username': student.username,
            'skills': student.skills,
            'matched_projects': projects
        }, 200


@api.route('/project/<int:student_id>/upload')
class FileUpload(Resource):
    @api.doc(description='Upload files to designated students and projects')
    def post(self, student_id):
        data = request.json

        project_id = data.get('project_id')
        content = data.get('content')

        file = request.files['file']
        if file.filename == '':
            return {'message': 'No file selected'}, 400

        file_path = f'uploads/{file.filename}'
        file.save(file_path)


        progress = ProjectProgress(
            project_id=project_id,
            student_id=student_id,
            content=content,
            file_url=file_path
        )

        db.session.add(progress)

        db.session.commit()

        return {'message': 'File uploaded successfully', 'student_id': student_id, 'project_id': project_id}
