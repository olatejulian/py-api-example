# pylint: disable=c-extension-no-member
from dependency_injector import containers
from fastapi import APIRouter, FastAPI


class App:
    def __init__(
        self, container: containers.DeclarativeContainer, routes: list[APIRouter]
    ):
        self.container = container
        self.api = FastAPI()

        for route in routes:
            self.api.include_router(route)

    def get_api(self) -> FastAPI:
        return self.api
