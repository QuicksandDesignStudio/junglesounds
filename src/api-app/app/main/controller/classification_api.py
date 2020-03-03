from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_restful import fields, marshal_with

from app.main.start import db
from app.main.model import category, user, sample, classification

from app.main.helpers.utils import abort_if_doesnt_exist,  not_supported

parser = reqparse.RequestParser()
parser.add_argument('sample_id')
parser.add_argument('category_id')
parser.add_argument('start_time')
parser.add_argument('end_time')
parser.add_argument('user_id')


user_fields = {
    'id':fields.Integer,
    'username': fields.String
}

category_fields = {
    'id':fields.Integer,
    'category': fields.String,
    'slug':fields.String
}

sample_fields = {
    'id':   fields.Integer,
    'sample_file_name':   fields.String,
    'no_of_reviews':fields.Integer
}

classification_fields = {
    'id':  fields.Integer,
    'user':fields.Nested(user_fields),
    'sample':fields.Nested(sample_fields),
    'category':fields.Nested(category_fields),
    'start_time':fields.Float,
    'end_time':fields.Float,
}


classification_list_fields = {
   'classifications':fields.List(fields.Nested(classification_fields)),
}

class Classification(Resource):
    @marshal_with(classification_fields)
    def get(self, classification_id):        
        s = classification.Classification.query.filter_by(id=classification_id).first()
        if s:
            return s
        else:
            abort_if_sample_doesnt_exist(classification_id)

    def delete(self, classification_id):
        not_supported()

    def put(self, classification_id):
        not_supported()


class ClassificationList(Resource):
    @marshal_with(classification_list_fields)
    def get(self):
        #TODO: We will improve this later
        return {"classifications": classification.Classification.query.filter().limit(10)}

    @marshal_with(classification_fields)
    def post(self):
        args = parser.parse_args()
        sample_id = args['sample_id']
        category_id = args['category_id']
        start_time = args['start_time']
        end_time = args['end_time']
        user_id = args['user_id']
        #TODO: We will also read the file from request and save it
        s = classification.Classification()
        s.sample_id = sample_id
        s.category_id = category_id
        s.start_time = start_time
        s.end_time = end_time
        s.user_id = user_id

        #TODO: Update the review count in sample
        no_of_reviews = 0

        db.session.add(s)
        db.session.commit()
        return s


