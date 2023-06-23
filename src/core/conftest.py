from uuid import uuid4

import pytest

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
    InMemoryAccountRepository,
    Jinja2AccountEmailTemplateRender,
)
from src.core.shared import EmailTemplateConfig, EventBus, FakeEventBus


@pytest.fixture
def random_account_fixture():
    return Account.create(
        AccountInputDto(
            name=Name(f"{uuid4()}"),
            email=EmailAddress(f"{uuid4()}@{uuid4()}.com"),
            password=Password(f"{uuid4()}"),
        )
    )


@pytest.fixture
def account_repository() -> AccountRepository:
    return InMemoryAccountRepository()


@pytest.fixture
def account_email_template_render() -> AccountEmailTemplateRender:
    return Jinja2AccountEmailTemplateRender(EmailTemplateConfig())


@pytest.fixture
def event_bus_fixture() -> EventBus:
    return FakeEventBus()
