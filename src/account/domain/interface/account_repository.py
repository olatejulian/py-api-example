from abc import ABC, abstractmethod

from ..account import Account


class DuplicateIdOrEmailException(Exception):
    pass


class AccountNotFoundException(Exception):
    pass


class AccountRepository(ABC):
    @abstractmethod
    async def save(self, account: Account) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, account_id) -> Account:
        raise NotImplementedError

    @abstractmethod
    async def update(self, account: Account) -> None:
        raise NotImplementedError
