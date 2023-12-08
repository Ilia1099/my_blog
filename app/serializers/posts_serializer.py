import uuid
from typing import Type, Union, Annotated, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator, Field
# from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo


class NewPostData(BaseModel):
    """
    Pydantic based class for storing and validating post's data received
    from client side
    """

    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
        validate_default=True,
        populate_by_name=True,
        extra='ignore',
    )

    post_header: str
    post_text: str
    user_id: str

    # @field_validator('*', check_fields=False)
    # @classmethod
    # def check_fields_not_empty(cls, value: str, info: ValidationInfo):
    #     if not value:
    #         raise ValueError(f"{value.title()} must mot be null")
    #     return value

    # @field_validator('user_id', check_fields=False)
    # @classmethod
    # def check_post_id(cls, value) -> str:
    #     if not all([isinstance(value, uuid.UUID), isinstance(value, str)]):
    #         raise ValueError(f"{value.title()} must be a string")
    #     elif isinstance(value, uuid.UUID):
    #         value = str(value)
    #     return value


class RetrievedPost(BaseModel):
    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
        validate_default=True,
        populate_by_name=True,
        extra='ignore',
    )

    post_id: uuid.UUID
    post_header: str
    post_text: str
    user_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class Reaction(BaseModel):
    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
        validate_default=True,
        populate_by_name=True,
    )
