from flask import Flask
from flask import current_app as app

from flask_restful import reqparse, abort, Api, Resource
from flask_restful import fields, marshal_with

from app.main.start import db
from app.main.model import category, user, sample, classification
from app.main.helpers.utils import abort_if_doesnt_exist,  not_supported, getHashOfFile, resource_exists, deleteFile
from app.main.helpers.constants import pagination_fields
from app.main.helpers.constants import default_per_page, default_page

import werkzeug
import os
import uuid
from datetime import datetime


parser = reqparse.RequestParser()
parser.add_argument(
    'sample_audio', type=werkzeug.datastructures.FileStorage, location='files')
parser.add_argument('no_of_reviews')
parser.add_argument('page')
parser.add_argument('per_page')
parser.add_argument(
    'recorded_time', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
parser.add_argument('recorded_location')


user_fields = {
    'id': fields.Integer,
    'username': fields.String
}

category_fields = {
    'id': fields.Integer,
    'category': fields.String,
    'slug': fields.String
}


classification_fields = {
    'id':  fields.Integer,
    'user': fields.Nested(user_fields),
    'category': fields.Nested(category_fields),
    'start_time': fields.Float,
    'end_time': fields.Float
}

sample_fields = {
    'id':   fields.Integer,
    'sample_file_name':   fields.String,
    'classifications': fields.List(fields.Nested(classification_fields)),
    'file_hash': fields.String,
    'no_of_reviews': fields.Integer,
    'recorded_time': fields.DateTime,
    'recorded_location': fields.String
}

sample_list_fields = {
    'samples': fields.List(fields.Nested(sample_fields)),
    'pagination': fields.Nested(pagination_fields)
}


class Sample(Resource):
    @marshal_with(sample_fields)
    def get(self, sample_id):
        return sample.Sample.query.filter_by(id=sample_id).first_or_404()

    def delete(self, sample_id):
        not_supported()

    def put(self, sample_id):
        not_supported()


class SampleList(Resource):
    @marshal_with(sample_list_fields)
    def get(self):
        args = parser.parse_args()
        no_of_reviews = 0
        per_page = default_per_page
        page = default_page
        pagination = None
        if 'per_page' in args and args['per_page']:
            per_page = int(args['per_page'])

        if 'page' in args and args['page']:
            page = int(args['page'])

        if 'no_of_reviews' in args and args['no_of_reviews']:
            no_of_reviews = int(args['no_of_reviews'])
            pagination = sample.Sample.query.filter_by(
                no_of_reviews=no_of_reviews).paginate(page, per_page)

        else:
            pagination = sample.Sample.query.filter().paginate(page, per_page)

        return {"samples": pagination.items, "pagination": {"has_next": pagination.has_next, "has_prev": pagination.has_prev, "page": pagination.page, "per_page": pagination.per_page, "pages": pagination.pages, "total": pagination.total}}

    @marshal_with(sample_fields)
    def post(self):
        args = parser.parse_args()
        sample_audio = args['sample_audio']
        recorded_location = args['recorded_location']
        recorded_time = args['recorded_time']

        # create a unique name and save the file
        file_name = str(uuid.uuid4())+".wav"
        saved_path = os.path.join(
            app.config['SAMPLE_AUDIO_UPLOAD_FOLDER'], file_name)
        sample_audio.save(saved_path)

        # get the hash of the file and error out if it already exists
        file_hash = getHashOfFile(saved_path)
        s = sample.Sample.query.filter_by(file_hash=file_hash).first()
        if s:
            deleteFile(saved_path)
            resource_exists()

        # TODO:move to S3 in production

        # add to db
        no_of_reviews = 0
        s = sample.Sample()
        s.sample_file_name = file_name
        s.no_of_reviews = no_of_reviews
        s.file_hash = file_hash
        s.recorded_time = recorded_time
        s.recorded_location = recorded_location
        db.session.add(s)
        db.session.commit()
        return s
