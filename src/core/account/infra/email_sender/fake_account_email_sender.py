from src.core.account.domain import (
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
        print(f"recipient: {recipient}")
        print(f"subject: {subject}")
        print(f"html_content: {html_content}")
        print(f"plaintext_content: {plaintext_content}")
