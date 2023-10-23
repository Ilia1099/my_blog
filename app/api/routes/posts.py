from typing import Annotated
from decouple import config
from pathlib import Path
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError
from jose.constants import ALGORITHMS
from datetime import datetime, timedelta

from jose.exceptions import JWTClaimsError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.databases.connection import get_session
from app.serializers.posts_serializer import PostData
from app.services.posts_management import create_post_inst, bind_post_to_user
from app.services.exception_tools import expired_jwt, credentials_exception
from app.services.user_verification import authorize_user
from app.services.exception_tools import data_caused_integrity_error

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.post("/add_post", status_code=201)
async def add_post_for_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        post_data: PostData,
        db_ses: Annotated[AsyncSession, Depends(get_session)]
):
    try:
        await authorize_user(db_ses=db_ses, token=token)
        new_post = await create_post_inst(db_ses=db_ses, post_data=post_data)
        await bind_post_to_user(
            db_ses=db_ses, user_id=post_data.user_id, np=new_post)
        await db_ses.commit()
    except ExpiredSignatureError:
        raise expired_jwt
    except IntegrityError as e:
        raise data_caused_integrity_error(e.orig.args[0])
    except (JWTError, JWTClaimsError):
        raise credentials_exception
