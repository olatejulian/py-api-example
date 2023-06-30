import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.account import Account, AccountRepository
from src.app import (
    beanie_account_repository_factory,
    celery_event_bus_factory,
    database_config_factory,
    fake_event_bus_factory,
    fastapi_bootstrap,
    signup_response_message,
    verify_email_response_message,
)
from src.shared import DatabaseConfig


def override_database_config_factory() -> DatabaseConfig:
    config = DatabaseConfig()

    config.name = "test-py-api-example"

    return config


app = fastapi_bootstrap()

app.dependency_overrides[database_config_factory] = override_database_config_factory

app.dependency_overrides[celery_event_bus_factory] = fake_event_bus_factory


client = TestClient(app)


def test_signup():
    # given
    request_body = {
        "name": "John Doe",
        "email": "john.doe@email.com",
        "password": "JohnDoePassword",
    }

    # when
    response = client.post("/signup", json=request_body)

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
    random_account_fixture: Account, account_repository: AccountRepository
):
    """
    should be able to verify an email using query params (email to be verified and it token)
    """
    # given
    entity = random_account_fixture

    repository = account_repository

    def override_account_repository_factory() -> AccountRepository:
        return repository

    app.dependency_overrides[
        beanie_account_repository_factory
    ] = override_account_repository_factory

    verification_code = entity.generate_verification_code()

    query_params = {
        "email": entity.email.address.value,
        "token": verification_code.value,
    }

    # when
    async with AsyncClient(app=app, base_url="http://localhost:3000") as async_client:
        await repository.save(entity)

        response = await async_client.post("/verify", params=query_params)

        # then
        assert response.status_code == 200

        response_body = response.json()

        assert response_body["status_code"] == 200

        assert response_body["message"] == verify_email_response_message()

        assert response_body["data"] == {}
