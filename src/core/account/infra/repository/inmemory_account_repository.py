from src.core.account.domain import Account, AccountNotFoundException, AccountRepository

from .exception import DuplicateIdOrEmailException


class InMemoryAccountRepository(AccountRepository):
    def __init__(self):
        self._accounts: dict[tuple[str, str], Account] = {}

    async def save(self, account: Account) -> Account:
        indexes = (account.id.value, account.email.address.value)

        if indexes not in self._accounts:
            self._accounts[indexes] = account

        else:
            raise DuplicateIdOrEmailException

        return account

    async def get_by_id(self, account_id) -> Account:
        for account in self._accounts.values():
            if account.id.value == account_id:
                return account

        raise AccountNotFoundException()

    async def update(self, account: Account) -> None:
        indexes = (account.id.value, account.email.address.value)

        if indexes in self._accounts:
            self._accounts[indexes] = account

        else:
            raise AccountNotFoundException()
