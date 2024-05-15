import pytest

from src.account import (
    EmailContent,
    EmailContentCannotBeEmptyException,
    EmailContentTooLongException,
    InvalidEmailContentTypeException,
)


def test_email_content_when_is_valid():
    """
    should return a EmailContent instance when value is valid
    """
    # given
    valid_value = "valid_value"

    # when
    email_content = EmailContent(valid_value)

    # then
    assert email_content == valid_value


def test_email_content_when_is_not_valid():
    """
    should raise an exception when value is not valid
    """
    # given
    invalid_value = 123

    # when / then
    with pytest.raises(InvalidEmailContentTypeException):
        EmailContent(invalid_value)  # type: ignore


def test_email_content_when_is_empty():
    """
    should raise an exception when value is empty
    """
    # given
    empty_value = ""

    # when / then
    with pytest.raises(EmailContentCannotBeEmptyException):
        EmailContent(empty_value)


def test_email_content_when_is_too_long():
    """
    should raise an exception when value is too long
    """
    # given
    EMAIL_BODY_MAX_LENGTH = 32000  # pylint: disable=invalid-name

    too_long_value = "a" * (EMAIL_BODY_MAX_LENGTH + 1)

    # when / then
    with pytest.raises(EmailContentTooLongException):
        EmailContent(too_long_value)
