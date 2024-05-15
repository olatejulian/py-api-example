from email.message import EmailMessage

from aiosmtplib import SMTP

from src.account.domain import (
    AccountEmailSender,
    EmailAddress,
    EmailContent,
    EmailSubject,
)
from src.shared import Config


class CannotSendEmailException(Exception):
    pass


class EmailSenderConfig(Config):
    def __init__(self):
        super().__init__()

        self.smtp_host = self._get("EMAIL_SMTP_HOST")
        self.smtp_port = int(self._get("EMAIL_SMTP_PORT"))
        self.username = self._get("EMAIL_USERNAME")
        self.password = self._get("EMAIL_PASSWORD")
        self.sender = self._get("EMAIL_SENDER_ADDRESS")


class AioSmtpAccountEmailSender(AccountEmailSender):
    def __init__(
        self,
        config: EmailSenderConfig,
    ):
        self.config = config

    async def send(
        self,
        recipient: EmailAddress,
        subject: EmailSubject,
        html_content: EmailContent,
        plaintext_content: EmailContent,
    ) -> None:
        email_message = EmailMessage()

        email_message["From"] = self.config.sender
        email_message["To"] = recipient.value
        email_message["Subject"] = subject.value

        email_message.set_content(plaintext_content.value)

        email_message.add_alternative(html_content.value, subtype="html")

        try:
            async with SMTP(
                hostname=self.config.smtp_host, port=self.config.smtp_port
            ) as smtp:
                await smtp.connect()
                await smtp.login(self.config.username, self.config.password)

                await smtp.send_message(email_message)

        except Exception as exc:
            raise CannotSendEmailException(exc.args) from exc
