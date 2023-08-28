from app.models.users import Users
from app.serializers.users_serializer import UserInfo


def test_users_model():
    test_data = UserInfo(
        user_login="test",
        password="qwert!234"
    )
    new_inst = Users(
        user_login=test_data.user_login,
        password=test_data.password
    )
    assert new_inst.user_login == test_data.user_login
    print("")
    print(new_inst.user_login)
    assert new_inst.password == test_data.password
    print(new_inst.password)