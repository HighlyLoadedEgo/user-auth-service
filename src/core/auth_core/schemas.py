import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    field_serializer,
)


class UserSubject(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID

    @field_serializer("id")
    @classmethod
    def id_serializer(cls, id_: UUID) -> str:
        return str(id_)


class UserTokenPayload(UserSubject):
    exp: datetime.datetime
    iat: datetime.datetime


class TokensData(BaseModel):
    access_token: str
    refresh_token: str
