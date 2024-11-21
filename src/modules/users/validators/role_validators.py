from uuid import UUID

import structlog
from pydantic import BaseModel

from src.core.common.exceptions import NotFoundError

logger = structlog.stdlib.get_logger(__name__)


def validate_role_exists(
    role: None | UUID | BaseModel,
) -> bool:
    """Raise an exception if the role is not found."""
    if not role:
        logger.warning("[Common] Role not found.")
        raise NotFoundError(info="Role doesn't exist.")
    return True
