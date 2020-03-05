from flask_restful import fields, marshal_with

pagination_fields = {
    "has_next":fields.Boolean, 
    "has_prev":fields.Boolean, 
    "page":fields.Integer, 
    "per_page":fields.Integer, 
    "pages":fields.Integer, 
    "total":fields.Integer 
}

default_per_page = 20
default_page = 1