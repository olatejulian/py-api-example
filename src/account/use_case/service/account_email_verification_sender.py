from src.account.domain import (
    AccountEmailSender,
    AccountEmailTemplateRender,
    EmailAddress,
    EmailSubject,
    Name,
    Url,
    VerificationCode,
)
from src.shared import AppConfig


class AccountEmailVerificationSender:
    def __init__(
        self,
        config: AppConfig,
        email_template_renderer: AccountEmailTemplateRender,
        email_sender: AccountEmailSender,
    ):
        self.config = config
        self.email_template_renderer = email_template_renderer
        self.email_sender = email_sender

    async def execute(
        self,
        account_name: Name,
        account_email_address: EmailAddress,
        verification_code: VerificationCode,
    ) -> None:
        email_verification_url = Url(
            f"{self.config.url}{self.config.verify_path}?email={account_email_address.value}&token={verification_code.value}"
        )

        contents = self.email_template_renderer.render_email_verification_code_template(
            account_name=account_name, email_verification_url=email_verification_url
        )

        recipient = account_email_address
        subject = EmailSubject("Verify your email address")
        html_content = contents.html_content
        plaintext_content = contents.plaintext_content

        await self.email_sender.send(
            recipient=recipient,
            subject=subject,
            html_content=html_content,
            plaintext_content=plaintext_content,
        )
