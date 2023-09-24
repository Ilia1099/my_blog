import pydantic
from pydantic import ValidationError, SecretStr
from app.serializers.users_serializer import UserInfo
import pytest


def test_user_valid():
    received_data = {
        "user_login": "test",
        "password": "qweRt!234",
        "email": "email@email.com"
    }
    test_uinfo = UserInfo(**received_data)
    for k in test_uinfo.model_dump():
        print(f"Key {k}; Value {test_uinfo.model_dump().get(k)}")
        print(k == "password")


def test_user_not_valid():
    with pytest.raises(ValidationError):
        received_data = {"user_login": 1234, "password": "qweRt!234"}
        print(UserInfo(**received_data))
