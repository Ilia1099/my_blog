import uuid
from typing import Literal, Optional, Any

from pydantic import BaseModel, ConfigDict
from app.databases.config import SecretStr


class UserInfo(BaseModel):
    """
    Pydantic class for received user data
    """
    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
        validate_default=True,
        extra='ignore',
        populate_by_name=True,

    )
    user_login: str
    user_uuid: Any = None
    password: SecretStr

    @classmethod
    def from_dict(cls, question: dict):
        return cls(
            user_login=question.get("user_login"),
            password=question.get("user_password")
        )
