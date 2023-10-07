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
app = Flask(__name__)
app.url_map.strict_slashes = False

# connect to database: ./database.db
# check if the file ./database.db exist, if not, exit the whole program
if not os.path.exists('./database.db'):
    print('Error: database.db not found!')
    print('Copy the backend/db/default_database.db to the backend folder, and rename it to database.db')
    exit(1)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# wrap with CORS
CORS(app)

# initialize
api.init_app(app)

# import the routes
from apis import auth, profile

api.add_namespace(auth.api)
api.add_namespace(profile.api)

