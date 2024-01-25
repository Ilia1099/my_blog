from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError
from jose.constants import ALGORITHMS
from jose.exceptions import JWTClaimsError
from sqlalchemy.exc import IntegrityError
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.databases.connection import get_session
from app.serializers.posts_serializer import NewPostData, Reaction
from app.services.posts_management import create_post_inst, bind_post_to_user,\
    select_posts, post_row_converter
from app.services.exception_tools import expired_jwt, credentials_exception
from app.services.user_verification import authorize_user
from app.services.exception_tools import data_caused_integrity_error

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.get("/posts", status_code=200)
async def get_all_posts(
        token: Annotated[str, Depends(oauth2_scheme)],
        db_ses: Annotated[AsyncSession, Depends(get_session)]
):
    """
    endpoint to get all posts regardless of who created it,
    uses StreamingResponse and sqlalchemy streaming asyncresult
    :param token: users token for authorization
    :param db_ses: async session instance
    """
    try:
        await authorize_user(db_ses=db_ses, token=token)
        all_posts = await select_posts(db_ses)
        resp = post_row_converter(all_posts)
        return StreamingResponse(resp, media_type="application/json")
    except ExpiredSignatureError:
        raise expired_jwt
    except (JWTError, JWTClaimsError):
        raise credentials_exception


@router.get("/posts/{post_id}")
async def get_post(
        token: Annotated[str, Depends(oauth2_scheme)],
        post_id: str,
        db_ses: Annotated[AsyncSession, Depends(get_session)]
):
    """
    endpoint to get a single post by post_id
    :param token: users token for authorization
    :param post_id: stringified id of the certain post
    :param db_ses: async session instance
    """
    users_id = await authorize_user(db_ses=db_ses, token=token)
    posts = await select_posts(db_ses=db_ses,
                               user_id=users_id,
                               post_id=post_id)
    # TODO
    # finish


@router.post("/posts", status_code=201)
async def add_post_for_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        post_data: NewPostData,
        db_ses: Annotated[AsyncSession, Depends(get_session)]
):
    """
    endpoint for adding new post
    :param token: users token for authorization
    :param post_data:
    :param db_ses: async session instance
    :return:
    """
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


@router.delete("/posts/{post_id}")
async def delete_a_post(
        token: Annotated[str, Depends(oauth2_scheme)],
        post_id: str,
        db_ses: Annotated[AsyncSession, Depends(get_session)]
):
    ...


@router.post("/posts/reactions")
async def add_reaction_to_post(
        token: Annotated[str, Depends(oauth2_scheme)],
        reaction: Reaction,
        db_ses: Annotated[AsyncSession, Depends(get_session)]
):
    ...


@router.delete("/posts/reaction/{reaction_id}")
async def del_reaction_from_post(
        token: Annotated[str, Depends(oauth2_scheme)],
        reaction_id: str,
        db_ses: Annotated[AsyncSession, Depends(get_session)]
):
    ...
