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


class DatabaseConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        self.name = self._get("DATABASE_NAME")
        self.uri = self._get("DATABASE_URI")


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


class CeleryConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        self.broker_url = self._get("CELERY_BROKER_URL")
        self.result_backend = self._get("CELERY_RESULT_BACKEND")
        self.task_serializer = self._get("CELERY_TASK_SERIALIZER")
        self.result_serializer = self._get("CELERY_RESULT_SERIALIZER")
        self.accept_content = self._get("CELERY_ACCEPT_CONTENT").split(",")
        # self.result_expires = self._get("CELERY_RESULT_EXPIRES")
        # self.timezone = self._get("CELERY_TIMEZONE")
