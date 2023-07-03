# pylint: disable=c-extension-no-member
from dependency_injector import containers, providers

from .infra import (
    AioSmtpAccountEmailSender,
    BeanieAccountRepository,
    DefaultAccountVerificationEmailSender,
    EmailSenderConfig,
    EmailTemplateRendererConfig,
    Jinja2AccountEmailTemplateRenderer,
    VerificationEmailSenderConfig,
)
from .use_case import (
    CreateAccountHandler,
    ResendVerificationEmailHandler,
    SendVerificationEmailHandler,
    VerifyAccountEmailHandler,
)


class AccountContainer(containers.DeclarativeContainer):
    session = providers.Dependency()

    # config
    verification_email_sender_config = providers.Singleton(
        VerificationEmailSenderConfig
    )

    email_template_renderer_config = providers.Singleton(EmailTemplateRendererConfig)

    email_sender_config = providers.Singleton(EmailSenderConfig)

    # infra
    account_repository = providers.Singleton(
        BeanieAccountRepository,
        session=session,
    )

    account_email_template_renderer = providers.Singleton(
        Jinja2AccountEmailTemplateRenderer,
        config=email_template_renderer_config,
    )

    account_email_sender = providers.Singleton(
        AioSmtpAccountEmailSender,
        config=email_sender_config,
    )

    # use_case
    # service
    account_verification_email_sender = providers.Singleton(
        DefaultAccountVerificationEmailSender,
        config=verification_email_sender_config,
        email_template_renderer=account_email_template_renderer,
        email_sender=account_email_sender,
    )

    # command
    create_account_command_handler = providers.Singleton(
        CreateAccountHandler,
        repository=account_repository,
    )

    resend_verification_email_command_handler = providers.Singleton(
        ResendVerificationEmailHandler,
        repository=account_repository,
        verification_email_sender=account_verification_email_sender,
    )

    verify_account_email_command_handler = providers.Singleton(
        VerifyAccountEmailHandler,
        repository=account_repository,
    )

    # event
    send_verification_email_event_handler = providers.Singleton(
        SendVerificationEmailHandler,
        repository=account_repository,
        verification_email_sender=account_verification_email_sender,
    )
