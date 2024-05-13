from src.shared import ValueObject, ValueValidator


class InvalidUrlTypeException(Exception):
    pass


class Url(ValueObject[str]):
    def __init__(self, value: str):
        super().__init__(
            value, [ValueValidator(isinstance(value, str), InvalidUrlTypeException())]
        )

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Url) and self.value == other.value) or (
            isinstance(other, str) and self.value == other
        )
