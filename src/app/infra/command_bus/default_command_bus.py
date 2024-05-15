from src.app.domain import (
    CommandBus,
    CommandDoesNotHaveHandlerException,
    CommandHandlerResponseType,
    CommandType,
)


class DefaultCommandBus(CommandBus[CommandType, CommandHandlerResponseType]):
    async def dispatch(self, command: CommandType) -> CommandHandlerResponseType:
        if handler := self.handlers.get(type(command), None):
            return await handler.handle(command)

        raise CommandDoesNotHaveHandlerException(type(command))
