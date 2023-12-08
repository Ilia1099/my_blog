import pytest

from app.tests.test_db import test_app

posts = [
    {

    }
]


@pytest.fixture  # necessary for pytest, to make possible testing async
# endpoints
def anyio_backend():
    return 'asyncio'


def test_add_post_ok():
    with test_app as ap:
        tkn = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmOGI3ZTdkZS0xYTE1LTQ2OGMtYmI5ZS1jZjBjNGIyNDMxZGUiLCJleHAiOjE2OTgyMzE4NDF9.av1_omtUJI-6KxqTXq4MbFlQbQCCUzxBgv-1F4Fh67c"
        response = ap.post(
                url="/add_post",
                json={
                    "post_header": "test_header3",
                    "post_text": "test_text",
                    "user_id": "f8b7e7de-1a15-468c-bb9e-cf0c4b2431de"
                },
                headers={"Authorization": f"Bearer {tkn}"}
            )
        assert response.status_code == 201


def test_add_post_exists():
    with test_app as ap:
        tkn = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMzQwZTZlZS1kNWQwLTQ4M2EtOTE3My1kYTQ4ZjM3NTNhNTYiLCJleHAiOjE3MDAzOTI4ODh9.inOLsqd_iS-ZCjPxbwCb4NT024xI_OI5f1wI-cyWH0U"
        response = ap.post(
                url="/add_post",
                json={
                    "post_header": "test_header3",
                    "post_text": "test_text",
                    "user_id": "f8b7e7de-1a15-468c-bb9e-cf0c4b2431de"
                },
                headers={"Authorization": f"Bearer {tkn}"}
            )
        assert response.status_code == 409


def test_add_multiple_posts():
    tkn = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMzQwZTZlZS1kNWQwLTQ4M2EtOTE3My1kYTQ4ZjM3NTNhNTYiLCJleHAiOjE3MDAzOTI4ODh9.inOLsqd_iS-ZCjPxbwCb4NT024xI_OI5f1wI-cyWH0U"
    with test_app as ap:
        for num in range(10, 15):
            response = ap.post(
                url="/add_post",
                json={
                    "post_header": f"test_header{num}",
                    "post_text": "test_text",
                    "user_id": "0340e6ee-d5d0-483a-9173-da48f3753a56"
                },
                headers={"Authorization": f"Bearer {tkn}"}
            )
