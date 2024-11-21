from enum import Enum

PASSWORD_MIN_LENGTH = 12


class CompanyRole(str, Enum):
    """Enum for table CompanyInformation."""

    SUPPLY = "SUPPLY"
    PROCUREMENT = "PROCUREMENT"
    TECHNOLOGY = "TECHNOLOGY"
    DEVELOPMENT = "DEVELOPMENT"
    SALES = "SALES"


class AdminUserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"


class UserWebRole(Enum):
    """User web role choices."""

    INDIVIDUAL = "INDIVIDUAL"
    CORPORATE = "CORPORATE"


admin_role_list: list[str] = list(AdminUserRole.__members__)
user_role_list: list[str] = list(UserWebRole.__members__)
