from abc import ABC, abstractmethod

from ..value_object import EmailContent, Name, Url


class EmailContents:
    def __init__(self, html_content: EmailContent, plaintext_content: EmailContent):
        self.html_content = html_content
        self.plaintext_content = plaintext_content


class AccountEmailTemplateRenderer(ABC):
    @abstractmethod
    def render_verification_email_template(
        self, account_name: Name, email_verification_url: Url
    ) -> EmailContents:
        raise NotImplementedError

    @abstractmethod
    def render_password_reset_email_template(
        self, account_name: Name, password_reset_url: Url
    ) -> EmailContents:
        raise NotImplementedError
