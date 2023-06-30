# pylint: disable=pointless-statement
import pytest

from src.account import InvalidTimeException, Time


def test_time_value_when_valid():
    """
    should be able to validate time value and return instance if valid
    """
    # given
    valid_value = 1616593800

    # when
    time = Time(valid_value)

    # then
    assert time == valid_value


def test_time_value_when_invalid():
    """
    should be able to validate time value and raise exception if not valid
    """
    # given
    invalid_value = 999999999999

    # when / then
    with pytest.raises(InvalidTimeException):
        Time(invalid_value)  # type: ignore


def test_time_generate():
    """
    should be able to generate time
    """
    # when
    time = Time.generate()

    # then
    assert isinstance(time.value, int)
