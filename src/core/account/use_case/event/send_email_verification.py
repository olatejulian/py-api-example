from src.core.account.domain import (
    AccountCreated,
    AccountEmailSender,
    AccountEmailTemplateRender,
    AccountRepository,
    EmailSubject,
    Url,
)
from src.core.shared import AppConfig, EventHandler


class SendEmailVerification(EventHandler[AccountCreated]):
    def __init__(
        self,
        app_config: AppConfig,
        repository: AccountRepository,
        email_sender: AccountEmailSender,
        email_template_render: AccountEmailTemplateRender,
    ):
        self.app_config = app_config
        self.repository = repository
        self.email_sender = email_sender
        self.email_template_render = email_template_render

    async def handle(self, event: AccountCreated) -> None:
        account = await self.repository.get_by_id(event.account_id)

        email_verification_code = account.generate_verification_code()

        account_name = account.name
        account_email_address = account.email.address
        email_verification_url = Url(
            f"{self.app_config.url}/verify?emailAddress={account_email_address}&code={email_verification_code.value}"
        )

        contents = self.email_template_render.render_email_verification_code_template(
            account_name=account_name, email_verification_url=email_verification_url
        )

        recipient = account.email.address
        subject = EmailSubject("Verify your email address")
        html_content = contents.html_content
        plaintext_content = contents.plaintext_content

        await self.email_sender.send(
            recipient=recipient,
            subject=subject,
            html_content=html_content,
            plaintext_content=plaintext_content,
        )

        await self.repository.update(account)
