from src.account.domain import (
    Account,
    AccountNotFoundException,
    AccountRepository,
    DuplicateIdOrEmailException,
    EmailAddress,
    Id,
)


class FakeAccountRepository(AccountRepository):
    def __init__(self):
        self._accounts: dict[tuple[str, str], Account] = {}

    async def save(self, account: Account) -> None:
        indexes = (account.id.value, account.email.address.value)

        if indexes not in self._accounts:
            self._accounts[indexes] = account

        else:
            raise DuplicateIdOrEmailException

    async def get_by_id(self, account_id: Id) -> Account:
        for index, account in self._accounts.items():
            if index[0] == account_id.value:
                return account

        raise AccountNotFoundException()

    async def get_by_email(self, email: EmailAddress) -> Account:
        for index, account in self._accounts.items():
            if index[1] == email.value:
                return account

        raise AccountNotFoundException()

    async def update(self, account: Account) -> None:
        indexes = (account.id.value, account.email.address.value)

        if indexes in self._accounts:
            self._accounts[indexes] = account

        else:
            raise AccountNotFoundException()
