from app.models import Users, Posts
from app.serializers.users_serializer import UserInfo
from app.serializers.posts_serializer import PostData


def test_users_model():
    test_data = UserInfo(
        user_login="test",
        password="qwert!234",
        email="email@email.com"
    )
    new_inst = Users(
        user_login=test_data.user_login,
        password=test_data.password,
        email=test_data.email
    )
    assert new_inst.user_login == test_data.user_login
    print("")
    print(new_inst.user_login)
    assert new_inst.password == test_data.password
    print(new_inst.password)
    print(new_inst.email)


def test_post_model():
    body = {
        "post_header": "test_header",
        "post_text": "test_text",
        "user_id": "some-uuid-1187-0423"
    }

    test_data = PostData(**body)
    new_inst = Posts(
        post_header=test_data.post_header,
        post_text=test_data.post_text,
        user_id=test_data.user_id
    )
    assert new_inst.post_text == body.get("post_text")


def test_post_appending():
    test_data = UserInfo(
        user_login="test",
        password="qwert!234",
        email="email@email.com"
    )
    new_user = Users(
        user_login=test_data.user_login,
        password=test_data.password,
        email=test_data.email
    )
    body = {
        "post_header": "test_header",
        "post_text": "test_text",
        "user_id": "some-uuid-1187-0423"
    }

    test_post_data = PostData(**body)
    new_post = Posts(
        post_header=test_post_data.post_header,
        post_text=test_post_data.post_text,
        user_id=test_post_data.user_id
    )
    assert len(new_user.posts) == 0
    new_user.posts.append(new_post)
    assert len(new_user.posts) == 1
    assert new_user.posts[0].post_header == test_post_data.post_header
    assert new_user.posts[0].post_text == test_post_data.post_text
    assert new_user.posts[0].user_id == test_post_data.user_id
