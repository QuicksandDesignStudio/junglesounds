from flask import Flask
from flask import current_app as app
from flask import send_from_directory

from flask_restful import reqparse, abort, Api, Resource
from flask_restful import fields, marshal_with
from flask_jwt_extended import jwt_required

class SampleDownload(Resource):
	def get(self, file_name):
		folder = app.config['SAMPLE_AUDIO_UPLOAD_FOLDER']
		return send_from_directory(folder, file_name)