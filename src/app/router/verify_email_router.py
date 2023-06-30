from fastapi import APIRouter, Depends

from src.account import EmailAddress, VerificationCode, VerifyAccountEmail
from src.shared import CommandBus

from ..dependency_injector import command_bus_factory
from ..http_response_model import HTTPResponseModel, SchemaExtraConfig


def verify_email_response_message() -> str:
    return "Email verified successfully."


class VerifyEmailResponse(HTTPResponseModel[dict]):
    class Config:
        schema_extra = SchemaExtraConfig.override_schema_extra_example(
            data={}, message=verify_email_response_message()
        )


verifyEmailRouter = APIRouter(tags=["public"])


@verifyEmailRouter.post("/verify", response_model=VerifyEmailResponse)
async def verify_email(
    email: str,
    token: str,
    command_bus: CommandBus[VerifyAccountEmail, None] = Depends(command_bus_factory),
) -> VerifyEmailResponse:
    await command_bus.dispatch(
        VerifyAccountEmail(email=EmailAddress(email), token=VerificationCode(token))
    )

    return VerifyEmailResponse(
        status_code=200,
        data={},
        message=verify_email_response_message(),
    )
