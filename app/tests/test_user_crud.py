import pytest

from app.tests.test_db import test_app

fixtures = [
    {
        "json": {
            "user_login": "ilya",
            "password": "qw@rty1234",
            "user_email": "email@email.com"
        },
        "assertion": {
            "status_code": 201
        }
    },
    {
        "json": {
            "user_login": "ilya2",
            "password": "qw@rty12345",
            "user_email": "email2@email.com"
        },
        "assertion": {
            "status_code": 201
        }
    },
    {
        "json": {
            "user_login": "ilya3",
            "password": "qw@rty123456",
            "user_email": "email3@email.com"
        },
        "assertion": {
            "status_code": 201
        }
    }
]


@pytest.fixture  # necessary for pytest, to make possible testing async
# endpoints
def anyio_backend():
    return 'asyncio'


def test_register_ok():
    with test_app as ac:
        for ts_cs in fixtures:
            response = ac.post(
                url="/users",
                json={
                    "user_login": ts_cs["json"]["user_login"],
                    "password": ts_cs["json"]["password"],
                    "email": ts_cs["json"]["user_email"]
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


def test_user_delete_ok():
    tkn = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjZTk1YTBiMi04MGNjLTQ1YzctYTU0NS03OGRiODM2MWFhNGMiLCJleHAiOjE2OTUwMzgxODh9.4Gl-A7r4p5ogqk4kfD4kg2wq76j28oZZpH42iIovzVI"
    response = test_app.delete(
        url="/users/ilya",
        headers={"Authorization": f"Bearer {tkn}"}
    )
    assert response.status_code == 200


def test_user_update_ok():
    tkn = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjZTk1YTBiMi04MGNjLTQ1YzctYTU0NS03OGRiODM2MWFhNGMiLCJleHAiOjE2OTUwMzgxODh9.4Gl-A7r4p5ogqk4kfD4kg2wq76j28oZZpH42iIovzVI"
    response = test_app.put(
        url="/users/ilya3",
        headers={"Authorization": f"Bearer {tkn}"},
        json={
            "user_login": "ilya3",
            "password": "qw@rty123456",
            "email": "new_email@gmail.com"
        }
    )
