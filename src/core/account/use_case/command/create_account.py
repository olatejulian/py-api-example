from src.core.account.domain import Account, AccountInputDto, AccountRepository
from src.core.shared import Command, CommandHandler, EventBus


class CreateAccount(Command, AccountInputDto):
    pass


class CreateAccountHandler(CommandHandler[CreateAccount]):
    def __init__(self, repository: AccountRepository, event_bus: EventBus):
        self.repository = repository
        self.event_bus = event_bus

    async def handle(self, command: CreateAccount) -> None:
        account = Account.create(command)

        await self.repository.save(account)

        events = account.collect_events()

        for event in events:
            await self.event_bus.dispatch(event)
