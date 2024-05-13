from src.account.domain import (
    AccountCreated,
    AccountRepository,
    AccountVerificationEmailSender,
)
from src.shared import EventHandler


class SendVerificationEmailHandler(EventHandler):
    def __init__(
        self,
        repository: AccountRepository,
        verification_email_sender: AccountVerificationEmailSender,
    ):
        self.repository = repository
        self.verification_email_sender = verification_email_sender

    async def handle(self, event: AccountCreated) -> None:
        account = await self.repository.get_by_id(event.account_id)

        account_name = account.name
        account_email_address = account.email.address
        verification_code = account.generate_verification_code()

        await self.repository.update(account)

        await self.verification_email_sender.send_verification_email(
            account_name,
            account_email_address,
            verification_code,
        )
