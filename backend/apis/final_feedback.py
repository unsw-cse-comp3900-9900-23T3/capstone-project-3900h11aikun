from flask import request, abort, jsonify
from flask_restx import Resource, Namespace
from db.models import *
from models.final_feedback import *
from db.models import *
from config import app
import os
import time
from datetime import datetime
from sqlalchemy import desc

api = Namespace(
    "final_feedback",
    description="supervisor leaves !! one !! final feedback for a project"
)


@api.route("/supervisor/<int:project_id>")
class PostNewFeedback(Resource):
    @api.doc(description="The supervisor post a new feedback for a given project, in text message")
    @api.response(200, "Success, return the new feedback dict")
    @api.response(400, "Feedback already exist / Project not found / Feedback not found / Supervisor does not belong to the project")
    @api.expect(supervisor_feedback_model)
    def post(self, project_id):
        """supervisor posts a feedback for a project"""

        data = request.json

        supervisor = Supervisor.query.get(data["supervisor_id"])
        if not supervisor:
            abort(400, "Supervisor id {} not found".format(data["supervisor_id"]))

        project = Project.query.get(data["project_id"])
        if not project:
            abort(400, "Project id {} not found".format(data["project_id"]))

        # the project.supervisor_id must be this supervisor
        if project.supervisor_id != supervisor.supervisor_id:
            abort(400, "Supervisor id {} does not belong to project id {}".format(supervisor.supervisor_id, project.project_id))

        # check if the feedback already exist
        check_feedback = ProjectSupervisorFeedback.query.filter_by(project_id=project_id).first()
        if check_feedback:
            abort(400, "Feedback for project id {} already exist".format(project_id))

        # create a new feedback
        new_feedback = ProjectSupervisorFeedback(
            project_id=project.project_id,
            supervisor_id=supervisor.supervisor_id,
            feedback=data["feedback"],
            supervisor_last_updated_at=datetime.now()
        )

        db.session.add(new_feedback)
        db.session.commit()
        return jsonify(new_feedback.as_dict())


    @api.doc(description="Get the supervisor feedback for a given project")
    @api.response(200, "Success, return the feedback dict")
    @api.response(400, "Invalid parameter / Project not found / Supervisor does not belong to the project, etc")
    def get(self, project_id):
        """get the supervisor feedback for a given project"""

        project = Project.query.get(project_id)
        if not project:
            abort(400, "Project id {} not found".format(project_id))

        feedback = ProjectSupervisorFeedback.query.filter_by(project_id=project_id) \
            .order_by(desc(ProjectSupervisorFeedback.project_supervisor_feedback_id)).first()

        if not feedback:
            abort(400, "Feedback for project id {} not found".format(project_id))

        return jsonify(feedback.as_dict())


    @api.doc(description="update the supervisor feedback for a given project")
    @api.response(200, "Success, return the feedback dict")
    @api.response(400, "Invalid parameter / Project not found / Supervisor does not belong to the project, etc")
    @api.expect(supervisor_feedback_model)
    def put(self, project_id):
        """the new supervisor's feedback replaces the old one"""

        data = request.json

        supervisor = Supervisor.query.get(data["supervisor_id"])
        if not supervisor:
            abort(400, "Supervisor id {} not found".format(data["supervisor_id"]))

        project = Project.query.get(data["project_id"])
        if not project:
            abort(400, "Project id {} not found".format(data["project_id"]))

        # the project.supervisor_id must be this supervisor
        if project.supervisor_id != supervisor.supervisor_id:
            abort(400, "Supervisor id {} does not belong to project id {}".format(supervisor.supervisor_id, project.project_id))

        # get the original feedback
        feedback = ProjectSupervisorFeedback.query.filter_by(project_id=project_id) \
            .order_by(desc(ProjectSupervisorFeedback.project_supervisor_feedback_id)).first()

        if not feedback:
            abort(400, "Feedback for project id {} not found".format(project_id))

        # update
        feedback.feedback = data["feedback"]
        feedback.supervisor_last_updated_at = datetime.now()
        db.session.commit()
        return jsonify(feedback.as_dict())
