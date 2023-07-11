from abc import ABC, abstractmethod

from ..account import Account
from ..value_object import EmailAddress


class AccessTokenDto:
    def __init__(self, access_token: str, token_type: str):
        self.access_token = access_token
        self.token_type = token_type


class AccountAuthenticator(ABC):
    @abstractmethod
    async def authenticate(
        self, email: EmailAddress, plain_password: str
    ) -> AccessTokenDto:
        raise NotImplementedError

    @abstractmethod
    async def get_current_account(self, token: str) -> Account:
        raise NotImplementedError
