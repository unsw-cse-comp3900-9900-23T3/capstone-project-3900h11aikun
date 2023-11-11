from flask import request, abort, jsonify
from flask_restx import Resource, Namespace
from db.models import *
from models.progress import *
from db.models import *
from config import app
import os
import time


api = Namespace(
    "progress",
    description="get all progress for a project, edit progress (text & file), delete progress, partner mark progress"
)


@api.route("/all_progress/<int:project_id>")
class GetAllProgress(Resource):
    @api.doc(description="This will return both the project dict, and the all progress into a list")
    @api.response(200, "Success, return the project dict and all progress dicts into a list")
    @api.response(400, "Project not found")
    def get(self, project_id):
        """for a project, get its project dict and all progresses in one list"""
        project = Project.query.get(project_id)
        if project is None:
            abort(400, "Project id {} not found".format(project_id))

        # get all the progress related to this project id
        # order by the project_progress_id by default
        all_progress = ProjectProgress.query.filter_by(project_id=project_id).all()

        # create a list to store all the progress dicts
        all_progress_list = [p.as_dict() for p in all_progress]

        # response
        response = {
            "project": project.as_dict(),
            "all_progress": all_progress_list,
        }

        return jsonify(response)


@api.route("")
class CreateNewProgress(Resource):
    @api.doc(description="The student create a new progress for a given project, in text message")
    @api.response(200, "Success, return the new progress dict")
    @api.response(400, "Invalid parameter / Project not found / Student does not belong to the project, etc")
    @api.expect(new_progress_model)
    def post(self):
        """student post a new progress in text first!!! For file, use the progress/file/<progress_id> route"""

        data = request.json

        # check if the project exists
        project = Project.query.get(data["project_id"])
        if project is None:
            abort(400, "Project id {} not found".format(data["project_id"]))

        # check if the student exist
        student = Student.query.get(data["student_id"])
        if student is None:
            abort(400, "Student id {} not found".format(data["student_id"]))

        # check if the student belongs to the project
        if project.student_id != student.student_id:
            abort(400, "Student id {} does not belong to project id {}".format(student.student_id, project.project_id))

        # create a new progress
        new_progress = ProjectProgress(
            project_id=data["project_id"],
            student_id=data["student_id"],
            content=data["content"],
            file_url=None,
            student_last_updated_at=datetime.now(),
            partner_id=project.partner_id,
            partner_feedback=None,
            partner_last_updated_at=None
        )

        # add to the database and return
        db.session.add(new_progress)
        db.session.commit()
        return jsonify(new_progress.as_dict())


@api.route("/<int:progress_id>")
class ProgressDeleteAction(Resource):
    @api.doc(description="Delete the progress")
    @api.response(200, "Success delete, nothing is returned")
    @api.response(400, "Progress id not found / other error")
    def delete(self, progress_id):
        """student / partner can choose to delete the whole progress. this will remove the whole progress"""

        progress = ProjectProgress.query.get(progress_id)
        if not progress:
            abort(400, "Progress id {} not found".format(progress_id))

        # delete the progress
        db.session.delete(progress)
        db.session.commit()
        return jsonify({})


    @api.doc(description="Get a progress by progress_id")
    @api.response(200, "Success, return the new progress dict")
    @api.response(400, "Progress id not found / other error")
    def get(self, progress_id):
        """anyone can get a progress by progress_id"""

        progress = ProjectProgress.query.get(progress_id)
        if not progress:
            abort(400, "Progress id {} not found".format(progress_id))

        return jsonify(progress.as_dict())


