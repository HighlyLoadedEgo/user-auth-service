import datetime

from jose import (
    ExpiredSignatureError,
    JWTError,
    jwt,
)

from src.config.auth import JWTConfig
from src.core.auth_core.exceptions import (
    InvalidTokenError,
    TokenExpiredError,
)
from src.core.auth_core.schemas import (
    TokensData,
    UserSubject,
    UserTokenPayload,
)


class JWTManager:
    def __init__(self, jwt_config: JWTConfig) -> None:
        self._jwt_config = jwt_config

    def create_token_pair(self, subject: UserSubject) -> TokensData:
        """Function to create jwt pair."""
        access_token = self.create_access_token(subject=subject)
        refresh_token = self.create_refresh_token(subject=subject)

        return TokensData(access_token=access_token, refresh_token=refresh_token)

    def decode_token(self, token: str, secret_key: str) -> UserTokenPayload:
        """Decodes a JWT token to extract the payload."""
        try:
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=[self._jwt_config.ALGORITHM],
            )
        except ExpiredSignatureError:
            raise TokenExpiredError()
        except JWTError as err:
            raise InvalidTokenError() from err

        return UserTokenPayload(**payload)

    def create_access_token(self, subject: UserSubject) -> str:
        """Creates an access token for a given user."""
        access_token = self._create_jwt_token(
            subject=subject,
            expire_minutes=self._jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES,
            secret_key=self._jwt_config.ACCESS_SECRET,
        )

        return access_token

    def create_refresh_token(self, subject: UserSubject) -> str:
        """Creates a refresh token for a given user."""
        access_token = self._create_jwt_token(
            subject=subject,
            expire_minutes=self._jwt_config.REFRESH_TOKEN_EXPIRE_MINUTES,
            secret_key=self._jwt_config.REFRESH_SECRET,
        )

        return access_token

    def _create_jwt_token(
        self, subject: UserSubject, expire_minutes: int, secret_key: str
    ) -> str:
        """Function to create jwt token."""
        iat = datetime.datetime.now(datetime.UTC)
        expires_delta = iat + datetime.timedelta(minutes=expire_minutes)

        payload = {
            "iat": iat,
            "exp": expires_delta,
            "id": str(subject.id),
        }

        return jwt.encode(payload, secret_key, algorithm=self._jwt_config.ALGORITHM)
