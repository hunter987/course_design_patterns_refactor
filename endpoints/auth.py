from flask import request
from flask_restful import Resource
from utils.auth_service import AuthService

class AuthenticationResource(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        token = AuthService.generate_token(username, password)
        if not token:
            return {'message': 'unauthorized'}, 401

        return {'token': token}, 200



