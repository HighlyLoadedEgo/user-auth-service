from re import search

import structlog.stdlib

from src.core.common.exceptions import BadRequestError
from src.modules.users.common.constants import (
    PASSWORD_MIN_LENGTH,
    UserWebRole,
)
from src.modules.users.dtos.user_dtos import (
    BaseUserDTO,
    FullUserDTO,
    UserCreateDTO,
    UserLoginDTO,
    WebUserCreateDTO,
)
from src.modules.users.exceptions import (
    AuthenticationError,
    EmailAlreadyInUseError,
    PermissionDeniedError,
)
from src.modules.users.utils.password import verify_password_hash

logger = structlog.stdlib.get_logger(__name__)


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


def validate_full_name(data: WebUserCreateDTO | UserCreateDTO) -> bool:
    """Raise an exception if there are non-letters in the name."""
    to_validate = [data.name, data.surname]
    if data.middle_name:
        to_validate.append(data.middle_name)
    for field in to_validate:
        if not all(char.isalpha() for char in field):
            logger.warning("[Common] User full name invalid.")
            raise BadRequestError(info="Bad user full name.")
    return True


def check_permission(
    user: FullUserDTO | BaseUserDTO, permission_list: list[str]
) -> bool:
    """Raise an exception if user doesn't have permission."""
    user_role = user.role
    try:
        if not user_role:
            raise PermissionDeniedError(info="User doesn't have permission")
        if user_role.name not in permission_list:
            raise PermissionDeniedError(info="User doesn't have permission")
    except PermissionDeniedError:
        logger.warning("[Common] User doesn't have permission.")
        raise
    return True


def validate_registering_user_role(
    create_user_data: WebUserCreateDTO, permission_list: list[str]
) -> bool:
    user_role = create_user_data.role
    try:
        if user_role.name not in permission_list:
            raise BadRequestError(info="Unsupported role.")
        if create_user_data.company_information and user_role == UserWebRole.INDIVIDUAL:
            raise BadRequestError(info="User doesn't set correct role.")
    except PermissionDeniedError:
        logger.warning("[Common] User doesn't set correct role.")
        raise
    return True


def password_validator(login_data: UserLoginDTO, user: FullUserDTO) -> bool:
    """Raise an exception if passwords don't match or user doesn't exist."""
    if not verify_password_hash(
        password=login_data.password, hashed_password=user.password
    ):
        logger.warning("[Common] User's credentials is invalid.")
        raise AuthenticationError()
    return True


def validate_user_active(
    user: FullUserDTO,
) -> bool:
    """Raise an exception if the user not active."""
    if not user.is_active:
        logger.warning("[Common] User is not active.")
        raise PermissionDeniedError(info="User is not active")
    return True


def validate_user_confirmed(
    user: FullUserDTO,
) -> bool:
    """Raise an exception if the user not active."""
    if not user.is_confirmed:
        logger.warning("[Common] User is not confirmed.")
        raise PermissionDeniedError(info="User is not confirmed")
    return True


def validate_email_not_in_use(user: FullUserDTO | None) -> bool:
    """Raise an exception if the email already exists."""
    if user:
        logger.warning("[Common] Email already in use.")
        raise EmailAlreadyInUseError(email=user.email)
    return True


def validate_base_authentication_data(
    user: FullUserDTO, login_data: UserLoginDTO
) -> bool:
    """Include base auth logic."""
    password_validator(login_data=login_data, user=user)
    validate_user_active(user=user)
    return True
