import pytest

from src.account import (
    EmailSubject,
    EmailSubjectTooLongException,
    InvalidEmailSubjectTypeException,
)


def test_email_subject_when_valid():
    """
    should be able to create an email subject when valid
    """
    # given
    valid_value = "valid_value"

    # when
    email_subject = EmailSubject(valid_value)

    # then
    assert email_subject == valid_value


def test_email_subject_when_invalid_type():
    """
    should raise an exception when invalid type
    """
    # given
    invalid_value = 1

    # when / then
    with pytest.raises(InvalidEmailSubjectTypeException):
        EmailSubject(invalid_value)  # type: ignore


def test_email_subject_when_too_long():
    """
    should raise an exception when too long
    """
    # given
    EMAIL_SUBJECT_MAX_LENGTH = 255  # pylint: disable=invalid-name

    too_long_value = "a" * (EMAIL_SUBJECT_MAX_LENGTH + 1)

    # when / then
    with pytest.raises(EmailSubjectTooLongException):
        EmailSubject(too_long_value)
