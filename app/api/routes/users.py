from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.databases.connection import get_session
from app.serializers.users_serializer import UserInfo
from app.services.users_management import (user_registration, usr_deletion,
                                           data_caused_integrity_error)
from app.services.user_verification import (authenticate_user,
                                            credentials_exception,
                                            grant_jwt,
                                            data_exception, expired_jwt,
                                            user_not_found, authorize_user)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


class ServiceError(Exception):
    pass


@router.post("/users")
async def register_new_user(
        user_data: UserInfo,
        db_ses: Annotated[AsyncSession, Depends(get_session)]
):
    """
    endpoint for creation of new user instance; in case of existence of such
    user, raises data exception - an HTTPResponse exception
    :param user_data: body of the request which ,ust correspond to a
    Pydantic class
    :param db_ses: yielded db session
    :return: a json object which contains JWT
    """
    try:
        result = await user_registration(
            credentials=user_data, db_ses=db_ses)
        await db_ses.commit()
        return grant_jwt(result)
    except IntegrityError as e:
        raise data_caused_integrity_error(e.orig.args[0])
    except ValueError:
        raise data_exception


@router.get("/users/login")
async def user_login(
        credentials: UserInfo,
        db_ses: Annotated[AsyncSession, Depends(get_session)]
):
    """
    endpoint for logining; authenticates client and in case of success
    grants new JWT
    :param credentials: body of the request which ,ust correspond to a
    Pydantic class
    :param db_ses: yielded db session
    :return: a json object which contains JWT
    """
    try:
        user = await authenticate_user(
            login=credentials.user_login, db_ses=db_ses,
            password=credentials.password.get_secret_value(),
        )
        if not user:
            raise user_not_found
        return grant_jwt(user, new_user=False)
    except ExpiredSignatureError:
        raise expired_jwt
    except (JWTError, JWTClaimsError):
        raise credentials_exception


@router.delete("/users/{user_login}")
async def delete_user(
        user_login: str, token: Annotated[str, Depends(oauth2_scheme)],
        db_ses: Annotated[AsyncSession, Depends(get_session)]
):
    """
    endpoint for deletion of specified user, it is possible to make a
    request by third user(administrator) to delete specified user, in any
    case the requester fill follow authorization for this
    :param user_login: login of the user to be deleted from db
    :param token: token granted by requesting client
    :param db_ses: AsyncSession instance
    :return: None
    """
    try:
        await authorize_user(db_ses=db_ses, token=token)
        was_deleted = await usr_deletion(login=user_login, db_ses=db_ses)
        if not was_deleted:
            raise user_not_found
        await db_ses.commit()
    except ExpiredSignatureError:
        raise expired_jwt
    except (JWTError, JWTClaimsError):
        raise credentials_exception


@router.put("/users/{user_id")
async def update_user(user_id: int):
    ...
