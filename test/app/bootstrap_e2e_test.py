import pytest
from httpx import AsyncClient

from src.account import Account, AccountRepository
from src.app import signup_response_message, verify_email_response_message


@pytest.mark.asyncio
async def test_signup(async_client: AsyncClient):
    # given
    request_body = {
        "name": "John Doe",
        "email": "john.doe@email.com",
        "password": "JohnDoePassword",
    }

    # when
    async with async_client as client:
        response = await client.post("/signup", json=request_body)

        # then
        assert response.status_code == 200

        response_body = response.json()

        assert response_body["status_code"] == 200

        assert response_body["message"] == signup_response_message(
            request_body["email"]
        )  # pylint: disable=line-too-long

        assert response_body["data"]["email"] == request_body["email"]


@pytest.mark.asyncio
async def test_verify_email(
    random_account_fixture: Account,
    account_repository: AccountRepository,
    async_client: AsyncClient,
):
    """
    should be able to verify an email using query params (email to be verified and it token)
    """
    # given
    entity = random_account_fixture

    repository = account_repository

    verification_code = entity.generate_verification_code()

    query_params = {
        "email": entity.email.address.value,
        "token": verification_code.value,
    }

    # when
    async with async_client as client:
        await repository.save(entity)

        response = await client.post("/verify", params=query_params)

        # then
        assert response.status_code == 200

        response_body = response.json()

        assert response_body["status_code"] == 200

        assert response_body["message"] == verify_email_response_message()

        assert response_body["data"] == {}
