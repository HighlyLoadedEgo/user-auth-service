from pydantic import (
    BaseModel,
    EmailStr,
)


class UserCreateRequestSchema(BaseModel):
    """User create response schema."""

    name: str
    surname: str
    middle_name: str | None
    email: EmailStr
    phone: str
    password: str
