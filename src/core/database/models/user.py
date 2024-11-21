import uuid
from typing import (
    TYPE_CHECKING,
    Optional,
)

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Index,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.core.database.models.base import Base
from src.core.database.models.mixins.date_mixins import DateMixin
from src.core.database.models.mixins.id_mixins import UUIDMixin

if TYPE_CHECKING:
    from src.core.database.models.company_information import CompanyInformation
    from src.core.database.models.role import Role


class User(Base, UUIDMixin, DateMixin):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, comment="User email."
    )
    phone: Mapped[str] = mapped_column(
        String, nullable=False, comment="User phone number."
    )
    password: Mapped[str] = mapped_column(
        String, nullable=False, comment="User password."
    )
    name: Mapped[str] = mapped_column(String, nullable=False, comment="User name.")
    middle_name: Mapped[Optional[str]] = mapped_column(
        String, comment="User middle name."
    )
    surname: Mapped[str] = mapped_column(
        String, nullable=False, comment="User surname."
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Access to UI Optional flag."
    )
    is_mail: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Mailing flag."
    )
    is_confirmed: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Confirmed email flag."
    )

    role_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("role.id", ondelete="SET NULL"), nullable=True
    )

    role: Mapped[Optional["Role"]] = relationship("Role", back_populates="users")
    company_information: Mapped[Optional["CompanyInformation"]] = relationship(
        "CompanyInformation", back_populates="user", uselist=False
    )

    __table_args__ = (Index(None, "role_id"),)
