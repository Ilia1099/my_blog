import uuid
from uuid import UUID

from app.models.base_model import MyBaseModel
from sqlalchemy import String, MetaData, DateTime, Text, UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import mapped_column, Mapped


class Users(MyBaseModel):
    __tablename__ = "users_table"
    user_uuid: Mapped[str] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, index=True)
    password: Mapped[str] = mapped_column(Text)
