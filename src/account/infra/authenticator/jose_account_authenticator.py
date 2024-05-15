import pendulum
from jose import JWTError, jwt

from src.account.domain import (
    AccessTokenDto,
    Account,
    AccountAuthenticator,
    AccountNotFoundException,
    AccountRepository,
    EmailAddress,
    InvalidEmailAddressException,
)
from src.shared import Config


class InvalidAccessTokenException(Exception):
    pass


class AuthConfig(Config):
    def __init__(self):
        super().__init__()

        self.secret_key = self._get("AUTH_SECRET_KEY")
        self.algorithm = self._get("AUTH_ALGORITHM")
        self.access_token_expire_minutes = int(
            self._get("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES")
        )


class JoseAccountAuthenticator(AccountAuthenticator):
    def __init__(self, config: AuthConfig, repository: AccountRepository):
        self.config = config
        self.repository = repository

    def __generate_access_token(self, email: EmailAddress) -> str:
        expire = pendulum.now().add(minutes=self.config.access_token_expire_minutes)

        data = {"sub": email.value, "exp": expire}

        return jwt.encode(data, self.config.secret_key, algorithm=self.config.algorithm)

    async def authenticate(
        self, email: EmailAddress, plain_password: str
    ) -> AccessTokenDto:
        try:
            account = await self.repository.get_by_email(email)

        except AccountNotFoundException as exc:
            raise InvalidAccessTokenException() from exc

        else:
            if not account.compare_password(plain_password):
                raise InvalidAccessTokenException()

            return AccessTokenDto(
                access_token=self.__generate_access_token(email),
                token_type="bearer",
            )

    async def get_current_account(self, token: str) -> Account:
        try:
            payload = jwt.decode(
                token, self.config.secret_key, algorithms=[self.config.algorithm]
            )

            if (
                (sub := payload.get("sub"))
                and (exp := payload.get("exp"))
                and pendulum.from_timestamp(int(exp)) > pendulum.now()
            ):
                account = await self.repository.get_by_email(EmailAddress(sub))

                return account

            raise InvalidAccessTokenException()

        except (
            JWTError,
            AccountNotFoundException,
            InvalidEmailAddressException,
        ) as exc:
            raise InvalidAccessTokenException() from exc
