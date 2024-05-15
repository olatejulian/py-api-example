from datetime import datetime

from src.shared import ValueObject, ValueValidator


class InvalidTimeException(Exception):
    pass


def is_valid_unix_timestamp(value: int) -> bool:
    try:
        datetime.fromtimestamp(value)

    except Exception:  # pylint: disable=broad-except
        return False

    else:
        return True


class Time(ValueObject[int]):
    def __init__(self, value: int):
        validators = [
            ValueValidator(
                is_valid_unix_timestamp(value),
                InvalidTimeException(),
            ),
        ]

        super().__init__(value, validators)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Time):
            return self.value == other.value

        return self.value == other

    @staticmethod
    def generate() -> "Time":
        return Time(int(datetime.now().timestamp()))
