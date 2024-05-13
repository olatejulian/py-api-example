# pylint: disable=too-many-ancestors
from uuid import UUID

from beanie import Document, Indexed
from beanie.exceptions import RevisionIdWasChanged
from motor.motor_asyncio import AsyncIOMotorClientSession
from pydantic import Field

from src.account.domain import (
    Account,
    AccountEmail,
    AccountNotFoundException,
    AccountPassword,
    AccountRepository,
    DuplicateIdOrEmailException,
    EmailAddress,
    Id,
    Name,
    Password,
    Time,
    VerificationCode,
)


class BeanieAccountModel(Document):
    id: UUID = Field(alias="_id")

    name: str

    email_address: Indexed(str, unique=True)  # type: ignore
    email_verification_code: str | None
    email_verification_code_sent_on: int | None
    email_verified: bool
    email_verified_on: int | None

    password: str
    password_reset_verification_code: str | None
    password_reset_verification_code_sent_on: int | None

    active: bool
    activated_on: int | None
    created_on: int
    updated_on: int

    class Settings:
        name = "accounts"


class BeanieAccountRepository(AccountRepository):
    def __init__(self, session: AsyncIOMotorClientSession) -> None:
        self.session = session

    @staticmethod
    def _to_domain(model: BeanieAccountModel) -> Account:
        return Account(
            id=Id(str(model.id)),
            name=Name(model.name),
            email=AccountEmail(
                address=EmailAddress(model.email_address),
                verification_code=VerificationCode(model.email_verification_code)
                if model.email_verification_code
                else None,
                verification_code_sent_on=Time(model.email_verification_code_sent_on)
                if model.email_verification_code_sent_on
                else None,
                verified=model.email_verified,
                verified_on=Time(model.email_verified_on)
                if model.email_verified_on
                else None,
            ),
            password=AccountPassword(
                password=Password(model.password, hashed=True),
                reset_verification_code=VerificationCode(
                    model.password_reset_verification_code
                )
                if model.password_reset_verification_code
                else None,
                reset_verification_code_sent_on=Time(
                    model.password_reset_verification_code_sent_on
                )
                if model.password_reset_verification_code_sent_on
                else None,
            ),
            active=model.active,
            activated_on=Time(model.activated_on) if model.activated_on else None,
            created_on=Time(model.created_on),
            updated_on=Time(model.updated_on),
        )

    @staticmethod
    def _to_model(account: Account) -> BeanieAccountModel:
        return BeanieAccountModel(
            id=UUID(account.id.value),  # type: ignore
            name=account.name.value,
            email_address=account.email.address.value,
            email_verification_code=account.email.verification_code.value
            if account.email.verification_code
            else None,
            email_verification_code_sent_on=account.email.verification_code_sent_on.value
            if account.email.verification_code_sent_on
            else None,
            email_verified=account.email.verified,
            email_verified_on=account.email.verified_on.value
            if account.email.verified_on
            else None,
            password=account.password.password.value,
            password_reset_verification_code=account.password.reset_verification_code.value
            if account.password.reset_verification_code
            else None,
            password_reset_verification_code_sent_on=account.password.reset_verification_code_sent_on.value  # pylint: disable=line-too-long
            if account.password.reset_verification_code_sent_on
            else None,
            active=account.active,
            activated_on=account.activated_on.value if account.activated_on else None,
            created_on=account.created_on.value,
            updated_on=account.updated_on.value,
        )

    async def __get_model_by(self, *expressions: bool) -> BeanieAccountModel:
        if model := await BeanieAccountModel.find_one(
            *expressions, session=self.session
        ):
            return model

        raise AccountNotFoundException()

    async def save(self, account: Account) -> None:
        model = self._to_model(account)

        try:
            await model.save(self.session)

        except RevisionIdWasChanged as exc:
            raise DuplicateIdOrEmailException(*exc.args) from exc

    async def get_by_id(self, account_id: Id) -> Account:
        model = await self.__get_model_by(
            BeanieAccountModel.id == UUID(account_id.value)
        )

        return self._to_domain(model)

    async def get_by_email(self, email: EmailAddress) -> Account:
        model = await self.__get_model_by(
            BeanieAccountModel.email_address == email.value
        )

        return self._to_domain(model)

    async def update(self, account: Account) -> None:
        account_id = account.id

        account_to_model = self._to_model(account)

        model_to_update = await self.__get_model_by(
            BeanieAccountModel.id == UUID(account_id.value)
        )

        await model_to_update.update({"$set": account_to_model.dict(exclude={"id"})})
