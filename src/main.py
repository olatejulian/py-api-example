from src.app import fastapi_bootstrap
from src.shared import celery_bootstrap

app = fastapi_bootstrap()

celery = celery_bootstrap()
