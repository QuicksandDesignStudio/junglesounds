from flask import Flask
from flask import current_app as app

from flask_restful import reqparse, abort, Api, Resource
from flask_restful import fields, marshal_with

from app.main.start import db
from app.main.model import category, user, sample, classification
from app.main.helpers.utils import abort_if_doesnt_exist,  not_supported, getHashOfFile, resource_exists, deleteFile

import werkzeug
import os
import uuid


parser = reqparse.RequestParser()
#parser.add_argument('sample_file_name')
parser.add_argument('sample_audio', type=werkzeug.datastructures.FileStorage, location='files')


user_fields = {
    'id':fields.Integer,
    'username': fields.String
}

category_fields = {
    'id':fields.Integer,
    'category': fields.String,
    'slug':fields.String
}


classification_fields = {
    'id':  fields.Integer,
    'user':fields.Nested(user_fields),
    'category':fields.Nested(category_fields),
    'start_time':fields.Float,
    'end_time':fields.Float
}

sample_fields = {
    'id':   fields.Integer,
    'sample_file_name':   fields.String,
    'classifications': fields.List(fields.Nested(classification_fields)),
    'file_hash': fields.String,
    'no_of_reviews':fields.Integer
}

sample_list_fields = {
   'samples':fields.List(fields.Nested(sample_fields)),
}




class Sample(Resource):
    @marshal_with(sample_fields)
    def get(self, sample_id):        
        s = sample.Sample.query.filter_by(id=sample_id).first()
        if s:
            return s
        else:
            abort_if_doesnt_exist(sample_id)

    def delete(self, sample_id):
        not_supported()

    def put(self, sample_id):
        not_supported()


class SampleList(Resource):
    @marshal_with(sample_list_fields)
    def get(self):
        #TODO: We will improve this later
        return {"samples": sample.Sample.query.filter().limit(10)}

    @marshal_with(sample_fields)
    def post(self):
        args = parser.parse_args()
        sample_audio = args['sample_audio']

        #create a unique name and save the file
        file_name = str(uuid.uuid4())+".wav"
        saved_path = os.path.join(app.config['SAMPLE_AUDIO_UPLOAD_FOLDER'], file_name)
        sample_audio.save(saved_path)

        #get the hash of the file and error out if it already exists
        file_hash = getHashOfFile(saved_path)
        s = sample.Sample.query.filter_by(file_hash=file_hash).first()
        if s:
            deleteFile(saved_path)
            resource_exists()

        #TODO:move to S3 in production

        #add to db
        no_of_reviews = 0
        s = sample.Sample()
        s.sample_file_name = file_name
        s.no_of_reviews = no_of_reviews
        s.file_hash = file_hash
        db.session.add(s)
        db.session.commit()
        return s



