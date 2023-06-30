from jinja2 import Environment, FileSystemLoader

from src.account.domain import (
    AccountEmailTemplateRender,
    EmailContent,
    EmailContents,
    Name,
    Url,
)
from src.shared import EmailTemplateConfig


class Jinja2AccountEmailTemplateRender(AccountEmailTemplateRender):
    def __init__(self, config: EmailTemplateConfig):
        self.config = config

        self._env = Environment(loader=FileSystemLoader(self.config.template_dir))

    def render_email_verification_code_template(
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
