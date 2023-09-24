from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated
from fastapi import Depends
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from app.models.users import Users
from app.serializers.users_serializer import UserInfo
from app.services.pswd_hasher import verify_password
from decouple import config

from app.services.users_management import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
secrets_path = Path(__file__).parent.parent.parent.resolve()
SECRET = config("SECRET")


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

data_exception = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="check data"
)

failed_login = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="check login or password"
)
expired_jwt = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="jwt expired, login to receive new one"
)

authorization_not_completed = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="authorization for operation wasn't completed, check login of "
           "requester for correctness"
)

user_not_found = HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail="certain user wasn't found"
)


async def authenticate_user(
        db_ses: AsyncSession,
        login: str, password: str) -> Users | bool:
    """
    a coroutine for user authentication, password wasn't verified raises
    exception
    :param db_ses: yielded db session instance
    :param login: user's login received from request
    :param password: user's password received from request
    :return: user instance
    """
    user = await get_user(db_ses, login)
    if not user:
        return False
    if verify_password(password=password, hashed_password=user.password):
        return user
    else:
        raise failed_login


def create_jwt_token(user_uuid: str) -> str:
    """
    a function which generates JWT for certain user
    :param user_uuid: user's uuid
    :return: JWT
    """
    payload = {
        "sub": user_uuid,
        "exp": datetime.utcnow() + timedelta(
            days=int(config("ACCESS_TOKEN_EXPIRE_DAYS"))
        )
    }
    encoded_jwt = jwt.encode(
        payload, SECRET, algorithm=config("ALGORITHM")
    )
    return encoded_jwt


async def validate_jwt(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    """
    a coroutine which decodes received JWT if successful returns user's uuid
    :param token: a JWT
    :return: uuid
    """
    payload = jwt.decode(token, SECRET, algorithms=[config("ALGORITHM")])
    user_uuid = payload.get("sub")
    return user_uuid


def grant_jwt(st_code: int, user: UserInfo, new_user: bool = True) -> (
        JSONResponse):
    """
    a function which generates JSONResponse as a finishing stage of user
    authentication or registration
    :param st_code: corresponding status code, may be different if this
    function is used during creation of a new user or authentication of
    existing
    :param user: user instance
    :param new_user: a flag, if not new user doesn't add info about
    successful creation
    """
    user_id = f"{user.user_uuid}"
    token = f"{create_jwt_token(user_id)}"
    content = {
        "user_uuid": f"{user.user_uuid}",
        "access_token": f"{create_jwt_token(user_id)}",
        "token_type": "bearer"
    }
    if new_user: content["user_created"] = new_user
    response = JSONResponse(content=content)
    response.set_cookie(key="access_token", value=token, httponly=True)
    response.status_code = st_code
    return response


async def authorize_user(db_ses: AsyncSession, token: str):
    """
    a coroutine which authenticates user which makes request; existences,
    permissions
    :param db_ses: AsyncSession instance
    :param token: JWT token
    :return: None
    """
    users_uid = await validate_jwt(token)
    chk_exists = await get_user(db_ses=db_ses, user_uuid=users_uid)
    if not chk_exists:
        raise authorization_not_completed
    