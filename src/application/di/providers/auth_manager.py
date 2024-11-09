# from enum import Enum
# from typing import Annotated
#
# from fastapi import Depends
# from fastapi.security import (
#     HTTPAuthorizationCredentials,
#     HTTPBearer,
# )
#
# from src.core.auth_core.constants import TokenTypes
# from src.core.auth_core.exceptions import AccessDeniedError
# from src.core.auth_core.jwt import JWTManager
# from src.core.auth_core.schemas import (
#     UserSubject,
#     UserTokenPayload,
# )
# from src.core.auth_core.stubs import jwt_manager_stub
#
#
# # TODO перенести в фппликейшн и сделать получение пользователя из кеша или бд
# class AuthManager:
#     def __init__(
#         self,
#         action_type: TokenTypes = TokenTypes.ACCESS,
#         # TODO: добавить конкретные классы ролей
#         permission_list: list[Enum] | None = None,
#     ) -> None:
#         self._action_type = action_type
#         self._permission_list = permission_list
#
#     def __call__(
#         self,
#         credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
#         jwt_manager: Annotated[JWTManager, Depends(jwt_manager_stub)],
#     ) -> UserSubject:
#         """Check access for permission list."""
#         payload: UserTokenPayload = jwt_manager.decode_token(
#             token=credentials.credentials, type_=self._action_type
#         )
#         if self._permission_list:
#             if payload.role not in self._permission_list:
#                 raise AccessDeniedError()
#
#         return UserSubject.model_validate(payload)
