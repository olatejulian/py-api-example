from src.account.domain import (
    AccountRepository,
    AccountVerificationEmailSender,
    EmailAddress,
)
from src.shared import Command, CommandHandler


class ResendVerificationEmail(Command):
    def __init__(self, email: EmailAddress):
        self.email = email


class ResendVerificationEmailHandler(CommandHandler):
    def __init__(
        self,
        repository: AccountRepository,
        verification_email_sender: AccountVerificationEmailSender,
    ):
        self.repository = repository
        self.verification_email_sender = verification_email_sender

    async def handle(self, command: ResendVerificationEmail) -> None:
        account = await self.repository.get_by_email(command.email)
        if not account.is_email_verified():
            verification_code = account.generate_verification_code()

            await self.repository.update(account)

            await self.verification_email_sender.send_verification_email(
                account.name, account.email.address, verification_code
            )
