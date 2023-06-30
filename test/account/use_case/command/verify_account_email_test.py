import pytest

from src.account import (
    Account,
    AccountRepository,
    VerifyAccountEmail,
    VerifyAccountEmailHandler,
)


@pytest.mark.asyncio
async def test_verify_account(
    random_account_fixture: Account, fake_account_repository: AccountRepository
):
    """
    should be able to verify  and if is not activate, activate it an account when the token is valid
    """
    # given
    account = random_account_fixture

    repository = fake_account_repository

    await repository.save(account)

    token = account.generate_verification_code()

    command = VerifyAccountEmail(email=account.email.address, token=token)

    handler = VerifyAccountEmailHandler(repository)

    # when
    await handler.handle(command)

    # then
    account = await repository.get_by_email(account.email.address)

    assert account.is_email_verified() is True

    assert account.is_active() is True
