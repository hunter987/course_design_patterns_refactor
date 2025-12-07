from utils.user_service import UserService
from utils.user_repository import InMemoryUserRepository
from utils.user_validators import BasicUserValidator


def setup_service():
    repo = InMemoryUserRepository()
    validator = BasicUserValidator()
    return UserService(repo, validator)


def test_create_user():
    service = setup_service()
    user = service.create_user({"username": "john", "email": "john@mail.com"})
    
    assert user.id == 1
    assert user.username == "john"
    assert user.email == "john@mail.com"
    assert user.is_active is True


def test_invalid_email():
    service = setup_service()
    try:
        service.create_user({"username": "john", "email": "invalid"})
        assert False, "Should have raised ValueError"
    except ValueError:
        assert True


def test_deactivate_user():
    service = setup_service()
    user = service.create_user({"username": "john", "email": "john@mail.com"})
    
    service.deactivate_user(user.id)
    updated = service.get_user(user.id)

    assert updated.is_active is False
