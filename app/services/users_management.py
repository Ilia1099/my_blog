from fastapi import HTTPException
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.serializers.users_serializer import UserInfo, UserRegData
from sqlalchemy.orm import aliased, joinedload
from app.models import Users
from app.services.pswd_hasher import hash_password


async def user_registration(
        credentials: UserRegData, db_ses: AsyncSession) -> Users:
    """
    coroutine for adding new user instance into db
    :param credentials: Pydantic class with validated registration info
    :param db_ses: yielded db session
    :return: user instance for following usage in case of need
    """
    try:
        user = Users(
            user_login=credentials.user_login,
            password=hash_password(credentials.password.get_secret_value()),
            email=credentials.email
        )
        db_ses.add(user)
        return user
    except ValueError:
        print("error occured during saving new db instance, "
              "check serializer or model")


async def get_user(
        db_ses: AsyncSession, user_login: str = None, user_uuid: str = None
) -> Users | None:
    """
    coroutine for querying user in db; for searching uses either login or
    uuid, since this coroutine could be used in different situations
    :param db_ses: yielded db session
    :param user_login: user's login, optional
    :param user_uuid: user's uuid, optional
    :return: user's instance or None
    """
    qs = aliased(Users, name="usr")
    query = (
        select(qs).
        options(joinedload(qs.posts)))
    filter_by = []
    if user_login is not None:
        filter_by.append(qs.user_login == user_login)
    else:
        filter_by.append(qs.user_uuid == user_uuid)
    query.filter(or_(*filter_by))
    
    query = (
        select(qs).
        options(joinedload(qs.posts))
        .filter(
            or_(
                        qs.user_login == user_login,
                        qs.user_uuid == user_uuid
                    )
         )
    )
    # (
    #                 qs.user_login == user_login,
    #                 qs.user_uuid == user_uuid
    #             )
    result = await db_ses.scalar(query)
    return result


async def usr_deletion(login: str, db_ses: AsyncSession):
    """
    a coroutine which deletes user instance from db; checks if specified
    login exists, after that proceeds deletion
    :param login: user's login specified for deletion
    :param db_ses: db session instance
    :return: True if successful, False if user not found
    """
    check_exists = await get_user(db_ses, login)
    if not check_exists:
        return False
    await db_ses.delete(check_exists)
    return True


async def usr_update(
        user_login: str, db_ses: AsyncSession, new_data: UserInfo) \
        -> Users | None:
    check_exists = await get_user(db_ses, user_login=user_login)
    if not check_exists:
        return
    for field in new_data.model_dump():
        new_value = new_data.model_dump().get(field)
        if not new_value:
            continue
        match field:
            case "password":
                new_value = hash_password(new_data.password.get_secret_value())
            case "user_uuid":
                continue
        setattr(check_exists, field, new_value)
    return check_exists