@api.route("/file/<int:progress_id>")
class ProgressFile(Resource):
    @api.doc(description="Delete the file from the progress")
    @api.response(200, "Success delete, return the new progress dict")
    @api.response(400, "Progress id not found / No file selected / other error")
    def delete(self, progress_id):
        """student delete the file for a particular progress"""

        # get that progress id and check
        progress = ProjectProgress.query.get(progress_id)
        if progress is None:
            abort(400, "Progress id {} not found".format(progress_id))

        # just update that url to None
        progress.file_url = None
        progress.student_last_updated_at = datetime.now()
        db.session.commit()
        return jsonify(progress.as_dict())


    @api.doc(description="put a new file for that progress")
    @api.response(200, "Success, return the new progress dict")
    @api.response(400, "Progress id not found / No file selected / other error")
    @api.expect(progress_file_parser)
    def put(self, progress_id):
        """student, after posting a new project, now upload a file to the progress, if file already exist, the new file will replace the old one"""

        # get that progress id and check
        progress = ProjectProgress.query.get(progress_id)
        if progress is None:
            abort(400, "Progress id {} not found".format(progress_id))

        if 'file' not in request.files:
            abort(400, "No file selected")

        # if there is a file, then also add the file to the new progress
        # give it a new name
        file = request.files['file']
        new_filename = "{}-{}".format(int(time.time()), file.filename)
        new_full_filename = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        new_full_filename = new_full_filename.replace("\\", "/")

        # now save to the uploads folder
        file.save(new_full_filename)

        # update the url
        progress.file_url = new_full_filename
        progress.student_last_updated_at = datetime.now()
        db.session.commit()
        return jsonify(progress.as_dict())


@api.route("/text/<int:progress_id>")
class ProgressAction(Resource):
    @api.doc(description="Edit the progress, only the content can be edited, " +
        "for the file, please use the /file<progress_id> route")
    @api.response(200, "Success, return the new progress dict")
    @api.response(400, "Progress id not found / other error")
    @api.expect(edit_progress_model)
    def put(self, progress_id):
        """student edit the progress text at here"""

        progress = ProjectProgress.query.get(progress_id)
        if not progress:
            abort(400, "Progress id {} not found".format(progress_id))

        # update the content
        data = request.json
        new_content = data["content"]

        progress.content = new_content
        progress.student_last_updated_at = datetime.now()
        db.session.commit()
        return jsonify(progress.as_dict())


@api.route("/partner_feedback/<int:progress_id>")
class PartnerFeedbackAction(Resource):
    @api.doc(description="Partner give / edit the feedback to the progress")
    @api.response(200, "Success, return the new progress dict")
    @api.response(400, "Progress id not found / other error")
    @api.expect(new_partner_feedback_model)
    def put(self, progress_id):
        """the partner can give feedback to the progress, and if the partner already give feedback, then this will replace the old feedback"""

        progress = ProjectProgress.query.get(progress_id)
        if not progress:
            abort(400, "Progress id {} not found".format(progress_id))

        # check the partner
        data = request.json
        partner = Partner.query.get(data["partner_id"])
        if not partner:
            abort(400, "Partner id {} not found".format(data["partner_id"]))

        # check if the progress.partner_id is the same as the partner_id
        if progress.partner_id != partner.partner_id:
            abort(400, "Progress id {} does not belong to partner id {}".format(progress_id, partner.partner_id))

        # now add the feedback
        progress.partner_feedback = data["partner_feedback"]
        progress.partner_last_updated_at = datetime.now()
        db.session.commit()
        return jsonify(progress.as_dict())


    @api.doc(description="Partner delete the feedback to the progress, " +
        "will only delete the partner_feedback and partner_last_updated_at, only student can choose to delete the whole progress")
    @api.response(200, "Success, return the new progress dict")
    @api.response(400, "Progress id not found / other error")
    def delete(self, progress_id):
        """partner can choose to delete his feedback, so only partner_feedback and partner_last_updated_at will be deleted"""

        progress = ProjectProgress.query.get(progress_id)
        if not progress:
            abort(400, "Progress id {} not found".format(progress_id))

        # delete the feedback
        progress.partner_feedback = None
        progress.partner_last_updated_at = None
        db.session.commit()
        return jsonify(progress.as_dict())

