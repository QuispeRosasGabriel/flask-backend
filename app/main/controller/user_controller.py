from flask import request
from flask_restx import Resource, Namespace, fields, marshal

from ..service.user_service import save_new_user, get_a_user
from ..service.auth_service import Auth

from app.main.util.decorator import token_required

api = Namespace('users', description='user related operations')
user_marshal = {
    'email': fields.String(required=True, description='user email address'),
    'username': fields.String(required=True, description='user username'),
    'firstName': fields.String(required=True, description='user first name'),
    'lastName': fields.String(required=True, description='user last name'),
    'id': fields.String(description='user Identifier')
}

@api.route('/')
class UserList(Resource):
    def get(self):
        """get a user given the JWT"""
        current_resp, status = Auth.get_logged_in_user(request)
        if status == 200:
            user = current_resp["data"]
            return marshal(user, user_marshal), 200
        else:
            return "Unauthorized", 401

    def post(self):
        """Creates a new User """
        data = request.json
        user = save_new_user(data)
        if user:
            response = Auth.login_user(data)
            return response
        else:
            return "Email or Username Already Taken", 409


@api.route('/<userId>')
@api.param('userId', 'The User identifier')
class User(Resource):

    @token_required
    def get(self, userId):
        """get a user given its identifier"""
        # current_resp, _ = Auth.get_logged_in_user(request)
        user = get_a_user(userId)
        if not user:
            return "User Not Found", 404
        # elif current_resp["data"].id != user.id: 
        #     return "Unauthorized", 401
        else:
            return marshal(user, user_marshal), 200



