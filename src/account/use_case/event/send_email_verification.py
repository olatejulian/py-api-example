from src.account.domain import AccountCreated, AccountRepository
from src.shared import EventHandler

from ..service import AccountEmailVerificationSender


class SendEmailVerificationHandler(EventHandler[AccountCreated]):
    def __init__(
        self,
        repository: AccountRepository,
        email_verification_sender: AccountEmailVerificationSender,
    ):
        self.repository = repository
        self.email_verification_sender = email_verification_sender

    async def handle(self, event: AccountCreated) -> None:
        account = await self.repository.get_by_id(event.account_id)

        account_name = account.name
        account_email_address = account.email.address
        verification_code = account.generate_verification_code()

        await self.repository.update(account)

        await self.email_verification_sender.execute(
            account_name,
            account_email_address,
            verification_code,
        )
