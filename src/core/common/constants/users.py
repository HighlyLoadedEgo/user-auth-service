import enum


class CompanyRoles(str, enum.Enum):
    SUPPLY = "SUPPLY"
    PROCUREMENT = "PROCUREMENT"
    TECHNOLOGY = "TECHNOLOGY"
    DEVELOPMENT = "DEVELOPMENT"
    SALES = "SALES"
