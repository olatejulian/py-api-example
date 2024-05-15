# pylint: disable=c-extension-no-member
from dependency_injector import containers, providers

from ..account import (
    AccountContainer,
    AccountCreated,
    CreateAccount,
    GetAccessToken,
    ResendVerificationEmail,
    VerifyAccountEmail,
)
from .infra import (
    BeanieMongoDatabaseConfig,
    DefaultCommandBus,
    DefaultEventBus,
    DefaultQueryBus,
    init_database,
)


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".presentation"])

    database_config = providers.Singleton(BeanieMongoDatabaseConfig)

    database = providers.Resource(init_database, config=database_config)

    account_container = providers.Container(
        AccountContainer,
        session=database.provided.session,
    )

    command_bus = providers.Singleton(
        DefaultCommandBus,
        handlers=providers.Dict(
            {
                CreateAccount: account_container.create_account_command_handler,
                VerifyAccountEmail: account_container.verify_account_email_command_handler,
                ResendVerificationEmail: account_container.resend_verification_email_command_handler,  # pylint: disable=line-too-long
            }
        ),
    )

    event_bus = providers.Singleton(
        DefaultEventBus,
        handlers=providers.Dict(
            {
                AccountCreated: providers.List(
                    account_container.send_verification_email_event_handler
                ),
            }
        ),
    )

    query_bus = providers.Singleton(
        DefaultQueryBus,
        handlers=providers.Dict(
            {
                GetAccessToken: account_container.get_access_token_query_handler,
            }
        ),
    )
