from abc import ABC, abstractmethod

from src.account.domain import EmailAddress, Name, VerificationCode


class AccountVerificationEmailSender(ABC):
    @abstractmethod
    async def send(
        self,
        account_name: Name,
        account_email_address: EmailAddress,
        verification_code: VerificationCode,
    ) -> None:
        raise NotImplementedError
