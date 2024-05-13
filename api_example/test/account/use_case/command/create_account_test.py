import pytest

from src.account import (
    AccountRepository,
    CreateAccount,
    CreateAccountHandler,
    EmailAddress,
    Name,
    Password,
)


@pytest.mark.asyncio
async def test_create_account_command_handler(
    fake_account_repository: AccountRepository,
):
    """
    should be able to create an account
    """
    # given
    repository = fake_account_repository

    password = "any password"

    command = CreateAccount(
        name=Name("any name"),
        email=EmailAddress("john.doe@email.com"),
        password=Password(password),
    )

    handler = CreateAccountHandler(repository)

    # when
    entity = await handler.handle(command)

    # then
    assert entity is not None
    assert entity.id is not None
    assert entity.name == command.name
    assert entity.email.address == command.email
    assert entity.password.password == password
