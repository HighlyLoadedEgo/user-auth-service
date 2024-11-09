import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
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


class CompanyInformation(Base, UUIDMixin, DateMixin):
    __tablename__ = "company_information"

    name: Mapped[str] = mapped_column(String, nullable=False, comment="Company name.")
    role: Mapped[str] = mapped_column(
        String, nullable=False, comment="Role in a company."
    )
    tin: Mapped[str] = mapped_column(
        String, nullable=False, comment="Taxpayer identification number"
    )
    rrc: Mapped[str] = mapped_column(
        String, nullable=False, comment="Registration reason code"
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, unique=True
    )

    user: Mapped["User"] = relationship("User", back_populates="company_information")
