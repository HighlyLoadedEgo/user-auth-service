from enum import Enum


class TokenTypes(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
