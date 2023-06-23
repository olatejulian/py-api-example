from abc import ABC, abstractmethod

from ..account import Account


class AccountNotFoundException(Exception):
    pass


class AccountRepository(ABC):
    @abstractmethod
    async def save(self, account: Account) -> Account:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, account_id) -> Account:
        raise NotImplementedError

    @abstractmethod
    async def update(self, account: Account) -> None:
        raise NotImplementedError
