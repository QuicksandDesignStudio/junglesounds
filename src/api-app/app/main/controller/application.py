from flask import Flask
from flask import current_app as app
from flask import send_from_directory
from flask import render_template

from flask_restful import reqparse, abort, Api, Resource

# class Home(Resource):
# 	def get(self):
# 		#folder = app.config['SAMPLE_AUDIO_UPLOAD_FOLDER']
# 		#return send_from_directory(folder, file_name)
# 		return f'Hello, World!'

@app.route('/')
def hello_world():
    return render_template('home.html')    

@app.route('/classifier')
def classifier():
    return render_template('classifier.html')    