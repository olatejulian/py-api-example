from src.app._celery import celery_bootstrap
from src.app._fastapi import fastapi_bootstrap

app = fastapi_bootstrap()

celery = celery_bootstrap()
