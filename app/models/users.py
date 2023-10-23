import uuid
from typing import List
from app.models.base_model import Base
from sqlalchemy import String, DateTime, Text, UUID
from datetime import datetime as dt
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Users(Base):
    __tablename__ = "users_table"
    user_uuid: Mapped[str] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, index=True, primary_key=True
    )
    user_login: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    date_created: Mapped[dt] = mapped_column(default=dt.now())
    date_updated: Mapped[dt] = mapped_column(DateTime, default=func.now())
    posts: Mapped[List['Posts']] = relationship(back_populates="user")

