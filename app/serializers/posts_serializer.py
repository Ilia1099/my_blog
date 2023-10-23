from pydantic import BaseModel, ConfigDict
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo


class PostData(BaseModel):
    """
    Pydantic based class for storing and validating post's data received
    from client side
    """

    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
        validate_default=True,
        populate_by_name=True,
    )

    post_header: str
    post_text: str
    user_id: str

    @field_validator('*')
    @classmethod
    def check_fields_not_empty(cls, value: str, info: ValidationInfo):
        if not value:
            raise ValueError(f"{value.title()} must mot be null")
        return value
