from src.account.domain import AccountRepository, EmailAddress
from src.shared import Command, CommandHandler

from ..service import AccountEmailVerificationSender


class ResendEmailVerification(Command):
    email: EmailAddress


class ResendEmailVerificationHandler(CommandHandler):
    def __init__(
        self,
        repository: AccountRepository,
        email_verification_sender: AccountEmailVerificationSender,
    ):
        self.repository = repository
        self.email_verification_sender = email_verification_sender

    async def handle(self, command: ResendEmailVerification) -> None:
        account = await self.repository.get_by_email(command.email)
        if not account.is_email_verified():
            if not account.email.verification_code:
                account.generate_verification_code()

            await self.email_verification_sender.execute(
                account.name, account.email.address, account.email.verification_code
            )