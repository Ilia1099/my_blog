from sqlalchemy import String, MetaData, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import mapped_column, DeclarativeBase


class MyBaseModel(DeclarativeBase):
    pass
