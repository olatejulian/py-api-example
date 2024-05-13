from jinja2 import Environment, FileSystemLoader

from src.account.domain import (
    AccountEmailTemplateRenderer,
    EmailContent,
    EmailContents,
    Name,
    Url,
)
from src.shared import Config


class EmailTemplateRendererConfig(Config):
    def __init__(self):
        super().__init__()

        self.template_dir = self._get("EMAIL_TEMPLATE_DIR")
        self.email_verification_html_template = self._get(
            "EMAIL_VERIFICATION_HTML_TEMPLATE"
        )
        self.email_verification_plaintext_template = self._get(
            "EMAIL_VERIFICATION_PLAINTEXT_TEMPLATE"
        )
        self.password_reset_html_template = self._get(
            "EMAIL_PASSWORD_RESET_HTML_TEMPLATE"
        )
        self.password_reset_plaintext_template = self._get(
            "EMAIL_PASSWORD_RESET_PLAINTEXT_TEMPLATE"
        )


class Jinja2AccountEmailTemplateRenderer(AccountEmailTemplateRenderer):
    def __init__(self, config: EmailTemplateRendererConfig):
        self.config = config

        self._env = Environment(loader=FileSystemLoader(self.config.template_dir))

    def __render_template(
        self, account_name: str, email_verification_url: str, template_name: str
    ) -> EmailContent:
        template = self._env.get_template(template_name)

        return EmailContent(
            template.render(
                account_name=account_name,
                email_verification_url=email_verification_url,
            )
        )

    def render_verification_email_template(
        self, account_name: Name, email_verification_url: Url
    ) -> EmailContents:
        html_content, plaintext_content = [
            self.__render_template(
                account_name=account_name.value,
                email_verification_url=email_verification_url.value,
                template_name=template_name,
            )
            for template_name in [
                self.config.email_verification_html_template,
                self.config.email_verification_plaintext_template,
            ]
        ]

        return EmailContents(
            html_content=html_content,
            plaintext_content=plaintext_content,
        )

    def render_password_reset_email_template(
        self, account_name: Name, password_reset_url: Url
    ) -> EmailContents:
        pass
