from src.shared import ValueObject, ValueValidator


class InvalidNameTypeException(Exception):
    pass


class EmptyNameException(Exception):
    pass


class Name(ValueObject[str]):
    def __init__(self, value: str):
        validators = [
            ValueValidator(
                isinstance(value, str),
                InvalidNameTypeException(),
            ),
            ValueValidator(
                bool(value),
                EmptyNameException(),
            ),
        ]

        super().__init__(value, validators)

    def __eq__(self, other: object) -> bool:
        other_value = other.value if isinstance(other, Name) else other

        return self.value == other_value
