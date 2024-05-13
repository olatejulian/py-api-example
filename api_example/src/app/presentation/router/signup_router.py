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


SIGNUP_RESPONSE_MESSAGE = "An email for verification purposes will send."


class SignupResponseData(BaseModel):
    email: str


class SignupResponse(APIResponse[SignupResponseData]):
    class Config:
        schema_extra = SchemaExtraConfig.override_schema_extra_example(
            data={"email": "john.doe@email.com"},
            message=SIGNUP_RESPONSE_MESSAGE,
        )


signupRouter = APIRouter(tags=["Public", "Signup"])


@signupRouter.post(
    "/signup",
    response_model=SignupResponse,
)
@inject
async def signup(
    request_body: SignupRequest,
    background_tasks: BackgroundTasks,
    command_bus: CommandBus[CreateAccount, Account] = Depends(
        Provide[AppContainer.command_bus]
    ),
    event_bus: EventBus = Depends(Provide[AppContainer.event_bus]),
):
    command = CreateAccount(
        name=Name(request_body.name),
        email=EmailAddress(request_body.email),
        password=Password(request_body.password),
    )

    account = await command_bus.dispatch(command)

    events = account.collect_events()

    for event in events:
        background_tasks.add_task(event_bus.dispatch, event)

    account_email = account.email.address.value

    response = SignupResponse(
        status_code=200,
        data=SignupResponseData(email=account_email),
        message=SIGNUP_RESPONSE_MESSAGE,
    )

    return response
