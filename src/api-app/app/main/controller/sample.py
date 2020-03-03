from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

SAMPLES = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_sample_doesnt_exist(sample_id):
    if sample_id not in SAMPLES:
        abort(404, message="Todo {} doesn't exist".format(sample_id))


def not_supported():
        abort(501, message="Not implemented yet")


parser = reqparse.RequestParser()
parser.add_argument('task')


class Sample(Resource):
    def get(self, sample_id):
        abort_if_sample_doesnt_exist(sample_id)
        return SAMPLES[sample_id]

    def delete(self, sample_id):
        not_supported()

    def put(self, sample_id):
        not_supported()


class SampleList(Resource):
    def get(self):
        return SAMPLES

    def post(self):
        args = parser.parse_args()
        sample_id = int(max(SAMPLES.keys()).lstrip('todo')) + 1
        sample_id = 'todo%i' % sample_id
        SAMPLES[sample_id] = {'task': args['task']}
        return SAMPLES[sample_id], 201