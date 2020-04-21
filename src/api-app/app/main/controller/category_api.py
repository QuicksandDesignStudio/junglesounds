from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_restful import fields, marshal_with
from flask_jwt_extended import jwt_required

from app.main.start import db
from app.main.model import category, user, sample, classification

from app.main.helpers.utils import abort_if_doesnt_exist,  not_supported


parser = reqparse.RequestParser()
parser.add_argument('category')
parser.add_argument('slug')


category_fields = {
    'id': fields.Integer,
    'category': fields.String,
    'slug': fields.String
}

category_list_fields = {
    'categories': fields.List(fields.Nested(category_fields))
}

class Category(Resource):
    @marshal_with(category_fields)
    @jwt_required
    def get(self, category_id):
        c = category.Category.query.filter_by(id=category_id).first()
        if c:
            return c
        else:
            abort_if_doesnt_exist(category_id)

    def delete(self, category_id):
        not_supported()

    def put(self, category_id):
        not_supported()


class CategoryList(Resource):
    @marshal_with(category_list_fields)
    @jwt_required
    def get(self):
        return {"categories": category.Category.query.filter()}

    @marshal_with(category_fields)
    @jwt_required
    def post(self):
        args = parser.parse_args()
        category_name = args['category']
        category_slug = args['slug']
        no_of_reviews = 0
        c = category.Category()
        c.category = category_name
        c.slug = category_slug
        db.session.add(c)
        db.session.commit()
        return c
