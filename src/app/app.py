from fastapi import FastAPI

from src.app.app_container import AppContainer
from src.app.domain import App
from src.app.presentation import signupRouter, verifyEmailRouter


def bootstrap(container=AppContainer()) -> FastAPI:
    application = App(container, [signupRouter, verifyEmailRouter])

    return application.get_api()
