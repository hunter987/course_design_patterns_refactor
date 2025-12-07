from flask_restful import reqparse
from flask import request

from endpoints.base_resource import AuthenticatedResource
from utils.user_service import UserService
from utils.user_repository import InMemoryUserRepository
from utils.user_validators import BasicUserValidator


class UsersResource(AuthenticatedResource):
    """
    Recurso RESTful para gestionar usuarios.
    Hereda de AuthenticatedResource para usar la validación de token.
    """

    def __init__(self):
        # Inicializamos repositorio, validador y servicio
        self.repository = InMemoryUserRepository()
        self.validator = BasicUserValidator()
        self.service = UserService(self.repository, self.validator)

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username", type=str, required=False)
        self.parser.add_argument("email", type=str, required=False)
        self.parser.add_argument("only_active", type=bool, required=False)

    def get(self, user_id=None):
        # 1. Validar token con la clase base
        error = self._require_valid_token()
        if error:
            return error

        if user_id is not None:
            user = self.service.get_user(user_id)
            if not user:
                return {"message": "User not found"}, 404
            return user.to_dict(), 200

        args = self.parser.parse_args()
        only_active = args.get("only_active") or False
        users = self.service.list_users(only_active=only_active)
        return [u.to_dict() for u in users], 200

    def post(self):
        error = self._require_valid_token()
        if error:
            return error

        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True, help="Username is required")
        parser.add_argument("email", type=str, required=True, help="Email is required")
        args = parser.parse_args()

        try:
            user = self.service.create_user(
                {"username": args["username"], "email": args["email"]}
            )
        except ValueError as e:
            return {"message": str(e)}, 400

        return {"message": "User created", "user": user.to_dict()}, 201

    def put(self, user_id):
        error = self._require_valid_token()
        if error:
            ret
