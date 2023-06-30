import pytest

from src.account import (
    InvalidVerificationCodeException,
    InvalidVerificationCodeLengthException,
    VerificationCode,
)

VERIFICATION_CODE_LENGTH = 6


def test_verification_code_value_when_valid():
    """
    should be able to validate email address verification code value and return instance if valid
    """
    # given
    valid_value = "1" * VERIFICATION_CODE_LENGTH

    # when
    verification_code = VerificationCode(valid_value)

    # then
    assert verification_code == valid_value


def test_verification_code_value_when_invalid():
    """
    should be able to validate email address verification code value
    and raise exception if not valid
    """
    # given
    invalid_value = True

    # when / then
    with pytest.raises(InvalidVerificationCodeException):
        VerificationCode(invalid_value)


def test_verification_code_value_when_invalid_length():
    """
    should be able to validate email address verification code value
    and raise exception if not valid
    """
    # given
    invalid_value = "1" * (VERIFICATION_CODE_LENGTH + 1)

    # when / then
    with pytest.raises(InvalidVerificationCodeLengthException):
        VerificationCode(invalid_value)


def test_verification_code_generate():
    """
    should be able to generate email address verification code
    """
    # when
    verification_code = VerificationCode.generate()

    # then
    assert isinstance(verification_code, VerificationCode)
    assert isinstance(verification_code.value, str)
    assert len(verification_code) == VERIFICATION_CODE_LENGTH
