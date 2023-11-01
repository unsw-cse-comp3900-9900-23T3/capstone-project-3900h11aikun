from flask_restx import fields, reqparse
from config import api
from werkzeug.datastructures import FileStorage

# supervisor upload resume
supervisor_resume_parser = reqparse.RequestParser()
supervisor_resume_parser.add_argument(
    'file', type=FileStorage, location='files', required=True, help='resume file in pdf, doc, docx')
