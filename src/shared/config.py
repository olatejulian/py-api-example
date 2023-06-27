import os

import dotenv


class CannotFindEnvVarException(Exception):
    pass


class BaseConfig:
    def __init__(self):
        dotenv.load_dotenv()

    @staticmethod
    def _get(key: str) -> str:
        if env := os.getenv(key):
            return env

        raise CannotFindEnvVarException(f"Cannot find env var {key}")


class AppConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        self.url = self._get("APP_URL")


class EmailConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        self.smtp_host = self._get("EMAIL_SMTP_HOST")
        self.smtp_port = int(self._get("EMAIL_SMTP_PORT"))
        self.username = self._get("EMAIL_USERNAME")
        self.password = self._get("EMAIL_PASSWORD")
        self.sender = self._get("EMAIL_SENDER_ADDRESS")


class EmailTemplateConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        self.template_dir = self._get("EMAIL_TEMPLATE_DIR")
        self.email_verification_html_template = self._get(
            "EMAIL_VERIFICATION_HTML_TEMPLATE"
        )
        self.email_verification_plaintext_template = self._get(
            "EMAIL_VERIFICATION_PLAINTEXT_TEMPLATE"
        )
        self.reset_password_html_template = self._get(
            "EMAIL_RESET_PASSWORD_HTML_TEMPLATE"
        )
        self.reset_password_plaintext_template = self._get(
            "EMAIL_RESET_PASSWORD_PLAINTEXT_TEMPLATE"
        )


class AuthConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        self.secret_key = self._get("AUTH_SECRET_KEY")
        self.algorithm = self._get("AUTH_ALGORITHM")
        self.access_token_expire_minutes = int(
            self._get("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES")
        )
