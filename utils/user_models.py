class User:
    """
    Modelo simple de usuario dentro del sistema.
    """
    def __init__(self, id_: int, username: str, email: str, is_active: bool = True):
        self.id = id_
        self.username = username
        self.email = email
        self.is_active = is_active

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
        }
