from src.account.domain import (
    AccountEmailSender,
    EmailAddress,
    EmailContent,
    EmailSubject,
)


class FakeAccountEmailSender(AccountEmailSender):
    async def send(
        self,
        recipient: EmailAddress,
        subject: EmailSubject,
        html_content: EmailContent,
        plaintext_content: EmailContent,
    ):
        print(f"recipient: {recipient.value}")
        print(f"subject: {subject.value}")
        print(f"html_content: {html_content.value}")
        print(f"plaintext_content: {plaintext_content.value}")
