# pylint: disable=c-extension-no-member
from dependency_injector import containers, providers

from .infra import (
    AioSmtpAccountEmailSender,
    AuthConfig,
    BeanieAccountRepository,
    DefaultAccountVerificationEmailSender,
    EmailSenderConfig,
    EmailTemplateRendererConfig,
    Jinja2AccountEmailTemplateRenderer,
    JoseAccountAuthenticator,
    VerificationEmailSenderConfig,
)
from .use_case import (
    CreateAccountHandler,
    GetAccessTokenHandler,
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

    auth_config = providers.Singleton(AuthConfig)

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

    account_verification_email_sender = providers.Singleton(
        DefaultAccountVerificationEmailSender,
        config=verification_email_sender_config,
        email_template_renderer=account_email_template_renderer,
        email_sender=account_email_sender,
    )

    account_authenticator = providers.Singleton(
        JoseAccountAuthenticator, config=auth_config, repository=account_repository
    )

    # use_case
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

    # query
    get_access_token_query_handler = providers.Singleton(
        GetAccessTokenHandler, authenticator=account_authenticator
    )
