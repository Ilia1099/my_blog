from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from app.models.users import Users
from app.serializers.users_serializer import UserInfo
from app.services.pswd_hasher import verify_password, hash_password
# from app.services.users_management import get_user
from starlette.status import HTTP_404_NOT_FOUND
from app.main import get_session
from decouple import config

from app.services.users_management import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
secrets_path = Path(__file__).parent.parent.parent.resolve()
SECRET = config("SECRET")


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
data_exception = HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "check data"
        )
failed_login = HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail="check login or password")


async def authenticate_user(
        db_ses: AsyncSession,
        login: str, password: str) -> Users:
    user = await get_user(db_ses, login)
    if verify_password(password=password, hashed_password=user.password):
        return user
    else:
        raise failed_login


def create_jwt_token(user_uuid: str):
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


async def authorize_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    payload = jwt.decode(token, SECRET, algorithms=[config("ALGORITHM")])
    user_uuid = payload.get("sub")
    return user_uuid


def grant_jwt(user: UserInfo, new_user: bool = True):
    user_id = f"{user.user_uuid}"
    token = f"{create_jwt_token(user_id)}"
    content = {
        "user_uuid": f"{user.user_uuid}",
        "access_token": f"{create_jwt_token(user_id)}",
        "token_type": "bearer"
    }
    if new_user: content["user_created"] = new_user
    response = JSONResponse(content=content)
    response.set_cookie(key="access_token", value=token)
    response.status_code = 201
    return response


# TODO
# Create models!!!!!
# Test user_verification
# Create endpoints for user registration, login
# Create connector, db engine, session, init alembic
# Test JWT creation and validation

