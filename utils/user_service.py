from typing import Dict, List, Optional

from utils.user_models import User
from utils.user_repository import UserRepository
from utils.user_validators import UserValidatorStrategy


class UserService:
    """
    Capa de servicio (Service Layer) que orquesta reglas de negocio
    para el módulo de gestión de usuarios.
    """

    def __init__(self, repository: UserRepository, validator: UserValidatorStrategy):
        self.repository = repository
        self.validator = validator

    def create_user(self, data: Dict) -> User:
        self.validator.validate(data)
        user = User(
            id_=0,
            username=data["username"],
            email=data["email"],
            is_active=True,
        )
        return self.repository.save(user)

    def update_user(self, user_id: int, data: Dict) -> Optional[User]:
        existing = self.repository.find_by_id(user_id)
        if not existing:
            return None

        # Puedes decidir si revalidar todo o solo algunos campos
        merged = {
            "username": data.get("username", existing.username),
            "email": data.get("email", existing.email),
        }
        self.validator.validate(merged)

        existing.username = merged["username"]
        existing.email = merged["email"]

        return self.repository.update(existing)

    def deactivate_user(self, user_id: int) -> Optional[User]:
        return self.repository.deactivate(user_id)

    def list_users(self, only_active: bool = False) -> List[User]:
        filters = {}
        if only_active:
            filters["is_active"] = True
        return self.repository.find_all(filters)

    def get_user(self, user_id: int) -> Optional[User]:
        return self.repository.find_by_id(user_id)
