from src.account.domain import (
    AccountEmailSender,
    AccountEmailTemplateRenderer,
    AccountVerificationEmailSender,
    EmailAddress,
    EmailSubject,
    Name,
    Url,
    VerificationCode,
)
from src.shared import Config


class VerificationEmailSenderConfig(Config):
    def __init__(self):
        super().__init__()

        self.url = self._get("APP_URL")
        self.verify_path = self._get("APP_VERIFY_PATH")


class DefaultAccountVerificationEmailSender(AccountVerificationEmailSender):
    def __init__(
        self,
        config: VerificationEmailSenderConfig,
        email_template_renderer: AccountEmailTemplateRenderer,
        email_sender: AccountEmailSender,
    ):
        self.config = config
        self.email_template_renderer = email_template_renderer
        self.email_sender = email_sender

    async def send_verification_email(
        self,
        account_name: Name,
        account_email_address: EmailAddress,
        verification_code: VerificationCode,
    ) -> None:
        email_verification_url = Url(
            f"{self.config.url}/{self.config.verify_path}"
            + f"?email={account_email_address.value}"
            + f"&token={verification_code.value}"
        )

        contents = self.email_template_renderer.render_verification_email_template(
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

    async def send_password_reset_email(
        self,
        account_name: Name,
        account_email_address: EmailAddress,
        password_reset_code: VerificationCode,
    ):
        password_reset_url = Url(
            f"{config.url}/{self.config.verify_path}"
            + f"?email={account_email_address.value}"
            + f"&token={password_reset_code.value}"
        )

        contents = self.email_template_renderer.render_pas
