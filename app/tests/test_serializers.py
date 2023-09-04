from pydantic import ValidationError
from app.serializers.users_serializer import UserInfo
import pytest


def test_user_valid():
    received_data = {
        "user_login": "test",
        "password": "qweRt!234",
        "email": "email@email.com"
    }
    test_uinfo = UserInfo(**received_data)
    print(test_uinfo)


def test_user_not_valid():
    with pytest.raises(ValidationError):
        received_data = {"user_login": 1234, "password": "qweRt!234"}
        print(UserInfo(**received_data))
