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

verifyEmailRouter = APIRouter(tags=["Public", "Verify"])


# post
class ResendVerificationEmailRequest(BaseModel):
    email: str

    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@email.com",
            }
        }


RESEND_VERIFICATION_EMAIL_RESPONSE_MESSAGE = "An email will be sent to you shortly."


class ResendVerificationEmailResponse(APIResponse[dict]):
    class Config:
        schema_extra = SchemaExtraConfig.override_schema_extra_example(
            data={}, message=RESEND_VERIFICATION_EMAIL_RESPONSE_MESSAGE
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
        message=RESEND_VERIFICATION_EMAIL_RESPONSE_MESSAGE,
    )


VERIFY_EMAIL_RESPONSE_MESSAGE = "Email verified successfully."


class VerifyEmailResponse(APIResponse[dict]):
    class Config:
        schema_extra = SchemaExtraConfig.override_schema_extra_example(
            data={}, message=VERIFY_EMAIL_RESPONSE_MESSAGE
        )


# get
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
        message=VERIFY_EMAIL_RESPONSE_MESSAGE,
    )
