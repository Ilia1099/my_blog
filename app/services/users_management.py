from fastapi import Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.serializers.users_serializer import UserInfo
from sqlalchemy.orm import aliased
from app.models.users import Users
from app.services.pswd_hasher import hash_password


user_exists = HTTPException(
    status.HTTP_409_CONFLICT,
    detail="user name is not free"
        )


async def user_registration(
        credentials: UserInfo,
        db_ses: AsyncSession):
    try:
        user = Users(
            user_login=credentials.user_login,
            password=hash_password(credentials.password.get_secret_value())
        )
        db_ses.add(user)
        return user
    except ValueError:
        print("error occured during saving new db instance, "
              "check serializer or model")


async def get_user(
        db_ses: AsyncSession,
        user_login: str):
    qs = aliased(Users, name="usr")
    query = select(qs).where(qs.user_login == user_login)
    result = await db_ses.execute(query)
    return result.scalar()


