# pylint: disable=redefined-outer-name
from typing import AsyncGenerator
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from src.account import (
    Account,
    AccountAuthenticator,
    AccountEmailSender,
    AccountEmailTemplateRenderer,
    AccountInputDto,
    AccountRepository,
    AuthConfig,
    BeanieAccountModel,
    BeanieAccountRepository,
    EmailAddress,
    EmailTemplateRendererConfig,
    FakeAccountEmailSender,
    FakeAccountRepository,
    Jinja2AccountEmailTemplateRenderer,
    JoseAccountAuthenticator,
    Name,
    Password,
)
from src.app import (
    AppContainer,
    BeanieMongoDatabase,
    BeanieMongoDatabaseConfig,
    bootstrap,
    init_database,
)


@pytest.fixture
def create_random_account():
    return Account.create(
        AccountInputDto(
            name=Name(f"{uuid4()}"),
            email=EmailAddress(f"{uuid4()}@{uuid4()}.com"),
            password=Password(f"{uuid4()}"),
        )
    )


@pytest_asyncio.fixture()
async def database() -> AsyncGenerator[BeanieMongoDatabase, None]:
    config = BeanieMongoDatabaseConfig()

    config.name = "test-py-api-example"

    database_ = await init_database(config)

    yield database_

    await BeanieAccountModel.delete_all(database_.session)


@pytest.fixture
def account_repository(
    database: BeanieMongoDatabase,  # pylint: disable=redefined-outer-name
) -> AccountRepository:
    repository = BeanieAccountRepository(database.session)

    return repository


@pytest.fixture()
def account_authenticator(
    fake_account_repository: AccountRepository,
) -> AccountAuthenticator:
    config = AuthConfig()

    repository = fake_account_repository

    return JoseAccountAuthenticator(config, repository)


@pytest.fixture
def account_email_template_renderer() -> AccountEmailTemplateRenderer:
    return Jinja2AccountEmailTemplateRenderer(EmailTemplateRendererConfig())


@pytest.fixture
def fake_account_repository() -> AccountRepository:
    return FakeAccountRepository()


@pytest.fixture
def fake_account_email_sender() -> AccountEmailSender:
    return FakeAccountEmailSender()


@pytest.fixture
def app(
    database: BeanieMongoDatabase, fake_account_email_sender: AccountEmailSender
) -> FastAPI:
    container = AppContainer()

    container.database.override(database)
    container.account_container.account_email_sender.override(fake_account_email_sender)

    app = bootstrap(container)

    return app


@pytest.fixture
def async_client(app: FastAPI):
    return AsyncClient(app=app, base_url="http://localhost:3000")
