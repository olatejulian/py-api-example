import pytest

from src.core.account.domain import AccountRepository, EmailAddress, Name, Password
from src.core.shared import EventBus

from .create_account import CreateAccount, CreateAccountHandler


@pytest.mark.asyncio
async def test_create_account_command_handler(
    fake_account_repository: AccountRepository, event_bus_fixture: EventBus
):
    """
    should be able to create an account
    """
    # given
    repository = fake_account_repository
    event_bus = event_bus_fixture

    command = CreateAccount(
        name=Name("any name"),
        email=EmailAddress("john.doe@email.com"),
        password=Password("any password"),
    )

    handler = CreateAccountHandler(repository, event_bus)

    # when
    await handler.handle(command)
