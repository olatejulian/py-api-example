import asyncio

from celery import Celery, shared_task

from .config import BaseConfig
from .interface import Event, EventHandler


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


def celery_bootstrap() -> Celery:
    app = Celery(__name__)

    config = CeleryConfig()

    app.conf.broker_url = config.broker_url  # type: ignore
    app.conf.result_backend = config.result_backend  # type: ignore

    app.conf.task_serializer = config.task_serializer  # type: ignore
    app.conf.result_serializer = config.result_serializer  # type: ignore
    app.conf.accept_content = config.accept_content  # type: ignore

    return app


@shared_task()
def event_handler_task(handler: EventHandler, event: Event) -> None:
    asyncio.run(handler.handle(event))
