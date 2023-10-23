from app.models import Posts, LikesForPost, DislikesForPost
from sqlalchemy.ext.asyncio import AsyncSession
from app.serializers.posts_serializer import PostData
from app.services.exception_tools import user_not_found
from app.services.users_management import get_user


async def create_post_inst(db_ses: AsyncSession, post_data: PostData) -> Posts:
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
    creator = await get_user(db_ses=db_ses, user_uuid=user_id)
    if not creator:
        raise user_not_found
    creator.posts.append(np)

