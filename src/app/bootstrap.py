from fastapi import FastAPI

from .router import signupRouter, verifyEmailRouter


def fastapi_bootstrap() -> FastAPI:
    app = FastAPI()

    routers = [signupRouter, verifyEmailRouter]

    for router in routers:
        app.include_router(router)

    return app
