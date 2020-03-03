from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from .config import config_by_name
from .controller import sample

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
	api.add_resource(sample.Sample, '/sample/<string:sample_id>')
	api.add_resource(sample.SampleList, '/samples')
	return app
