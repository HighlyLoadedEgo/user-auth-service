from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.core.database.models import Base
from src.core.database.models.mixins.date_mixins import DateMixin
from src.core.database.models.mixins.id_mixins import UUIDMixin

if TYPE_CHECKING:
    from src.core.database.models.user import User


class Role(Base, UUIDMixin, DateMixin):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(
        String, nullable=False, comment="Role name.", unique=True
    )

    users: Mapped[list["User"]] = relationship("User", back_populates="role")
