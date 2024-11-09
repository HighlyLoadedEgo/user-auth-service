from src.core.database.models.base import Base
from src.core.database.models.company_information import CompanyInformation
from src.core.database.models.role import Role
from src.core.database.models.user import User

models: list[type[Base]] = [
    User,
    Role,
    CompanyInformation,
]
m2m_models: list[type[Base]] = []
