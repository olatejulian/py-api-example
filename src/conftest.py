from typing import AsyncGenerator
from uuid import uuid4

import pytest
import pytest_asyncio

from src.core.account import BeanieAccountModel
from src.core.account.domain import (
    Account,
    AccountEmailTemplateRender,
    AccountInputDto,
    AccountRepository,
    EmailAddress,
    Name,
    Password,
)
from src.core.account.infra import (
    BeanieAccountRepository,
    InMemoryAccountRepository,
    Jinja2AccountEmailTemplateRender,
)
from src.core.shared import Database, EmailTemplateConfig, EventBus, FakeEventBus


@pytest.fixture
def random_account_fixture():
    return Account.create(
        AccountInputDto(
            name=Name(f"{uuid4()}"),
            email=EmailAddress(f"{uuid4()}@{uuid4()}.com"),
            password=Password(f"{uuid4()}"),
        )
    )


@pytest_asyncio.fixture
async def account_repository(
    database_fixture: Database,  # pylint: disable=redefined-outer-name
) -> AsyncGenerator[AccountRepository, None]:
    database = database_fixture

    session = database.session

    repository = BeanieAccountRepository(session)

    yield repository

    await BeanieAccountModel.delete_all(session)


@pytest.fixture
def fake_account_repository() -> AccountRepository:
    return InMemoryAccountRepository()


@pytest.fixture
def account_email_template_render() -> AccountEmailTemplateRender:
    return Jinja2AccountEmailTemplateRender(EmailTemplateConfig())


@pytest_asyncio.fixture()
async def database_fixture():
    database = Database(
        uri="mongodb://mongo:mongo@localhost:27017",
        db_name="test-py-api-example",
        models=[BeanieAccountModel],
    )

    await database.connect()

    return database


@pytest.fixture
def event_bus_fixture() -> EventBus:
    return FakeEventBus()
