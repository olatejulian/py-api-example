import pytest
from httpx import AsyncClient

from src.account import Account, AccountRepository, EmailAddress
from src.app import (
    LOGIN_RESPONSE_MESSAGE,
    RESEND_VERIFICATION_EMAIL_RESPONSE_MESSAGE,
    SIGNUP_RESPONSE_MESSAGE,
    VERIFY_EMAIL_RESPONSE_MESSAGE,
)


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

        assert (
            response_body["message"] == SIGNUP_RESPONSE_MESSAGE
        )  # pylint: disable=line-too-long

        assert response_body["data"]["email"] == request_body["email"]


@pytest.mark.asyncio
async def test_resend_verification_email(
    create_random_account: Account,
    account_repository: AccountRepository,
    async_client: AsyncClient,
):
    """
    should be able to resend a verification email
    """
    # given
    entity = create_random_account

    repository = account_repository

    request_body = {
        "email": entity.email.address.value,
    }

    await repository.save(entity)

    # when
    async with async_client as client:
        response = await client.post("/verify", json=request_body)

        # then
        assert response.status_code == 202

        response_body = response.json()

        assert response_body["status_code"] == 200

        assert response_body["message"] == RESEND_VERIFICATION_EMAIL_RESPONSE_MESSAGE


@pytest.mark.asyncio
async def test_verify_email(
    create_random_account: Account,
    account_repository: AccountRepository,
    async_client: AsyncClient,
):
    """
    should be able to verify an email using query params (email to be verified and it token)
    """
    # given
    entity = create_random_account

    repository = account_repository

    verification_code = entity.generate_verification_code()

    query_params = {
        "email": entity.email.address.value,
        "token": verification_code.value,
    }

    # when
    async with async_client as client:
        await repository.save(entity)

        response = await client.get("/verify", params=query_params)

        # then
        assert response.status_code == 200

        response_body = response.json()

        assert response_body["status_code"] == 200

        assert response_body["message"] == VERIFY_EMAIL_RESPONSE_MESSAGE

        assert response_body["data"] == {}


@pytest.mark.asyncio
async def test_login(
    account_repository: AccountRepository,
    async_client: AsyncClient,
):
    """
    should be able to login
    """
    # given
    name = "John Doe"
    email = "john.doe@email.com"
    plain_password = "JohnDoePassword"

    signup_request_body = {
        "name": name,
        "email": email,
        "password": plain_password,
    }

    async with async_client as client:
        signup_response = await client.post("/signup", json=signup_request_body)

        assert signup_response.status_code == 200

        account = await account_repository.get_by_email(EmailAddress(email))

        verification_code = (
            account.email.verification_code.value
            if account.email.verification_code
            else None
        )

        verify_query_params = {
            "email": email,
            "token": verification_code,
        }

        verify_email_response = await client.get("/verify", params=verify_query_params)

        assert verify_email_response.status_code == 200

        login_request_body = {
            "username": email,
            "password": plain_password,
        }

        # when
        response = await client.post(
            "/login",
            data=login_request_body,
        )

        # then
        assert response.status_code == 200

        response_body = response.json()

        assert response_body["status_code"] == 200

        assert response_body["message"] == LOGIN_RESPONSE_MESSAGE

        assert response_body["data"]["access_token"] is not None

        assert response_body["data"]["token_type"] == "bearer"
