# endpoints/base_resource.py

from flask_restful import Resource
from flask import request

from utils.auth_service import AuthService


class AuthenticatedResource(Resource):
    """
    Recurso base que centraliza la validación del token de autenticación.
    Otros recursos que requieran autenticación deben heredar de esta clase.
    """

    def _require_valid_token(self):
        """
        Valida el token enviado en el header 'Authorization'.
        Retorna:
          - None si el token es válido.
          - (dict, int) -> (mensaje, status_code) si es inválido.
        """
        token = request.headers.get("Authorization")

        if not token:
            return {'message': 'Unauthorized: token not found'}, 401

        if not AuthService.is_valid_token(token):
            return {'message': 'Unauthorized: invalid token'}, 401

        return None
