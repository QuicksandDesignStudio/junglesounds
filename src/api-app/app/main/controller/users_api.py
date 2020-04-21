from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_restful import fields, marshal_with
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)

from app.main.start import db
from app.main.model import user

from app.main.helpers.utils import abort_if_doesnt_exist,  not_supported



parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('role')


user_fields = {
    'username': fields.String,
    'jwt': fields.String
}



class UserLogin(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        u = user.User.query.filter_by(username=username).first()
        if u and u.approved == 1:
            print(u.check_password(password))
            if u.check_password(password):
                c = {"username":username, "role": u.role}
                access_token = create_access_token(identity=c)
                return {"username": username, "jwt": access_token}
            else:
                abort_if_doesnt_exist(username)    
        else:
            abort_if_doesnt_exist(username)


class UserRefresh(Resource):
    @marshal_with(user_fields)
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        c = {"username":current_user["username"], "jwt":access_token}
        return c

class UserSignup(Resource):
    @marshal_with(user_fields)
    @jwt_required
    def post(self):
        current_identity =  get_jwt_identity()
        current_role = get_jwt_identity()["role"]
        if current_role == "admin":
            pass
        else:
            abort_if_doesnt_exist("We need admin")                

        args = parser.parse_args()
        username = args['username']
        password = args['password']
        role = args['role']        
        if role == "admin":
            pass
        else:
            role = "user"
        u = user.User()
        u.username = username
        u.approved = 1
        u.role = role
        u.set_hash_password(password)
        db.session.add(u)
        db.session.commit()        
        c = {"username":username, "jwt":""}
        return c
