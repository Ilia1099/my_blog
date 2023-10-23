import pydantic
from pydantic import ValidationError, SecretStr
from app.serializers.users_serializer import UserInfo
from app.serializers.posts_serializer import PostData
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


def test_postdata_not_valid():
    with pytest.raises(ValueError):
        received_data = {
            "post_header": "test",
            "post_text": "test",
            "user_id": ""
        }
        print(PostData(**received_data))


def test_postdata_valid():
    received_data = {
        "post_header": "test",
        "post_text": "test",
        "user_id": "f8b7e7de-1a15-468c-bb9e-cf0c4b2431de"
    }
    print(PostData(**received_data))
