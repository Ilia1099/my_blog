from fastapi import HTTPException
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.serializers.users_serializer import UserInfo
from sqlalchemy.orm import aliased
from app.models.users import Users
from app.services.pswd_hasher import hash_password
from app.services.exception_tools import get_integrity_violation_key_name


def data_caused_integrity_error(ex_arg: str) -> HTTPException:
    """
    function which generates HTTPException instance for cases when db
    IntegrityError exception is raised
    :param ex_arg: exception's detail message
    :return: instance of HTTPException
    """
    column_name = get_integrity_violation_key_name(ex_arg)
    return HTTPException(
        status.HTTP_409_CONFLICT,
        detail=f"{column_name} is not free, try another"
    )


async def user_registration(credentials: UserInfo, db_ses: AsyncSession):
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
        db_ses: AsyncSession, user_login: str = None, user_uuid: str = None):
    """
    coroutine for querying user in db; for searching uses either login or
    uuid, since this coroutine could be used in different situations
    :param db_ses: yielded db session
    :param user_login: user's login, optional
    :param user_uuid: user's uuid, optional
    :return: user's instance or None
    """
    qs = aliased(Users, name="usr")
    query = select(qs).filter(
        or_(
            qs.user_login == user_login,
            qs.user_uuid == user_uuid
        )
    )

    result = await db_ses.execute(query)
    return result.scalar()


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


