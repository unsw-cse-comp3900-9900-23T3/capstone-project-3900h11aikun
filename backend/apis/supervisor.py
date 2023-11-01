from flask import request, abort, jsonify
from flask_restx import Resource, Namespace
from db.models import *
from models.supervisor import *
from db.models import *
from datetime import datetime
from config import app
import os
import time
from .util import *


api = Namespace(
    "supervisorInfo",
    description="supervisor resume here"
)


supervisor_resume_note = """
Supervisor can upload resume here.
The resume file is wrapped in the FormData.
File can only be .pdf, .docx. .doc only.
File size cannot be larger than 20MB.

On the frontend, create an input.
And when input change, get the file and wrap into a FormData !!!
"""

@api.route("/supervisor_upload_resume/<int:supervisor_id>")
class StudentRegisterWithResumeFile(Resource):
    @api.doc(description=supervisor_resume_note)
    @api.response(200, 'success upload, will return that resume url on the server database')
    @api.response(400, 'invalid inputs, please see the detail error message')
    @api.expect(supervisor_resume_parser)
    def post(self, supervisor_id):
        # check if the supervisor exist
        supervisor = Supervisor.query.get(supervisor_id)
        if supervisor is None:
            abort(400, 'unknown supervisor id {}'.format(supervisor))

        # check this file exist
        if 'file' not in request.files:
            abort(400, 'require to submit a file')

        file = request.files['file']

        # require to match from the end of the file.filename: pdf, docx, doc
        if not file.filename.lower().endswith(('.pdf', '.docx', '.doc')):
            abort(400, 'require to submit a pdf, docx or doc file')

        # file cannot be too large, larger than 20MB will be rejected
        if len(file.read()) > 20 * 1024 * 1024:
            abort(400, 'file size cannot be larger than 20MB')

        # reset the file pointer to beginning
        file.seek(0)

        # no need to hash, simply add a timestamp at the beginning
        # and replace \\ to /
        new_filename = "{}-{}".format(int(time.time()), file.filename)
        new_full_filename = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        new_full_filename = new_full_filename.replace("\\", "/")

        # save the file
        file.save(new_full_filename)

        # update the resume_url
        supervisor.resume_url = new_full_filename
        db.session.commit()

        # return the resume_url for that student id
        base_url = request.url_root
        response = {
            "resume_url": base_url + new_full_filename,
            "supervisor_id": supervisor_id
        }

        return jsonify(response)

