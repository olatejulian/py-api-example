# pylint: disable=invalid-name,redefined-builtin,too-few-public-methods,too-many-arguments,too-many-instance-attributes

import pendulum

from src.shared import Entity

from .event import AccountCreated
from .value_object import EmailAddress, Id, Name, Password, Time, VerificationCode


class AccountEmail:
    verification_code_expiration_in_minutes = 15

    def __init__(
        self,
        address: EmailAddress,
        verification_code: VerificationCode | None,
        verification_code_sent_on: Time | None,
        verified: bool,
        verified_on: Time | None,
    ):
        self.address = address
        self.verification_code = verification_code
        self.verification_code_sent_on = verification_code_sent_on
        self.verified = verified
        self.verified_on = verified_on


class AccountPassword:
    reset_code_expiration_in_minutes = 15

    def __init__(
        self,
        password: Password,
        reset_verification_code: VerificationCode | None,
        reset_verification_code_sent_on: Time | None,
    ):
        self.password = password
        self.reset_verification_code = reset_verification_code
        self.reset_verification_code_sent_on = reset_verification_code_sent_on


class AccountInputDto:
    def __init__(
        self,
        name: Name,
        email: EmailAddress,
        password: Password,
    ):
        self.name = name
        self.email = email
        self.password = password


class CannotVerifyAccountEmailException(Exception):
    pass


class CannotResetAccountPasswordException(Exception):
    pass


class AccountEmailMustBeVerifiedException(Exception):
    pass


class Account(Entity):
    def __init__(
        self,
        id: Id,
        name: Name,
        email: AccountEmail,
        password: AccountPassword,
        active: bool,
        activated_on: Time | None,
        created_on: Time,
        updated_on: Time,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.activated_on = activated_on
        self.created_on = created_on
        self.updated_on = updated_on

        account_created_event = AccountCreated(self.id, self.name, self.email.address)

        self._events = []
        self._add_event(account_created_event)

    @staticmethod
    def create(data: AccountInputDto, id: str | None = None) -> "Account":
        account_id = Id(id) if id else Id.generate()

        account = Account(
            id=account_id,
            name=data.name,
            email=AccountEmail(
                address=data.email,
                verification_code=None,
                verification_code_sent_on=None,
                verified=False,
                verified_on=None,
            ),
            password=AccountPassword(
                password=data.password,
                reset_verification_code=None,
                reset_verification_code_sent_on=None,
            ),
            active=False,
            activated_on=None,
            created_on=Time.generate(),
            updated_on=Time.generate(),
        )

        return account

    def __update_time(self) -> None:
        self.updated_on = Time.generate()

    def change_name(self, name: Name) -> None:
        self.name = name

        self.__update_time()

    def change_email(self, email: EmailAddress) -> None:
        self.email.address = email

        self.email.verified = False

        self.email.verified_on = None

        self.__update_time()

    def generate_verification_code(self) -> VerificationCode:
        self.email.verification_code = VerificationCode.generate()

        self.email.verification_code_sent_on = Time.generate()

        self.__update_time()

        return self.email.verification_code

    def verify_email(self, verification_code: VerificationCode) -> None:
        if (
            not self.email.verification_code
            or not self.email.verification_code_sent_on
            or pendulum.now()
            .diff(pendulum.from_timestamp(self.email.verification_code_sent_on.value))
            .in_minutes()
            > AccountEmail.verification_code_expiration_in_minutes
            or self.email.verification_code != verification_code
        ):
            raise CannotVerifyAccountEmailException()

        self.email.verified = True

        self.email.verification_code = None

        self.email.verified_on = Time.generate()

        self.__update_time()

    def is_email_verified(self) -> bool:
        return (
            True
            if self.email.verified is True
            and self.email.verification_code is None
            and self.email.verified_on is not None
            else False
        )

    def generate_reset_password_code(self) -> VerificationCode:
        self.password.reset_verification_code = VerificationCode.generate()

        self.password.reset_verification_code_sent_on = Time.generate()

        self.__update_time()

        return self.password.reset_verification_code

    def reset_password(self, password: Password, reset_code: VerificationCode) -> None:
        if (
            not self.password.reset_verification_code
            or not self.password.reset_verification_code_sent_on
            or pendulum.now()
            .diff(
                pendulum.from_timestamp(
                    self.password.reset_verification_code_sent_on.value
                )
            )
            .in_minutes()
            > AccountPassword.reset_code_expiration_in_minutes
            or self.password.reset_verification_code != reset_code
        ):
            raise CannotResetAccountPasswordException()

        self.password.password = password

        self.password.reset_verification_code = None

        self.__update_time()

    def compare_password(self, password: str) -> bool:
        return self.password.password == password

    def activate(self) -> None:
        if not self.is_email_verified():
            raise AccountEmailMustBeVerifiedException()

        self.active = True

        self.activated_on = Time.generate()

        self.__update_time()

    def is_active(self) -> bool:
        return bool(self.active is True and self.activated_on is not None)

    def deactivate(self) -> None:
        self.active = False

        self.activated_on = None

        self.__update_time()
