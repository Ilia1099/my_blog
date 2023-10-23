from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.databases.connection import get_session
from app.serializers.users_serializer import UserInfo, UserLogin, UserRegData
from app.services.users_management import (user_registration, usr_deletion,
                                           usr_update)
from app.services.user_verification import (authenticate_user, grant_jwt,
                                            authorize_user)
from app.services.exception_tools import (credentials_exception,
                                          data_exception, expired_jwt,
                                          user_not_found,
                                          data_caused_integrity_error)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


class ServiceError(Exception):
    pass


@router.post("/add_user")
async def register_new_user(
        user_data: UserRegData,
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
        print("DATA")
        print(user_data)
        result = await user_registration(
            credentials=user_data, db_ses=db_ses)
        await db_ses.commit()
        return grant_jwt(user=result, st_code=201)
    except IntegrityError as e:
        raise data_caused_integrity_error(e.orig.args[0])
    except ValueError:
        raise data_exception


@router.post("/users/login")
async def user_login(
        credentials: UserLogin,
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
        return grant_jwt(user=user, st_code=200, new_user=False)
    except ExpiredSignatureError:
        raise expired_jwt
    except (JWTError, JWTClaimsError):
        raise credentials_exception


@router.delete("/users/{user_login}", status_code=200)
async def delete_user(
        user_login: str,
        token: Annotated[str, Depends(oauth2_scheme)],
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
        return {"message": "successfully deleted"}
    except ExpiredSignatureError:
        raise expired_jwt
    except (JWTError, JWTClaimsError):
        raise credentials_exception


@router.patch("/users/{user_login}", status_code=202)
async def update_user(
        user_login: str,
        user_info: UserInfo,
        token: Annotated[str, Depends(oauth2_scheme)],
        db_ses: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    """
    user update endpoint, implemented via PATCH method, due to flexibility;
    in current implementation up on success returns corresponding message
    and the path to updated user (if permissions allow to see it; - to be
    developed)
    :param user_login: login of the user whose account record should be
    updated; supposed that the process could be initialized by user himself
    or authorized admin
    :param user_info: new user's data
    :param token: JWT for authorization
    :param db_ses: database session object
    :return: dictionary containing necessary data
    """
    try:
        await authorize_user(db_ses=db_ses, token=token)
        updated = await usr_update(
            user_login=user_login, db_ses=db_ses, new_data=user_info)
        if not updated:
            raise user_not_found
        await db_ses.commit()
        await db_ses.refresh(updated)
        return {
            "message": "successfully updated",
            "path": f"/users/{user_login}"
        }
    except ExpiredSignatureError:
        raise expired_jwt
    except IntegrityError as e:
        raise data_caused_integrity_error(e.orig.args[0])
    except (JWTError, JWTClaimsError):
        raise credentials_exception

# TODO
# permissions, roles logic
