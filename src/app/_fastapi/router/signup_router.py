from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from src.core.account import CreateAccount, EmailAddress, Name, Password
from src.core.shared import CommandBus

from ..dependency_injector import command_bus_factory


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


class SignupResponse(BaseModel):
    success: bool


signupRouter = APIRouter(tags=["public"])


@signupRouter.post(
    "/signup",
    response_model=SignupResponse,
)
async def signup(
    request: SignupRequest, command_bus: CommandBus = Depends(command_bus_factory)
):
    await command_bus.dispatch(
        CreateAccount(
            name=Name(request.name),
            email=EmailAddress(request.email),
            password=Password(request.password),
        )
    )

    return SignupResponse(success=True)
