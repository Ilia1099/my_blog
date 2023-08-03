from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from app.services.pswd_hasher import verify_password, hash_password
from app.services.users_management import get_user
from starlette.status import HTTP_404_NOT_FOUND
from decouple import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
secrets_path = Path(__file__).parent.parent.parent.resolve()
SECRET = config("SECRET")


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})


class UserNotFound(Exception):
    status_code = HTTP_404_NOT_FOUND


async def authenticate_user(db_ses: Annotated[AsyncSession, Depends("connector.get_session")],
                            user_uuid: str, password: str) -> bool:
    try:
        user = await get_user(db_ses, user_uuid)
        if not verify_password(password=password, hashed_password=user.password):
            return False
        return user
    except AttributeError as e:
        raise UserNotFound


def create_jwt_token(user_uuid: str):
    payload = {
        "sub": user_uuid,
        "exp": datetime.utcnow() + timedelta(days=config("ACCESS_TOKEN_EXPIRE_DAYS"))
    }
    encoded_jwt = jwt.encode(
        payload, SECRET, algorithm=config("ALGORITHM")
    )
    return encoded_jwt


async def authorize_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[config("ALGORITHM")])
        user_uuid = payload.get("sub")
        expiry = datetime.strptime(payload.get("exp"), "%Y-%m-%d %H:%M:%S.%f")
        if not user_uuid or datetime.utcnow() > expiry:
            raise credentials_exception
        return user_uuid
    except JWTError:
        raise credentials_exception


# TODO
# Create models
# Create endpoints for user registration, login
# Create connector, db engine, session, init alembic
# Test JWT creation and validation

