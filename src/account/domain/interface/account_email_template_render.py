from abc import ABC, abstractmethod

from ..value_object import EmailContent, Name, Url


class EmailContents:
    def __init__(self, html_content: EmailContent, plaintext_content: EmailContent):
        self.html_content = html_content
        self.plaintext_content = plaintext_content


class AccountEmailTemplateRender(ABC):
    @abstractmethod
    def render_email_verification_code_template(
        self, account_name: Name, email_verification_url: Url
    ) -> EmailContents:
        raise NotImplementedError
