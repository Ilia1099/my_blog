from pydantic import ValidationError
from app.serializers.users_serializer import UserInfo
import pytest


def test_user_valid():
    received_data = {"user_login": "test", "user_password": "qweRt!234"}
    print(UserInfo.from_dict(received_data))


def test_user_not_valid():
    with pytest.raises(ValidationError):
        received_data = {"user_login": 1234, "user_password": "qweRt!234"}
        print(UserInfo.from_dict(received_data))
