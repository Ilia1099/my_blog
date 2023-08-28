import pytest

from app.tests.test_db import test_app

fixtures = [
    {
        "json": {
            "user_login": "ilya",
            "password": "qw@rty1234"
        },
        "assertion": {
            "status_code": 201
        }
    },
    {
        "json": {
            "user_login": "ilya2",
            "password": "qw@rty12345"
        },
        "assertion": {
            "status_code": 201
        }
    },
    {
        "json": {
            "user_login": "ilya3",
            "password": "qw@rty123456"
        },
        "assertion": {
            "status_code": 201
        }
    }
]


@pytest.fixture
def anyio_backend():
    return 'asyncio'


def test_register_ok():
    with test_app as ac:
        for ts_cs in fixtures:
            response = ac.post(
                url="/users",
                json={
                    "user_login": ts_cs["json"]["user_login"],
                    "password": ts_cs["json"]["password"]
                }
            )
            assert response.status_code == ts_cs["assertion"]["status_code"]


def test_register_fail():
    response = test_app.post(
        url="/users",
        json={
            "user_login": "ilya3",
            "password": "qw@rty123456"
        }
    )
    assert response.status_code == 409