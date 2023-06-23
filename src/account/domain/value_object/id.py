from uuid import UUID, uuid4

from src.shared import ValueObject, ValueValidator


class InvalidIdException(Exception):
    pass


class Id(ValueObject[str]):
    def __init__(self, value: str):
        validators = [ValueValidator(self.is_valid_id(value), InvalidIdException())]

        super().__init__(value, validators)

    def __eq__(self, other: object) -> bool:
        other_value = other.value if isinstance(other, Id) else other

        return self.value == other_value

    @staticmethod
    def is_valid_id(value: str) -> bool:
        try:
            UUID(value)

        except ValueError:
            return False

        except TypeError:
            return False

        else:
            return True

    @staticmethod
    def generate() -> "Id":
        return Id(str(uuid4()))
