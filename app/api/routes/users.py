from typing import Annotated

import starlette.status
from fastapi import APIRouter, Depends, HTTPException,Request
from jose import JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.databases.connection import get_session
from app.serializers.users_serializer import UserInfo
from app.services.users_management import (user_registration, user_exists,
                                           get_user)
from app.services.user_verification import (authenticate_user, authorize_user,
                                            credentials_exception,
                                            grant_jwt,
                                            data_exception)

router = APIRouter()


class ServiceError(Exception):
    pass


@router.post("/users")
async def register_new_user(
        user_data: UserInfo,
        db_ses: Annotated[AsyncSession, Depends(get_session)]
):
    try:
        result = await user_registration(
            credentials=user_data, db_ses=db_ses)
        await db_ses.commit()
        return grant_jwt(result)
    except IntegrityError:
        raise user_exists
    except ValueError:
        raise data_exception


@router.get("/users/login")
async def user_login(
        credentials: UserInfo,
        db_ses: Annotated[AsyncSession, Depends(get_session)]
):
    try:
        user = await authenticate_user(
            login=credentials.user_login, db_ses=db_ses,
            password=credentials.password.get_secret_value(),
        )
        return grant_jwt(user, new_user=False)
    except (JWTError, ExpiredSignatureError, JWTClaimsError):
        raise credentials_exception


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    ...


@router.put("/users/{user_id")
async def update_user(user_id: int):
    ...
