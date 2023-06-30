import pytest

from src.account import (
    EmptyNameException,
    InvalidNameTypeException,
    Name,
)


def test_name_value_when_valid():
    """
    should be able to validate name value and return instance if valid
    """
    # given
    valid_value = "John Doe"

    # when
    name = Name(valid_value)

    # then
    assert name == valid_value


def test_name_when_type_is_invalid():
    """
    should be able to validate name value type and raise exception if not valid
    """
    # given
    invalid_value = 123

    # when / then
    with pytest.raises(InvalidNameTypeException):
        Name(invalid_value)  # type: ignore


def test_name_when_value_is_empty():
    """
    should be able to validate name value empty and raise exception if not valid
    """
    # given
    invalid_value = ""

    # when / then
    with pytest.raises(EmptyNameException):
        Name(invalid_value)
