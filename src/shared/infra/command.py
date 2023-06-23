from ..interface import (
    Command,
    CommandBus,
    CommandDoesNotHaveHandlerException,
    CommandHandler,
)


class DefaultCommandBus(CommandBus):
    def __init__(self) -> None:
        self.__handlers: dict[type[Command], CommandHandler] = {}

    def register(
        self,
        command_class: type[Command],
        handler: CommandHandler,
    ) -> None:
        self.__handlers[command_class] = handler

    def register_many(
        self, commands_and_handlers: dict[type[Command], CommandHandler]
    ) -> None:
        self.__handlers.update(commands_and_handlers)

    async def dispatch(self, command: Command) -> None:
        command_class = type(command)

        if command_class not in self.__handlers:
            raise CommandDoesNotHaveHandlerException()

        handler = self.__handlers[command_class]

        await handler.handle(command)
