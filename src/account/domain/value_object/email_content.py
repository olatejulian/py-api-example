from src.shared import ValueObject, ValueValidator


class InvalidEmailContentTypeException(Exception):
    pass


class EmailContentCannotBeEmptyException(Exception):
    pass


class EmailContentTooLongException(Exception):
    pass


class EmailContent(ValueObject[str]):
    __max_length = 32000

    def __init__(self, value: str):
        super().__init__(
            value,
            [
                ValueValidator(
                    isinstance(value, str), InvalidEmailContentTypeException()
                ),
                ValueValidator(
                    self.__is_not_empty(value), EmailContentCannotBeEmptyException()
                ),
                ValueValidator(
                    self.__is_not_too_long(value), EmailContentTooLongException()
                ),
            ],
        )

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, EmailContent) and self.value == other.value) or (
            isinstance(other, str) and self.value == other
        )

    @staticmethod
    def __is_not_empty(value: str) -> bool:
        return bool(value)

    @classmethod
    def __is_not_too_long(cls, value: str) -> bool:
        return isinstance(value, str) and len(value) <= cls.__max_length
