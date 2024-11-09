from src.core.database.models import User
from src.modules.users.dtos.user_dtos import (
    UserCreateDTO,
    UserDTO,
)
from src.modules.users.exceptions import UserIsAlreadyExistError
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.utils.password import generate_password_hash
from src.modules.users.validators.user_validators import validate_password


class RegistrateAdminUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def __call__(self, registrate_data: UserCreateDTO) -> UserDTO:
        validate_password(password=registrate_data.password)
        user: User | None = await self._user_repo.get_user_by_email(
            email=registrate_data.email
        )
        if user:
            raise UserIsAlreadyExistError(email=registrate_data.email)
        registrate_data.password = generate_password_hash(
            password=registrate_data.password
        )
        return await self._user_repo.create_user(data=registrate_data)
