from pydantic import BaseModel, ConfigDict, field_validator
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
    user_login: str | None
    user_uuid: str | None = None
    password: SecretStr | None
    email: str | None

    # TODO
    # rethink validators for fields


class UserRegData(BaseModel):
    """
    Pydantic class for received user data to proceed registration
    """
    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
        validate_default=True,
        extra='ignore',
        populate_by_name=True,

    )
    user_login: str
    password: SecretStr
    email: str

    @field_validator('*')
    @classmethod
    def check_fields_not_empty(cls, value: str):
        if not value:
            raise ValueError(f" must not be null")
        return value


class UserLogin(BaseModel):
    """
    Pydantic class designed specifically for validating credentials during
    login
    """
    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
        validate_default=True,
        extra='ignore',
        populate_by_name=True,

    )
    user_login: str
    password: SecretStr

    @field_validator('*')
    @classmethod
    def check_fields_not_empty(cls, value: str):
        if not value:
            raise ValueError(f"fields must not be null")
        return value
