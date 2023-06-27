from src.app._fastapi import fastapi_bootstrap
from src.shared import celery_bootstrap

app = fastapi_bootstrap()

celery = celery_bootstrap()
