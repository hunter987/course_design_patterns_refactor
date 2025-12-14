from typing import Dict, List, Optional, Any

from utils.user_models import User
from utils.user_repository import UserRepository
from utils.user_validators import UserValidatorStrategy


class UserService:
    """
    Service Layer: encapsula y orquesta la lógica de negocio del módulo de usuarios.
    - Desacopla los endpoints (capa Resource) del acceso a datos (Repository).
    - Delegación de validación mediante Strategy (UserValidatorStrategy).
    """

    def __init__(self, repository: UserRepository, validator: UserValidatorStrategy) -> None:
        self.repository = repository
        self.validator = validator

    def create_user(self, data: Dict[str, Any]) -> User:
        """
        Crea un usuario tras validar el payload de entrada.
        """
        self.validator.validate(data)

        user = User(
            id_=0,
            username=str(data["username"]),
            email=str(data["email"]),
            is_active=True,
        )
        return self.repository.save(user)

    def update_user(self, user_id: int, data: Dict[str, Any]) -> Optional[User]:
        """
        Actualiza campos del usuario existente. Retorna None si no existe.
        La validación se aplica sobre el estado final (merged) para evitar inconsistencias.
        """
        existing = self.repository.find_by_id(user_id)
        if existing is None:
            return None

        merged = {
            "username": data.get("username", existing.username),
            "email": data.get("email", existing.email),
        }
        self.validator.validate(merged)

        existing.username = str(merged["username"])
        existing.email = str(merged["email"])

        return self.repository.update(existing)

    def deactivate_user(self, user_id: int) -> Optional[User]:
        """
        Desactiva un usuario (borrado lógico). Retorna None si no existe.
        """
        return self.repository.deactivate(user_id)

    def list_users(self, only_active: bool = False) -> List[User]:
        """
        Lista usuarios. Si only_active=True, retorna únicamente activos.
        """
        filters: Dict[str, Any] = {}
        if only_active:
            filters["is_active"] = True
        return self.repository.find_all(filters)

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por id. Retorna None si no existe.
        """
        return self.repository.find_by_id(user_id)
