from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# create the api
api = Api(
    version='1.0',
    title='Student Industry Project Management System',
    description='A simple API for the Student Industry Project Management System',
    validate=True
)

# create the app
app = Flask(__name__, static_folder='db/raw_data/avatars')
app.url_map.strict_slashes = False

# connect to database: ./database.db
# check if the file ./database.db exist, if not, exit the whole program
if not os.path.exists('./database.db'):
    print('Error: database.db not found!')
    print('Copy the backend/db/default_database.db to the backend folder, and rename it to database.db')
    exit(1)

# initialize the database
# get the absolute path of the database.db
db = SQLAlchemy()
db_path = os.path.join(os.getcwd(), 'database.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# allow upload
app.config['UPLOAD_FOLDER'] = 'uploads'

# finish the setup
CORS(app)
api.init_app(app)
db.init_app(app)

# import the routes
from apis import auth, profile, student, project

api.add_namespace(auth.api)
api.add_namespace(profile.api)
api.add_namespace(student.api)
api.add_namespace(project.api)

