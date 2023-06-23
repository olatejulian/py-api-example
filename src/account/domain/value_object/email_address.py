from pydantic import EmailError, EmailStr

from src.shared import ValueObject, ValueValidator


class InvalidEmailAddressException(Exception):
    pass


class EmailAddress(ValueObject[str]):
    def __init__(self, value: str):
        validators = [
            ValueValidator(
                self.is_valid_email_address(value), InvalidEmailAddressException()
            ),
        ]

        super().__init__(value, validators)

    def __eq__(self, other: object) -> bool:
        other_value = other.value if isinstance(other, EmailAddress) else other

        return self.value == other_value

    @staticmethod
    def is_valid_email_address(value: str) -> bool:
        try:
            EmailStr.validate(value)

        except EmailError:
            return False

        else:
            return True
