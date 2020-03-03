from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
api = None
app = None


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config_by_name[config_name])
	db.init_app(app)
	flask_bcrypt.init_app(app)
	api = Api(app)	
	
	from .controller import sample_api
	from .controller import category_api
	from .controller import classification_api

	api.add_resource(sample_api.Sample, '/sample/<string:sample_id>')
	api.add_resource(sample_api.SampleList, '/samples')
	api.add_resource(category_api.Category, '/category/<string:category_id>')
	api.add_resource(category_api.CategoryList, '/categories')
	api.add_resource(classification_api.Classification, '/classification/<string:classification_id>')
	api.add_resource(classification_api.ClassificationList, '/classifications')

	return app
