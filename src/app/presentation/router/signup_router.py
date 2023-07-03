from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel, EmailStr

from src.account import Account, CreateAccount, EmailAddress, Name, Password
from src.app.app_container import AppContainer
from src.app.domain import APIResponse, CommandBus, EventBus, SchemaExtraConfig


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


class SignupResponse(APIResponse[SignupResponseData]):
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
@inject
async def signup(
    request: SignupRequest,
    background_tasks: BackgroundTasks,
    command_bus: CommandBus[CreateAccount, Account] = Depends(
        Provide[AppContainer.command_bus]
    ),
    event_bus: EventBus = Depends(Provide[AppContainer.event_bus]),
):
    account = await command_bus.dispatch(
        CreateAccount(
            name=Name(request.name),
            email=EmailAddress(request.email),
            password=Password(request.password),
        )
    )

    events = account.collect_events()

    for event in events:
        background_tasks.add_task(event_bus.dispatch, event)

    account_email = account.email.address.value

    response = SignupResponse(
        status_code=200,
        data=SignupResponseData(email=account_email),
        message=signup_response_message(account_email),
    )

    return response
