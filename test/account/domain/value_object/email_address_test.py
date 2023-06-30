import pytest

from src.account import (
    EmailAddress,
    InvalidEmailAddressException,
)


def test_email_address_when_valid():
    """
    should be able to validate email address value and return instance if valid
    """
    # given
    valid_value = "john.doe@email.valid"

    # when
    email = EmailAddress(valid_value)

    # then
    assert email == valid_value


def test_email_address_when_invalid():
    """
    should be able to validate email address value and raise exception if not valid
    """
    # given
    invalid_value = "invalid-email-address"

    # when / then
    with pytest.raises(InvalidEmailAddressException):
        EmailAddress(invalid_value)
