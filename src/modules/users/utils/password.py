from re import search

import bcrypt
import structlog.stdlib

from src.core.common.exceptions import BadRequestError
from src.modules.users.common.constants import PASSWORD_MIN_LENGTH

logger = structlog.stdlib.get_logger(__name__)


def generate_password_hash(password: str) -> str:
    """Generate hashed password."""
    salt = bcrypt.gensalt()
    password_bytes = password.encode("utf-8")
    hash_password = bcrypt.hashpw(password=password_bytes, salt=salt)

    return hash_password.decode("utf-8")


def verify_password_hash(password: str, hashed_password: str) -> bool:
    """Verify hashed password."""
    password_bytes = password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


def validate_password(password: str) -> bool:
    """Raise an exception if the password is not safe."""
    try:
        if len(password) < PASSWORD_MIN_LENGTH:
            raise BadRequestError(info="The password is too short.")
        if not any(char.isdigit() for char in password):
            raise BadRequestError(info="The password must contain at least one digit.")
        if not any(char.isupper() for char in password):
            raise BadRequestError(
                info="The password must contain at least one uppercase letter."
            )
        if not search("[@_!#info%^&*()<>?/|}{~:]", password):
            raise BadRequestError(
                info="The password must contain at least one special character."
            )
    except BadRequestError:
        logger.warning("[Common] User password invalid.")
        raise
    return True
