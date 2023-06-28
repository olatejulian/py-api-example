from src.account.domain import Account, AccountInputDto, AccountRepository, EmailAddress
from src.shared import Command, CommandHandler, EventBus


class CreateAccount(Command, AccountInputDto):
    pass


class CreateAccountHandlerResponse:
    def __init__(self, email: EmailAddress):
        self.email = email


class CreateAccountHandler(CommandHandler):
    def __init__(self, repository: AccountRepository, event_bus: EventBus):
        self.repository = repository
        self.event_bus = event_bus

    async def handle(self, command: CreateAccount) -> CreateAccountHandlerResponse:
        account = Account.create(command)

        await self.repository.save(account)

        events = account.collect_events()

        for event in events:
            await self.event_bus.dispatch(event)

        return CreateAccountHandlerResponse(email=account.email.address)
