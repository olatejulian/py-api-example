import pytest

from src.account import (
    AccountRepository,
    CreateAccount,
    CreateAccountHandler,
    EmailAddress,
    Name,
    Password,
)
from src.shared import EventBus


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
    handler_response = await handler.handle(command)

    # then
    assert handler_response.email == command.email
