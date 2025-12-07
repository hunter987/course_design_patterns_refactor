from abc import ABC, abstractmethod
from typing import Dict


class UserValidatorStrategy(ABC):
    """
    Estrategia de validación de datos de usuario.
    Permite intercambiar validadores sin cambiar el servicio.
    """

    @abstractmethod
    def validate(self, data: Dict) -> None:
        """
        Lanza ValueError si los datos no son válidos.
        """
        pass


class BasicUserValidator(UserValidatorStrategy):
    """
    Implementación básica de validación de usuario.
    """

    def validate(self, data: Dict) -> None:
        username = data.get("username")
        email = data.get("email")

        if not username:
            raise ValueError("username is required")

        if not email:
            raise ValueError("email is required")

        if "@" not in email:
            raise ValueError("email is not valid")
