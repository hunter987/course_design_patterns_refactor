from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from utils.user_models import User


class UserRepository(ABC):
    """
    Repository: define el contrato para persistencia/consulta de usuarios.
    Permite intercambiar la implementación (memoria, JSON, DB real) sin afectar el Service Layer.
    """

    @abstractmethod
    def save(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> Optional[User]:
        """
        Actualiza un usuario existente. Retorna None si no existe.
        """
        raise NotImplementedError

    @abstractmethod
    def deactivate(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self, filters: Optional[Dict[str, Any]] = None) -> List[User]:
        raise NotImplementedError


class InMemoryUserRepository(UserRepository):
    """
    Implementación en memoria.
    Adecuada para pruebas unitarias y demostración del patrón Repository.
    """

    def __init__(self) -> None:
        self._users: List[User] = []
        self._next_id = 1

    def save(self, user: User) -> User:
        user.id = self._next_id
        self._next_id += 1
        self._users.append(user)
        return user

    def update(self, user: User) -> Optional[User]:
        for idx, existing in enumerate(self._users):
            if existing.id == user.id:
                self._users[idx] = user
                return user
        return None

    def deactivate(self, user_id: int) -> Optional[User]:
        user = self.find_by_id(user_id)
        if user is not None:
            user.is_active = False
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        return next((u for u in self._users if u.id == user_id), None)

    def find_all(self, filters: Optional[Dict[str, Any]] = None) -> List[User]:
        result = list(self._users)

        if filters:
            if "is_active" in filters:
                result = [u for u in result if u.is_active == filters["is_active"]]

        return result
