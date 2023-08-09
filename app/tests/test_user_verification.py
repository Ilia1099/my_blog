# import app.services.user_verification as uv
from app.services.user_verification import create_jwt_token
import pytest


# @pytest.fixture
# def mock_wrong_secret(monkeypatch, secret: str):
#     def mock_get(*args, **kwargs):
#         SECRET = secret
#         return SECRET
#
#     monkeypatch.setattr(uv.SECRET, mock_get)


# @pytest.mark.parametrize(mock_wrong_secret, "qwerty", indirect=True)
def test_create_jwt_token_ok():
    tkn = create_jwt_token("7d83aa247f9e07070e305ca8")
    print(tkn)
    assert tkn


