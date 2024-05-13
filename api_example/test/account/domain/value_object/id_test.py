import pytest

from src.account import Id, InvalidIdException


def test_id_value_when_valid():
    """
    should be able to validate id value and return instance if valid
    """
    # given
    valid_value = "123e4567-e89b-12d3-a456-426614174000"

    # when
    test_id = Id(valid_value)

    # then
    assert test_id == valid_value


def test_id_value_when_invalid():
    """
    should be able to validate id value and raise exception if not valid
    """
    # given
    invalid_value = "invalid-id"

    # when / then
    with pytest.raises(InvalidIdException):
        Id(invalid_value)


def test_id_generate():
    """
    should be able to generate id
    """
    # when
    test_id = Id.generate()

    # then
    assert isinstance(test_id.value, str)
