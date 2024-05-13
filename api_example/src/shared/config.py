import os

import dotenv


class CannotFindEnvVarException(Exception):
    pass


class Config:
    def __init__(self):
        dotenv.load_dotenv()

    @staticmethod
    def _get(key: str) -> str:
        if env := os.getenv(key):
            return env

        raise CannotFindEnvVarException(f"Cannot find env var {key}")


class AuthConfig(Config):
    def __init__(self):
        super().__init__()

        self.secret_key = self._get("AUTH_SECRET_KEY")
        self.algorithm = self._get("AUTH_ALGORITHM")
        self.access_token_expire_minutes = int(
            self._get("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES")
        )
