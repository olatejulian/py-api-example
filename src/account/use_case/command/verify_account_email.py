from src.account.domain import AccountRepository, EmailAddress, VerificationCode
from src.shared import Command, CommandHandler


class VerifyAccountEmail(Command):
    def __init__(self, email: EmailAddress, token: VerificationCode):
        self.email = email
        self.token = token


class VerifyAccountEmailHandler(CommandHandler):
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    async def handle(self, command: VerifyAccountEmail) -> None:
        account = await self.repository.get_by_email(command.email)

        account.verify_email(command.token)

        account.activate()

        await self.repository.update(account)
