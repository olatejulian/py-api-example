import pytest

from src.account import (
    EmptyPasswordException,
    InvalidPasswordTypeException,
    Password,
)


def test_password_value_when_valid():
    """
    should be able to validate password value and return instance if valid
    """
    # given
    valid_value = "john.doe.password"

    # when
    password = Password(valid_value)

    # then
    assert password == valid_value


def test_password_when_type_is_invalid():
    """
    should be able to validate password value type and raise exception if not valid
    """
    # given
    invalid_value = 123

    # when / then
    with pytest.raises(InvalidPasswordTypeException):
        Password(invalid_value)  # type: ignore


def test_password_when_value_is_empty():
    """
    should be able to validate password value empty and raise exception if not valid
    """
    # given
    invalid_value = ""

    # when / then
    with pytest.raises(EmptyPasswordException):
        Password(invalid_value)
