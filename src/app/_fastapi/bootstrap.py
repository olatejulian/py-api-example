from fastapi import APIRouter, FastAPI

from .router.signup_router import signupRouter


def fastapi_bootstrap() -> FastAPI:
    app = FastAPI()

    routers: list[APIRouter] = [signupRouter]

    for router in routers:
        app.include_router(router)

    return app
