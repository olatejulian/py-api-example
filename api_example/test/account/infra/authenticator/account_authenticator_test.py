import pytest

from src.account import (
    Account,
    AccountAuthenticator,
    AccountRepository,
    InvalidAccessTokenException,
    Password,
)


@pytest.mark.asyncio
async def test_authenticate_with_valid_email_and_password(
    create_random_account: Account,
    fake_account_repository: AccountRepository,
    account_authenticator: AccountAuthenticator,
):
    """
    Should be able to return an access token when the email and password are valid
    """
    # given
    entity = create_random_account

    plain_password = "123456"

    password = Password(plain_password)

    entity.password.password = password

    repository = fake_account_repository

    authenticator = account_authenticator

    await repository.save(entity)

    # when
    result = await authenticator.authenticate(entity.email.address, plain_password)

    # then
    assert result.access_token is not None
    assert result.token_type == "bearer"


@pytest.mark.asyncio
async def test_authenticate_when_email_does_not_exist(
    create_random_account: Account,
    account_authenticator: AccountAuthenticator,
):
    """
    Should be able to raise an exception when the email does not exist
    """
    # given
    entity = create_random_account

    plain_password = "123456"

    password = Password(plain_password)

    entity.password.password = password

    authenticator = account_authenticator

    # when / then
    with pytest.raises(InvalidAccessTokenException):
        await authenticator.authenticate(entity.email.address, plain_password)


@pytest.mark.asyncio
async def test_authenticate_when_password_is_wrong(
    create_random_account: Account,
    fake_account_repository: AccountRepository,
    account_authenticator: AccountAuthenticator,
):
    """
    Should be able to raise an exception when the email does not exist
    """
    # given
    entity = create_random_account

    plain_password = "123456"

    password = Password(plain_password)

    entity.password.password = password

    repository = fake_account_repository

    await repository.save(entity)

    authenticator = account_authenticator

    # when / then
    with pytest.raises(InvalidAccessTokenException):
        await authenticator.authenticate(entity.email.address, plain_password + "A")


# @pytest.mark.asyncio
# async def test_authenticate_when_time_expired(
#     create_random_account: Account,
#     fake_account_repository: AccountRepository,
#     account_authenticator: AccountAuthenticator,
# ):
#     """
#     Should be able to raise an exception when jwt code is expired
#     """
#     # given
#     entity = create_random_account

#     plain_password = "123456"

#     password = Password(plain_password)

#     entity.password.password = password

#     repository = fake_account_repository

#     await repository.save(entity)

#     authenticator = account_authenticator

#     access_token_dto = await authenticator.authenticate(
#         entity.email.address, plain_password
#     )

#     # when / then
#     with pytest.raises(InvalidAccessTokenException):
#         await authenticator.get_current_account(access_token_dto.access_token)


@pytest.mark.asyncio
async def test_get_current_account_with_valid_token(
    create_random_account: Account,
    fake_account_repository: AccountRepository,
    account_authenticator: AccountAuthenticator,
):
    """
    should be able to return the account when the token is valid
    """
    # given
    entity = create_random_account

    plain_password = "123456"

    password = Password(plain_password)

    entity.password.password = password

    repository = fake_account_repository

    await repository.save(entity)

    authenticator = account_authenticator

    access_token_dto = await authenticator.authenticate(
        entity.email.address, plain_password
    )

    # when
    entity_got = await authenticator.get_current_account(access_token_dto.access_token)

    # then
    assert entity_got.id == entity.id
    assert entity_got.name == entity.name
    assert entity_got.email.address == entity.email.address
