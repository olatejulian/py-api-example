from abc import ABC, abstractmethod

from ..value_object import EmailAddress, EmailContent, EmailSubject


class AccountEmailSender(ABC):
    @abstractmethod
    async def send(
        self,
        recipient: EmailAddress,
        subject: EmailSubject,
        html_content: EmailContent,
        plaintext_content: EmailContent,
    ):
        raise NotImplementedError
