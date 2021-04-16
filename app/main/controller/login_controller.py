from flask import request
from flask_restx import Resource, Namespace, fields

from app.main.service.auth_service import Auth


api = Namespace('auth', description='authentication related operations')


@api.route('/')
class UserLogin(Resource):
    """
        User Login Resource
    """

    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)