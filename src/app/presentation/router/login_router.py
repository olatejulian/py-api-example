from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from src.account import AccessTokenDto, EmailAddress, GetAccessToken
from src.app.app_container import AppContainer
from src.app.domain import APIResponse, QueryBus, SchemaExtraConfig

loginRouter = APIRouter(tags=["Public", "Login"])

LOGIN_RESPONSE_MESSAGE = "Login successful"


class LoginResponseData(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(APIResponse[LoginResponseData]):
    class Config:
        schema_extra = SchemaExtraConfig.override_schema_extra_example(
            data={
                "access_token": "some access token",
                "token_type": "bearer",
            },
            message=LOGIN_RESPONSE_MESSAGE,
        )


@loginRouter.post("/login", response_model=LoginResponse)
@inject
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    query_bus: QueryBus[AccessTokenDto] = Depends(Provide[AppContainer.query_bus]),
):
    response = await query_bus.dispatch(
        GetAccessToken(EmailAddress(form.username), form.password)
    )

    return LoginResponse(
        status_code=200,
        message=LOGIN_RESPONSE_MESSAGE,
        data=LoginResponseData(
            access_token=response.data.access_token, token_type=response.data.token_type
        ),
    )
