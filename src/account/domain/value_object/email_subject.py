from src.shared import ValueObject, ValueValidator


class InvalidEmailSubjectTypeException(Exception):
    pass


class EmailSubjectTooLongException(Exception):
    pass


class EmailSubject(ValueObject[str]):
    __email_subject_max_length = 255

    def __init__(self, value: str) -> None:
        super().__init__(
            value,
            [
                ValueValidator(
                    isinstance(value, str), InvalidEmailSubjectTypeException()
                ),
                ValueValidator(
                    self.__is_not_too_long(value), EmailSubjectTooLongException()
                ),
            ],
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EmailSubject):
            return self.value == other.value

        if isinstance(other, str):
            return self.value == other

        return False

    @classmethod
    def __is_not_too_long(cls, value: str) -> bool:
        return (
            len(value) <= cls.__email_subject_max_length
            if isinstance(value, str)
            else False
        )
