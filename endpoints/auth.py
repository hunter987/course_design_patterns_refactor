from flask import Blueprint, request
from flask_restful import Resource, Api
from utils.auth_service import AuthService

class AuthenticationResource(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        token = AuthService.generate_token(username, password)
        if not token:
            return {'message': 'unauthorized'}, 401

        return {'token': token}, 200



