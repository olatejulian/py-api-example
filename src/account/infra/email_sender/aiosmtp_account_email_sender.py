from email.message import EmailMessage

from aiosmtplib import SMTP

from src.account.domain import (
    AccountEmailSender,
    EmailAddress,
    EmailContent,
    EmailSubject,
)


class CannotSendEmailException(Exception):
    pass


class AioSmtpAccountEmailSender(AccountEmailSender):
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        sender: EmailAddress,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.sender = sender

    async def send(
        self,
        recipient: EmailAddress,
        subject: EmailSubject,
        html_content: EmailContent,
        plaintext_content: EmailContent,
    ) -> None:
        email_message = EmailMessage()

        email_message["From"] = self.sender.value
        email_message["To"] = recipient.value
        email_message["Subject"] = subject.value

        email_message.set_content(plaintext_content.value)

        email_message.add_alternative(html_content.value, subtype="html")

        try:
            async with SMTP(hostname=self.smtp_host, port=self.smtp_port) as smtp:
                await smtp.connect()
                await smtp.login(self.username, self.password)

                await smtp.send_message(email_message)

        except Exception as exc:
            raise CannotSendEmailException(exc.args) from exc
