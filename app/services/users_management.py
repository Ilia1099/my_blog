from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from app.models.users import Users


async def get_user(db_ses: Annotated[AsyncSession, Depends("connector.get_session")],
                   user_uuid: str):
    qs = aliased(Users, name="user")
    query = select(qs).where(qs.user_uuid == user_uuid)
    result = await db_ses.execute(query)
    return result.one()