import json
import uuid
from typing import List, Any, Sequence

from sqlalchemy import select, or_, Row, RowMapping
from sqlalchemy.orm import aliased

from app.models import Posts, LikesForPost, DislikesForPost
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from app.serializers.posts_serializer import NewPostData, RetrievedPost
from app.services.exception_tools import user_not_found
from app.services.users_management import get_user


async def select_posts(
        db_ses: AsyncSession,
        user_id: str = None,
        post_id: str = None
) -> AsyncResult:
    """
    a coroutine to query posts; if neither user_id and post_id were provided
    then all posts will be queried and returned (equal to select *...);
    in other case either one or another parameter will be applied to filter
    :param db_ses: AsyncSession instance
    :param user_id: user's uuid
    :param post_id: post's uuid
    :return: AsyncResult
    """
    qs = aliased(Posts, name="pst")
    query = select(qs)
    if user_id is None and post_id is None:
        pass
    else:
        filters = []
        if user_id is not None:
            filters.append(qs.user_id == user_id)
        elif post_id is not None:
            filters.append(qs.post_id == post_id)
        query = query.filter(or_(*filters))
    result = await db_ses.stream(query)
    return result


async def post_row_converter(rows: AsyncResult):
    """
    coroutine generator which iterates over AsyncResult, converts each row
    into PostData object and yields it
    :param rows:
    :return:
    """
    async for row in rows:
        cur_post = RetrievedPost.model_validate(*row).model_dump()
        yield json.dumps(cur_post, default=str)


async def create_post_inst(
        db_ses: AsyncSession, post_data: NewPostData
) -> Posts:
    """
    a coroutine which creates new post instance
    :param db_ses: AsyncSession instance
    :param post_data: Pydantic class which holds necessary information to
    create new instance of Posts model
    :return: freshly created Posts instance
    """
    try:
        new_post = Posts(
            post_header=post_data.post_header,
            post_text=post_data.post_text,
            user_id=post_data.user_id
        )
        db_ses.add(new_post)
        return new_post
    except ValueError:
        print("error occured during saving new db instance, "
              "check serializer or model")


async def bind_post_to_user(
    db_ses: AsyncSession, user_id: str, np: Posts
):
    """
    a coroutine which binds new post instance to user created it
    :param db_ses: async session instance
    :param user_id: id of the user who created certain post
    :param np: newly created post
    """
    creator = await get_user(db_ses=db_ses, user_uuid=user_id)
    if not creator:
        raise user_not_found
    creator.posts.append(np)


async def delete_post(
        db_ses: AsyncSession,
        post_id: str
):
    ...


async def add_reaction_to_post():
    ...


async def del_reaction_to_post():
    ...


# TODO
# make get_posts function with possible parametrization
# make functions for manipulation with user reactions (only authenticated
# users can leave a reaction)
