from abc import ABC, abstractmethod

from ..account import Account, EmailAddress, Id


class DuplicateIdOrEmailException(Exception):
    pass


class AccountNotFoundException(Exception):
    pass


class AccountRepository(ABC):
    @abstractmethod
    async def save(self, account: Account) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, account_id: Id) -> Account:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: EmailAddress) -> Account:
        raise NotImplementedError

    @abstractmethod
    async def update(self, account: Account) -> None:
        raise NotImplementedError
