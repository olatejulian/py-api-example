from fastapi import Depends

from src.account import (
    AccountCreated,
    AccountEmailSender,
    AccountEmailTemplateRender,
    AccountEmailVerificationSender,
    AccountRepository,
    AioSmtpAccountEmailSender,
    BeanieAccountModel,
    BeanieAccountRepository,
    CreateAccount,
    CreateAccountHandler,
    EmailAddress,
    Jinja2AccountEmailTemplateRender,
    SendEmailVerificationHandler,
    VerifyAccountEmail,
    VerifyAccountEmailHandler,
)
from src.shared import (
    AppConfig,
    CeleryEventBus,
    CommandBus,
    Database,
    DatabaseConfig,
    DefaultCommandBus,
    EmailConfig,
    EmailTemplateConfig,
    EventBus,
)


def app_config_factory() -> AppConfig:
    return AppConfig()


def account_email_template_render_config_factory() -> EmailTemplateConfig:
    return EmailTemplateConfig()


def account_email_config_factory() -> EmailConfig:
    return EmailConfig()


def database_config_factory() -> DatabaseConfig:
    return DatabaseConfig()


async def database_factory(
    config: DatabaseConfig = Depends(database_config_factory),
) -> Database:
    database = Database(config, [BeanieAccountModel])

    await database.connect()

    return database


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


def account_verification_email_sender_factory(
    config: AppConfig = Depends(app_config_factory),
    email_sender: AccountEmailSender = Depends(account_email_sender_factory),
    email_template_renderer: AccountEmailTemplateRender = Depends(
        account_email_template_render_factory
    ),
) -> AccountEmailVerificationSender:
    return AccountEmailVerificationSender(config, email_template_renderer, email_sender)


def celery_event_bus_factory(
    account_repository: AccountRepository = Depends(beanie_account_repository_factory),
    account_email_verification_sender: AccountEmailVerificationSender = Depends(
        account_verification_email_sender_factory
    ),
) -> EventBus:
    bus = CeleryEventBus()

    bus.register_many(
        {
            AccountCreated: [
                SendEmailVerificationHandler(
                    account_repository,
                    account_email_verification_sender,
                )
            ]
        }
    )

    return bus


def command_bus_factory(
    repository: AccountRepository = Depends(beanie_account_repository_factory),
    event_bus: EventBus = Depends(celery_event_bus_factory),
) -> CommandBus:
    bus = DefaultCommandBus()

    bus.register_many(
        {
            CreateAccount: CreateAccountHandler(repository, event_bus),
            VerifyAccountEmail: VerifyAccountEmailHandler(repository),
        }
    )

    return bus
