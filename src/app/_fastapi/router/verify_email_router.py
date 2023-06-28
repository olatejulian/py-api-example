from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.account import EmailAddress, VerificationCode, VerifyAccountEmail
from src.shared import CommandBus

from ..dependency_injector import command_bus_factory


class VerifyEmailResponse(BaseModel):
    success: bool


verifyEmailRouter = APIRouter(tags=["public"])


@verifyEmailRouter.post("/verify", response_model=VerifyEmailResponse)
async def verify_email(
    email: str,
    token: str,
    command_bus: CommandBus = Depends(command_bus_factory),
) -> VerifyEmailResponse:
    await command_bus.dispatch(
        VerifyAccountEmail(email=EmailAddress(email), token=VerificationCode(token))
    )

    return VerifyEmailResponse(success=True)
