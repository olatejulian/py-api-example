import pytest

from src.core.account.domain import Account, AccountRepository


@pytest.mark.asyncio
async def test_account_repository_save_method(
    account_repository: AccountRepository, random_account_fixture: Account
):
    """
    should be able to save an account
    """
    # given
    entity = random_account_fixture

    repository = account_repository

    # when
    account_saved = await repository.save(entity)

    # then
    assert account_saved.id == entity.id
    assert account_saved.email.address == entity.email.address
