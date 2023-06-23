from random import randint

from src.shared import ValueObject, ValueValidator


class InvalidVerificationCodeException(Exception):
    pass


class InvalidVerificationCodeLengthException(Exception):
    pass


class VerificationCode(ValueObject[str]):
    __code_length = 6

    def __init__(self, value: str | int):
        if isinstance(value, int):
            value = self.__stringify(value)

        validators = [
            ValueValidator(
                self.is_valid_code(value),
                InvalidVerificationCodeException(),
            ),
            ValueValidator(
                self.is_valid_code_length(value),
                InvalidVerificationCodeLengthException(),
            ),
        ]

        super().__init__(value, validators)

    def __eq__(self, other: object) -> bool:
        other_value = other.value if isinstance(other, VerificationCode) else other

        return self.value == other_value

    def __len__(self) -> int:
        return len(self.value)

    @staticmethod
    def is_valid_code(value: str) -> bool:
        try:
            int(value)

        except (ValueError, TypeError):
            return False

        else:
            return True

    @classmethod
    def is_valid_code_length(cls, value: str) -> bool:
        try:
            if len(value) == cls.__code_length:
                return True

        except (ValueError, TypeError):
            return False

        else:
            return False

    @classmethod
    def __stringify(cls, value: int) -> str:
        return str(value).zfill(cls.__code_length)

    @classmethod
    def generate(cls) -> "VerificationCode":
        return VerificationCode(
            cls.__stringify(randint(0, int("9" * cls.__code_length)))
        )
