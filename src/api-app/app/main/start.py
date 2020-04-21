from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from .config import config_by_name


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
api = None
app = None


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)

    # all the API end points setup
    from .controller import sample_api
    from .controller import category_api
    from .controller import classification_api
    from .controller import users_api
    from .controller import download
    api.add_resource(sample_api.Sample, '/api/sample/<string:sample_id>')
    api.add_resource(sample_api.SampleList, '/api/samples')
    api.add_resource(download.SampleDownload,
                     '/api/download/<string:file_name>')
    api.add_resource(category_api.Category,
                     '/api/category/<string:category_id>')
    api.add_resource(category_api.CategoryList, '/api/categories')
    api.add_resource(classification_api.Classification,
                     '/api/classification/<string:classification_id>')
    api.add_resource(classification_api.ClassificationList,
                     '/api/classifications')


    api.add_resource(users_api.UserLogin, '/api/user/login')
    api.add_resource(users_api.UserSignup, '/api/user/create')
    api.add_resource(users_api.UserRefresh, '/api/token/refresh')


    # this is where the regular web gets started
    app.app_context().push()
    from app.main.controller import application

    return app
