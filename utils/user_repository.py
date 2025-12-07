from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from utils.user_models import User


class UserRepository(ABC):
    """
    Patrón Repository para abstraer el acceso a datos de usuarios.
    """

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def deactivate(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def find_all(self, filters: Optional[Dict] = None) -> List[User]:
        pass


class InMemoryUserRepository(UserRepository):
    """
    Implementación simple en memoria.
    Es suficiente para la actividad y para hacer pruebas unitarias.
    """

    def __init__(self):
        self._users: List[User] = []
        self._next_id = 1

    def save(self, user: User) -> User:
        user.id = self._next_id
        self._next_id += 1
        self._users.append(user)
        return user

    def update(self, user: User) -> User:
        for idx, existing in enumerate(self._users):
            if existing.id == user.id:
                self._users[idx] = user
                return user
        # si no existe, por simplicidad lo agregamos
        return self.save(user)

    def deactivate(self, user_id: int) -> Optional[User]:
        user = self.find_by_id(user_id)
        if user:
            user.is_active = False
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        return next((u for u in self._users if u.id == user_id), None)

    def find_all(self, filters: Optional[Dict] = None) -> List[User]:
        users = self._users

        if filters:
            # de momento solo filtramos por is_active si viene
            if "is_active" in filters:
                users = [u for u in users if u.is_active == filters["is_active"]]

        return users
