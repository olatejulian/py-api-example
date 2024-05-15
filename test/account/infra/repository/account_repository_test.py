import pytest

from src.account import (
    Account,
    AccountInputDto,
    AccountNotFoundException,
    AccountRepository,
    DuplicateIdOrEmailException,
    EmailAddress,
    Name,
)


@pytest.mark.asyncio
async def test_account_repository_save_method(
    account_repository: AccountRepository, create_random_account: Account
):
    """
    should be able to save an account
    """
    # given
    entity = create_random_account

    repository = account_repository

    # when
    result = await repository.save(entity)

    # then
    assert result is None


@pytest.mark.asyncio
async def test_account_repository_save_method_when_try_to_save_with_same_email(
    account_repository: AccountRepository, create_random_account: Account
):
    """
    should be able to raise an exception when trying to save an account with duplicated id or email
    """
    # given
    entity = create_random_account

    another_entity = Account.create(
        AccountInputDto(entity.name, entity.email.address, entity.password.password),
    )

    another_entity.email.address.value = entity.email.address.value

    repository = account_repository

    # when
    await repository.save(entity)

    with pytest.raises(DuplicateIdOrEmailException):
        await repository.save(another_entity)


@pytest.mark.asyncio
async def test_account_repository_get_by_id_method(
    account_repository: AccountRepository, create_random_account: Account
):
    """
    should be able to get an account by id
    """
    # given
    entity = create_random_account

    repository = account_repository

    await repository.save(entity)

    # when
    entity_found = await repository.get_by_id(entity.id)

    # then
    assert entity_found.id == entity.id
    assert entity_found.name == entity.name
    assert entity_found.email.address == entity.email.address


@pytest.mark.asyncio
async def test_account_repository_get_by_id_method_when_id_does_not_exist(
    account_repository: AccountRepository, create_random_account: Account
):
    """
    should be able to raises an exception when trying to get an account by id that does not exist
    """
    # given
    entity = create_random_account

    repository = account_repository

    # when / then
    with pytest.raises(AccountNotFoundException):
        await repository.get_by_id(entity.id)


@pytest.mark.asyncio
async def test_account_repository_update_method(
    account_repository: AccountRepository, create_random_account: Account
):
    """
    should be able to update an account
    """
    # given
    entity = create_random_account

    repository = account_repository

    await repository.save(entity)

    # when
    entity.change_name(Name("new_name"))
    entity.change_email(EmailAddress("new.email@email.com"))

    await repository.update(entity)
