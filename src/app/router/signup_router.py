from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from src.account import (
    CreateAccount,
    CreateAccountHandlerResponse,
    EmailAddress,
    Name,
    Password,
)
from src.shared import CommandBus

from ..dependency_injector import command_bus_factory
from ..http_response_model import HTTPResponseModel, SchemaExtraConfig


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@email.com",
                "password": "John.Doe.Password",
            }
        }


def signup_response_message(account_email: str) -> str:
    return f"An email for verification purposes will send. If you don't receive any one, resend it using the route '/verify/resend/{account_email}'"  # pylint: disable=line-too-long


class SignupResponseData(BaseModel):
    email: str


class SignupResponse(HTTPResponseModel[SignupResponseData]):
    class Config:
        schema_extra = SchemaExtraConfig.override_schema_extra_example(
            data={"email": "john.doe@email.com"},
            message=signup_response_message("john.doe@email.com"),
        )


signupRouter = APIRouter(tags=["public"])


@signupRouter.post(
    "/signup",
    response_model=SignupResponse,
)
async def signup(
    request: SignupRequest,
    command_bus: CommandBus[CreateAccount, CreateAccountHandlerResponse] = Depends(
        command_bus_factory
    ),
):
    handler_response = await command_bus.dispatch(
        CreateAccount(
            name=Name(request.name),
            email=EmailAddress(request.email),
            password=Password(request.password),
        )
    )

    account_email = handler_response.email.value

    response = SignupResponse(
        status_code=200,
        data=SignupResponseData(email=account_email),
        message=signup_response_message(account_email),
    )

    return response
