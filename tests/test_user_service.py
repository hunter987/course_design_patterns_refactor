import pytest

from utils.user_service import UserService
from utils.user_repository import InMemoryUserRepository
from utils.user_validators import BasicUserValidator


def setup_service() -> UserService:
    repo = InMemoryUserRepository()
    validator = BasicUserValidator()
    return UserService(repo, validator)


def test_create_user_success():
    service = setup_service()

    user = service.create_user({
        "username": "john",
        "email": "john@mail.com"
    })

    assert user.id == 1
    assert user.username == "john"
    assert user.email == "john@mail.com"
    assert user.is_active is True


def test_create_user_invalid_email_raises_value_error():
    service = setup_service()

    with pytest.raises(ValueError):
        service.create_user({
            "username": "john",
            "email": "invalid"
        })


def test_deactivate_user_sets_is_active_false():
    service = setup_service()

    user = service.create_user({
        "username": "john",
        "email": "john@mail.com"
    })

    service.deactivate_user(user.id)
    updated = service.get_user(user.id)

    assert updated is not None
    assert updated.is_active is False


def test_update_nonexistent_user_returns_none():
    service = setup_service()

    result = service.update_user(999, {"username": "x"})

    assert result is None
