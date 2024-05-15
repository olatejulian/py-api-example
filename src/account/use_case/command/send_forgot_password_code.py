from src.account.domain import AccountRepository, EmailAddress
from src.shared import Command, CommandHandler


class SendForgotPasswordCode(Command):
    def __init__(self, email: EmailAddress):
        self.email = email


class SendForgotPasswordCodeHandler(CommandHandler):
    def __init__(self, repository: AccountRepository, forgot_password_email_sender):
        self.repository = repository
        self.forgot_password_email_sender = forgot_password_email_sender

    async def handle(self, command: SendForgotPasswordCode) -> None:
        account = await self.repository.get_by_email(command.email)
        if account.is_email_verified():
            code = account.generate_reset_password_code()

            await self.repository.update(account)

            await self.forgot_password_email_sender.send(
                account.name,
                account.email.address,
                code,
            )
