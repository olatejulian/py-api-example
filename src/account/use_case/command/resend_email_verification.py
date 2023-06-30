from src.account.domain import AccountRepository, EmailAddress
from src.shared import Command, CommandHandler

from ..service import AccountEmailVerificationSender


class ResendVerificationEmail(Command):
    def __init__(self, email: EmailAddress):
        self.email = email


class ResendVerificationEmailHandler(CommandHandler):
    def __init__(
        self,
        repository: AccountRepository,
        email_verification_sender: AccountEmailVerificationSender,
    ):
        self.repository = repository
        self.email_verification_sender = email_verification_sender

    async def handle(self, command: ResendVerificationEmail) -> None:
        account = await self.repository.get_by_email(command.email)
        if not account.is_email_verified():
            verification_code = (
                account.email.verification_code
                if account.email.verification_code
                else account.generate_verification_code()
            )

            await self.email_verification_sender.execute(
                account.name, account.email.address, verification_code
            )
