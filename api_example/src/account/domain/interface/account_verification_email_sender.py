from abc import ABC, abstractmethod

from src.account.domain import EmailAddress, Name, VerificationCode


class AccountVerificationEmailSender(ABC):
    @abstractmethod
    async def send_verification_email(
        self,
        account_name: Name,
        account_email_address: EmailAddress,
        verification_code: VerificationCode,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def send_password_reset_email(
        self,
        account_name: Name,
        account_email_address: EmailAddress,
        password_reset_code: VerificationCode,
    ):
        raise NotImplementedError
