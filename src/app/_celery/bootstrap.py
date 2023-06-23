from celery import Celery

from src.core.shared import CeleryConfig


def celery_bootstrap() -> Celery:
    app = Celery(__name__)

    config = CeleryConfig()

    app.conf.broker_url = config.broker_url  # type: ignore
    app.conf.result_backend = config.result_backend  # type: ignore

    app.conf.task_serializer = config.task_serializer  # type: ignore
    app.conf.result_serializer = config.result_serializer  # type: ignore
    app.conf.accept_content = config.accept_content  # type: ignore

    return app
