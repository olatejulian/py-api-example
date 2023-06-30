# pylint: disable=redefined-outer-name
from typing import AsyncGenerator
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from src.account import (
    Account,
    AccountEmailTemplateRender,
    AccountInputDto,
    AccountRepository,
    BeanieAccountModel,
    BeanieAccountRepository,
    EmailAddress,
    InMemoryAccountRepository,
    Jinja2AccountEmailTemplateRender,
    Name,
    Password,
)
from src.app import celery_event_bus_factory, database_factory, fastapi_bootstrap
from src.shared import (
    Database,
    DatabaseConfig,
    EmailTemplateConfig,
    EventBus,
    FakeEventBus,
)


@pytest.fixture
def random_account_fixture():
    return Account.create(
        AccountInputDto(
            name=Name(f"{uuid4()}"),
            email=EmailAddress(f"{uuid4()}@{uuid4()}.com"),
            password=Password(f"{uuid4()}"),
        )
    )


@pytest_asyncio.fixture()
async def database_fixture() -> AsyncGenerator[Database, None]:
    config = DatabaseConfig()

    config.name = "test-py-api-example"

    database = Database(
        config=config,
        models=[BeanieAccountModel],
    )

    await database.connect()

    yield database

    await BeanieAccountModel.delete_all(database.session)


@pytest.fixture
def account_repository(
    database_fixture: Database,  # pylint: disable=redefined-outer-name
) -> AccountRepository:
    database = database_fixture

    repository = BeanieAccountRepository(database.session)

    return repository


@pytest.fixture
def fake_account_repository() -> AccountRepository:
    return InMemoryAccountRepository()


@pytest.fixture
def account_email_template_render() -> AccountEmailTemplateRender:
    return Jinja2AccountEmailTemplateRender(EmailTemplateConfig())


@pytest.fixture
def event_bus_fixture() -> EventBus:
    return FakeEventBus()


@pytest.fixture
def app(database_fixture: Database, event_bus_fixture: EventBus) -> FastAPI:
    app = fastapi_bootstrap()

    def override_database_dependency() -> Database:
        return database_fixture

    def override_event_bus_dependency() -> EventBus:
        return event_bus_fixture

    app.dependency_overrides[database_factory] = override_database_dependency

    app.dependency_overrides[celery_event_bus_factory] = override_event_bus_dependency

    return app


@pytest.fixture
def async_client(app: FastAPI):
    return AsyncClient(app=app, base_url="http://localhost:3000")
