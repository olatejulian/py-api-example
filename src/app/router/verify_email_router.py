from fastapi import APIRouter, Depends

from src.account import (
    EmailAddress,
    ResendVerificationEmail,
    VerificationCode,
    VerifyAccountEmail,
)
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


verifyEmailRouter = APIRouter(tags=["public", "verify email"])


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


def resend_verification_email_response_message() -> str:
    return "Verification email resent successfully."


class ResendVerificationEmailResponse(HTTPResponseModel[dict]):
    class Config:
        schema_extra = SchemaExtraConfig.override_schema_extra_example(
            data={}, message=resend_verification_email_response_message()
        )


@verifyEmailRouter.post("verify/resend/{email}")
async def resend_verification_email(
    email: str,
    command_bus: CommandBus[ResendVerificationEmail, None] = Depends(
        command_bus_factory
    ),
):
    await command_bus.dispatch(ResendVerificationEmail(email=EmailAddress(email)))

    return VerifyEmailResponse(
        status_code=200,
        data={},
        message=verify_email_response_message(),
    )
