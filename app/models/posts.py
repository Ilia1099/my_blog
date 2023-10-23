import uuid
from typing import List
from app.models.base_model import Base
from sqlalchemy import String, DateTime, Text, UUID, ForeignKey
from datetime import datetime as dt
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Posts(Base):
    __tablename__ = "users_posts"
    post_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, index=True, primary_key=True
    )
    post_header: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    post_text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users_table.user_uuid"))
    date_created: Mapped[dt] = mapped_column(default=dt.now())
    date_updated: Mapped[dt] = mapped_column(DateTime, default=func.now())
    user: Mapped["Users"] = relationship(back_populates="posts")
    likes: Mapped[List["LikesForPost"]] = relationship(
        back_populates="post")
    dislikes: Mapped[List["DislikesForPost"]] = relationship(
        back_populates="post")


class LikesForPost(Base):
    __tablename__ = "likes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_valid: Mapped[bool] = mapped_column()
    date_created: Mapped[dt] = mapped_column(default=dt.now())
    date_updated: Mapped[dt] = mapped_column(DateTime, default=func.now())
    post_id: Mapped[str] = mapped_column(ForeignKey("users_posts.post_id"))
    post: Mapped["Posts"] = relationship(back_populates="likes")


class DislikesForPost(Base):
    __tablename__ = "dislikes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_valid: Mapped[bool] = mapped_column()
    date_created: Mapped[dt] = mapped_column(default=dt.now())
    date_updated: Mapped[dt] = mapped_column(DateTime, default=func.now())
    post_id: Mapped[str] = mapped_column(ForeignKey("users_posts.post_id"))
    post: Mapped["Posts"] = relationship(back_populates="dislikes")
