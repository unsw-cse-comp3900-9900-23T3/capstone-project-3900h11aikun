import sqlite3
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request, send_from_directory, g
import os

app = Flask(__name__)

DATABASE = 'projects.db'
UPLOAD_FOLDER = 'uploads'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/db/raw_data/avatars/<path:filename>', methods=['GET'])
def get_avatar(filename):
    """
    从'static/avatars'The endpoint to get the avatar image from the directory.
    """
    return send_from_directory('static/avatars', filename)



@app.route('/students/<int:student_id>/profile', methods=['PUT'])
def update_student_profile(student_id):
    """
    Endpoint for updating student profile information.
    """
    student_data = request.get_json()
    student_education = student_data.get('education', '')
    student_major = student_data.get('major', '')
    student_skills = student_data.get('skills', '')
    student_strength = student_data.get('strength', '')

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET education=?, major=?, skills=?, strength=? WHERE id=?",
                       (student_education, student_major, student_skills, student_strength, student_id))
        conn.commit()

    return jsonify({"message": "Student profile updated successfully"})


@app.route('/mentors/<int:mentor_id>/upload_resume', methods=['POST'])
def upload_mentor_resume(mentor_id):
    """
    Endpoint for academic tutors to upload resumes.
    """
    if 'file' not in request.files:
        return jsonify({"message": "File not found"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "File not found"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE mentors SET resume=? WHERE id=?", (filename, mentor_id))
            conn.commit()

        return jsonify({"message": "Resume uploaded successfully"})

    return jsonify({"message": "Unsupported file format"})


def allowed_file(filename):
    """
    Check if the file extension is PDF.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'


@app.route('/projects', methods=['GET'])
def get_project_list():
    """
    Endpoint to get the list of items.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT project_name, project_type, student_requirements FROM projects")
        projects = cursor.fetchall()

    project_list = []
    for project in projects:
        project_name, project_type, student_requirements = project
        project_list.append({
            'project_name': project_name,
            'project_type': project_type,
            'student_requirements': student_requirements
        })

    return jsonify(project_list)

@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project_details(project_id):
    """
    Endpoint to get project details.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT project_name, problem_statement, project_results, required_skills, deliverables FROM projects WHERE id=?", (project_id,))
        project = cursor.fetchone()

    if project is None:
        return jsonify({"message": "No project found"})

    project_name, problem_statement, project_results, required_skills, deliverables = project
    project_details = {
        'project_name': project_name,
        'problem_statement': problem_statement,
        'project_results': project_results,
        'required_skills': required_skills,
        'deliverables': deliverables
    }

    return jsonify(project_details)


@app.route('/projects/<int:project_id>/apply', methods=['POST'])
def apply_for_project(project_id):
    """
    The endpoint of the application project.
    """
    # Process the logic for students to submit applications, such as saving application information to the database or sending notifications, etc.
    # ...

    return jsonify({"message": "Application has been submitted"})
@app.route('/students/<int:student_id>/recommended_projects', methods=['GET'])
def get_recommended_projects(student_id):
    """
    Get the endpoint for recommended items.
    """
    # Capture students’ key skills
    student_skills = get_student_skills(student_id)

    if not student_skills:
        return jsonify({"message": "No student or student skills information found"})

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, project_name, project_type, student_requirements FROM projects")
        projects = cursor.fetchall()

    recommended_projects = []
    for project in projects:
        project_id, project_name, project_type, student_requirements = project
        required_skills = parse_student_requirements(student_requirements)

        if skills_match(student_skills, required_skills):
            recommended_projects.append({
                'project_id': project_id,
                'project_name': project_name,
                'project_type': project_type,
                'student_requirements': student_requirements
            })

    return jsonify(recommended_projects)


def get_student_skills(student_id):
    """
    Obtain students' main skills from the database.
    These are just examples, you will need to adjust accordingly based on your data model and database structure.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT skills FROM students WHERE id=?", (student_id,))
        row = cursor.fetchone()

    if row:
        return row[0]

    return None


def parse_student_requirements(student_requirements):
    """
    Parse the student requirements for the project and return the skills list.
    These are just examples, you will need to parse accordingly based on the representation of your data model and skill requirements.
    """
    return student_requirements.split(',')


def skills_match(student_skills, required_skills):
    """
    Check whether the student's skills meet the program's skill requirements.
    These are just examples, you can adjust them accordingly according to your matching rules.
    """
    student_skill_set = set(student_skills)
    required_skill_set = set(required_skills)

    return required_skill_set.issubset(student_skill_set)


from flask import request


@app.route('/projects/<int:project_id>/apply', methods=['POST'])
def apply_for_project(project_id):
    """
    The endpoint of applying to a program, where students submit their resume to the program.
    """
    # Check if students have uploaded resume files
    if 'resume' not in request.files:
        return jsonify({"message": "Uploaded resume file not found"})

    resume_file = request.files['resume']

    # Check if the file type is PDF
    if not allowed_file(resume_file.filename):
        return jsonify({"message": "Only PDF files allowed to be uploaded"})

    # Save resume file to disk or database
    save_resume(resume_file, project_id)

    # Other processing logic, such as sending notifications, etc.

    return jsonify({"message": "Resume has been submitted"})


def allowed_file(filename):
    """
    Check if the file type is PDF.
    These are just examples, you can adjust the validation rules for file types as needed。
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'


def save_resume(resume_file, project_id):
    """
    Save resume file to disk or database.
    These are just examples, you need to implement them accordingly according to your needs.
    """
    # Generate saved file name based on project ID
    filename = f"resume_{project_id}.pdf"

    # Save resume file to specified location
    resume_file.save(filename)

    # Other processing logic, such as saving the file path to the database

@app.route('/students/<int:student_id>/applied_projects', methods=['GET'])
def get_applied_projects(student_id):
    """
    Other processing logic, such as saving the file path to the database
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT project_id, project_name, application_status FROM applications WHERE student_id=?", (student_id,))
        applied_projects = cursor.fetchall()

    project_list = []
    for project in applied_projects:
        project_id, project_name, application_status = project
        project_list.append({
            'project_id': project_id,
            'project_name': project_name,
            'application_status': application_status
        })

    return jsonify(project_list)


@app.route('/students/<int:student_id>/applied_projects/<int:project_id>', methods=['DELETE'])
def delete_applied_project(student_id, project_id):
    """
    Delete the endpoint for projects that students have applied for.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM applications WHERE student_id=? AND project_id=?", (student_id, project_id))
        conn.commit()

    return jsonify({"message": "Project application successfully deleted"})


# Suppose there is a table named "applications" in the database, which is used to store project application information, 
including fields such as student ID, project ID, and application status.
# When students submit project applications, the corresponding records need to be inserted into the "applications" table.

@app.route('/advisors/<int:advisor_id>/projects', methods=['GET'])
def get_projects_for_advisor(advisor_id):
    """
    Endpoint to get the academic tutor's project list.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT project_id, project_name, project_type, advisor_requirements FROM projects WHERE advisor_id=?", (advisor_id,))
        projects = cursor.fetchall()

    project_list = []
    for project in projects:
        project_id, project_name, project_type, advisor_requirements = project
        project_list.append({
            'project_id': project_id,
            'project_name': project_name,
            'project_type': project_type,
            'advisor_requirements': advisor_requirements
        })

    return jsonify(project_list)


# Assume that there is a table named "projects" in the database, which is used to store project information, including fields such as project ID, 
project name, project type, and requirements for academic tutors.
# When creating a project, you need to insert the corresponding record into the "projects" table and associate it with the corresponding academic tutor.

if __name__ == '__main__':
    app.run()