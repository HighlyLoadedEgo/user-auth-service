import datetime

from jose import (
    ExpiredSignatureError,
    JWTError,
    jwt,
)

from src.config.auth import AuthConfig
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
    def __init__(self, jwt_config: AuthConfig) -> None:
        self._jwt_config = jwt_config

    def create_token_pair(self, subject: UserSubject) -> TokensData:
        """Function to create jwt pair."""
        access_token = self._create_access_token(subject=subject)
        refresh_token = self._create_refresh_token(subject=subject)

        return TokensData(access_token=access_token, refresh_token=refresh_token)

    def refresh_access_token(self, refresh_token: str) -> str:
        """Refresh token and get new access token."""
        payload = self.decode_token(
            token=refresh_token, secret_key=self._jwt_config.REFRESH_SECRET
        )
        return self._create_access_token(subject=UserSubject.model_validate(payload))

    def decode_token(
        self, token: str, secret_key: str | None = None
    ) -> UserTokenPayload:
        """Decodes a JWT token to extract the payload."""
        if not secret_key:
            secret_key = self._jwt_config.ACCESS_SECRET
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

    def _create_access_token(self, subject: UserSubject) -> str:
        """Creates an access token for a given user."""
        access_token = self._create_jwt_token(
            subject=subject,
            expire_minutes=self._jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES,
            secret_key=self._jwt_config.ACCESS_SECRET,
        )

        return access_token

    def _create_refresh_token(self, subject: UserSubject) -> str:
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
