from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel

from src.account import (
    EmailAddress,
    ResendVerificationEmail,
    VerificationCode,
    VerifyAccountEmail,
)
from src.app.app_container import AppContainer
from src.app.domain import APIResponse, CommandBus, SchemaExtraConfig


def verify_email_response_message() -> str:
    return "Email verified successfully."


class VerifyEmailResponse(APIResponse[dict]):
    class Config:
        schema_extra = SchemaExtraConfig.override_schema_extra_example(
            data={}, message=verify_email_response_message()
        )


verifyEmailRouter = APIRouter(tags=["public", "verify email"])


@verifyEmailRouter.get("/verify", response_model=VerifyEmailResponse)
@inject
async def verify_email(
    email: str,
    token: str,
    command_bus: CommandBus[VerifyAccountEmail, None] = Depends(
        Provide[AppContainer.command_bus]
    ),
) -> VerifyEmailResponse:
    await command_bus.dispatch(
        VerifyAccountEmail(email=EmailAddress(email), token=VerificationCode(token))
    )

    return VerifyEmailResponse(
        status_code=200,
        data={},
        message=verify_email_response_message(),
    )


class ResendVerificationEmailRequest(BaseModel):
    email: str

    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@email.com",
            }
        }


def resend_verification_email_response_message() -> str:
    return "An email will be sent to you shortly."


class ResendVerificationEmailResponse(APIResponse[dict]):
    class Config:
        schema_extra = SchemaExtraConfig.override_schema_extra_example(
            data={}, message=resend_verification_email_response_message()
        )


@verifyEmailRouter.post(
    "/verify", response_model=ResendVerificationEmailResponse, status_code=202
)
@inject
async def resend_verification_email(
    email: ResendVerificationEmailRequest,
    background_tasks: BackgroundTasks,
    command_bus: CommandBus[ResendVerificationEmail, None] = Depends(
        Provide[AppContainer.command_bus]
    ),
):
    command = ResendVerificationEmail(email=EmailAddress(email.email))

    background_tasks.add_task(command_bus.dispatch, command)

    return VerifyEmailResponse(
        status_code=200,
        data={},
        message=resend_verification_email_response_message(),
    )
