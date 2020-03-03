# from flask import Flask
# from flask_restful import reqparse, abort, Api, Resource
# from flask_restful import fields, marshal_with

# from app.main.start import db
# from app.main.model import category, user, sample, classification, prediction

# from app.main.helpers.utils import abort_if_doesnt_exist,  not_supported

# prediction_fields = {
#     'id': fields.String
# }
# class Pedict(Resource):
#     @marshal_with(prediction_fields)
#     def get(self, prediction_id):        
#         s = prediction.Prediction.query.filter_by(id=prediction_id).first()
#         if s:
#             return s
#         else:
#             abort_if_sample_doesnt_exist(prediction_id)

#     @marshal_with(prediction_fields)
#     def post(self):
#         args = parser.parse_args()
#         sample_file_name = args['sample_file_name']
#         #TODO: We will also read the file from request and save it
#         no_of_reviews = 0
#         s = sample.Sample()
#         s.sample_file_name = sample_file_name
#         s.no_of_reviews = no_of_reviews
#         db.session.add(s)
#         db.session.commit()
#         return s

