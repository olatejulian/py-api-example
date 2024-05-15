from passlib.context import CryptContext

from src.shared import ValueObject, ValueValidator


class InvalidPasswordTypeException(Exception):
    pass


class EmptyPasswordException(Exception):
    pass


class Password(ValueObject[str]):
    __cryptographer = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, value: str, hashed: bool = False):
        validators = [
            ValueValidator(
                isinstance(value, str),
                InvalidPasswordTypeException(),
            ),
            ValueValidator(
                bool(value),
                EmptyPasswordException(),
            ),
        ]

        super().__init__(value, validators)

        if not hashed:
            self.__hash_itself()

    def __eq__(self, other: object) -> bool:
        return self.verify(other, self.value) if isinstance(other, str) else False

    @classmethod
    def hash(cls, password: str) -> str:
        return cls.__cryptographer.hash(password)

    @classmethod
    def verify(cls, password: str, hashed_password: str) -> bool:
        return cls.__cryptographer.verify(password, hashed_password)

    def __hash_itself(self) -> None:
        self.value = self.hash(self.value)
