from fastapi import Depends

from src.core.account import (
    AccountCreated,
    AccountEmailSender,
    AccountEmailTemplateRender,
    AccountRepository,
    AioSmtpAccountEmailSender,
    BeanieAccountModel,
    BeanieAccountRepository,
    CreateAccount,
    CreateAccountHandler,
    EmailAddress,
    FakeAccountEmailSender,
    InMemoryAccountRepository,
    Jinja2AccountEmailTemplateRender,
    SendEmailVerification,
)
from src.core.shared import (
    AppConfig,
    AsyncioEventBus,
    CeleryEventBus,
    CommandBus,
    Database,
    DatabaseConfig,
    DefaultCommandBus,
    EmailConfig,
    EmailTemplateConfig,
    EventBus,
    FakeEventBus,
)


def app_config_factory() -> AppConfig:
    return AppConfig()


def account_email_template_render_config_factory() -> EmailTemplateConfig:
    return EmailTemplateConfig()


def account_email_config_factory() -> EmailConfig:
    return EmailConfig()


def database_config_factory() -> DatabaseConfig:
    return DatabaseConfig()


def database_factory(
    config: DatabaseConfig = Depends(database_config_factory),
) -> Database:
    return Database(uri=config.uri, db_name=config.name, models=[BeanieAccountModel])


def fake_account_repository_factory() -> AccountRepository:
    return InMemoryAccountRepository()


def beanie_account_repository_factory(
    database: Database = Depends(database_factory),
) -> AccountRepository:
    return BeanieAccountRepository(database.session)


def account_email_template_render_factory(
    config: EmailTemplateConfig = Depends(account_email_template_render_config_factory),
) -> AccountEmailTemplateRender:
    return Jinja2AccountEmailTemplateRender(config)


def account_email_sender_factory(
    config: EmailConfig = Depends(account_email_config_factory),
) -> AccountEmailSender:
    return AioSmtpAccountEmailSender(
        smtp_host=config.smtp_host,
        smtp_port=config.smtp_port,
        username=config.username,
        password=config.password,
        sender=EmailAddress(config.sender),
    )


def fake_account_email_sender_factory() -> AccountEmailSender:
    return FakeAccountEmailSender()


def asyncio_event_bus_factory(
    app_config: AppConfig = Depends(app_config_factory),
    account_repository: AccountRepository = Depends(fake_account_repository_factory),
    account_email_template_render: AccountEmailTemplateRender = Depends(
        account_email_template_render_factory
    ),
    account_email_sender: AccountEmailSender = Depends(account_email_sender_factory),
) -> EventBus:
    bus = AsyncioEventBus()

    bus.register_many(
        {
            AccountCreated: [
                SendEmailVerification(
                    app_config=app_config,
                    repository=account_repository,
                    email_sender=account_email_sender,
                    email_template_render=account_email_template_render,
                )
            ]
        }
    )

    return bus


def fake_event_bus_factory() -> EventBus:
    return FakeEventBus()


def celery_event_bus_factory(
    app_config: AppConfig = Depends(app_config_factory),
    account_repository: AccountRepository = Depends(fake_account_repository_factory),
    account_email_template_render: AccountEmailTemplateRender = Depends(
        account_email_template_render_factory
    ),
    account_email_sender: AccountEmailSender = Depends(account_email_sender_factory),
) -> EventBus:
    bus = CeleryEventBus()

    bus.register_many(
        {
            AccountCreated: [
                SendEmailVerification(
                    app_config=app_config,
                    repository=account_repository,
                    email_sender=account_email_sender,
                    email_template_render=account_email_template_render,
                )
            ]
        }
    )

    return bus


def command_bus_factory(
    repository: AccountRepository = Depends(fake_account_repository_factory),
    event_bus: EventBus = Depends(celery_event_bus_factory),
) -> CommandBus:
    bus = DefaultCommandBus()

    bus.register_many(
        {
            CreateAccount: CreateAccountHandler(repository, event_bus),
        }
    )

    return bus
