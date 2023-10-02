from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


# create the api
api = Api(
    version='1.0',
    title='Student Industry Project Management System',
    description='A simple API for the Student Industry Project Management System',
    validate=True
)

# no database for now

# create the app
app = Flask(__name__)
app.url_map.strict_slashes = False

# wrap with CORS
CORS(app)

# initialize
api.init_app(app)

# import the routes
from apis import auth, profile

api.add_namespace(auth.api)
api.add_namespace(profile.api)

