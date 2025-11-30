# utils/auth_service.py

class AuthService:
    _TOKEN = "abcd1234"  # Token único y consistente para toda la app

    @classmethod
    def generate_token(cls, username: str, password: str):
        """
        Valida credenciales y devuelve un token si son correctas.
        """
        if username == "student" and password == "desingp":
            return cls._TOKEN
        return None

    @classmethod
    def is_valid_token(cls, token: str) -> bool:
        """
        Valida si el token enviado por el cliente es correcto.
        """
        return token == cls._TOKEN
    
