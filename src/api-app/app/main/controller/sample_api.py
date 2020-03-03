from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_restful import fields, marshal_with

from app.main.start import db
from app.main.model import category, user, sample, classification

def abort_if_sample_doesnt_exist(sample_id):
    if sample_id not in SAMPLES:
        abort(404, message="Todo {} doesn't exist".format(sample_id))


def not_supported():
        abort(501, message="Not implemented yet")


parser = reqparse.RequestParser()
parser.add_argument('sample_file_name')


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
            abort_if_sample_doesnt_exist(sample_id)

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
        sample_file_name = args['sample_file_name']
        #TODO: We will also read the file from request and save it
        no_of_reviews = 0
        s = sample.Sample()
        s.sample_file_name = sample_file_name
        s.no_of_reviews = no_of_reviews
        db.session.add(s)
        db.session.commit()
        return s



