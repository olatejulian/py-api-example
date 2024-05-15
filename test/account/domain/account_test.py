import pytest

from src.account import (
    Account,
    AccountEmailMustBeVerifiedException,
    AccountInputDto,
    CannotResetAccountPasswordException,
    CannotVerifyAccountEmailException,
    EmailAddress,
    Name,
    Password,
    VerificationCode,
)


def test_account_create_staticmethod():
    """
    should be able to create an account
    """
    # given
    name = "John Doe"
    email = "john.doe@email.com"
    password = "123456"

    entity = Account.create(
        AccountInputDto(
            name=Name(name), email=EmailAddress(email), password=Password(password)
        )
    )

    # then
    expressions = [
        (entity.id is not None),
        (entity.name == name),
        (entity.email.address == email),
        (entity.email.verification_code is None),
        (entity.email.verification_code_sent_on is None),
        (entity.email.verified is False),
        (entity.email.verified_on is None),
        (entity.password.password == password),
        (entity.password.reset_verification_code is None),
        (entity.password.reset_verification_code_sent_on is None),
        (entity.active is False),
        (entity.activated_on is None),
        (entity.created_on is not None),
        (entity.updated_on is not None),
    ]

    assert all(expressions)


def test_account_change_name_method(create_random_account: Account):
    """
    should be able to change the account name
    """
    # given
    entity = create_random_account

    new_name = "Jane Doe"

    old_name = entity.name

    # when
    entity.change_name(Name(new_name))

    # then
    assert entity.name != old_name
    assert entity.name == new_name


def test_account_change_email_method(create_random_account: Account):
    """
    should be able to change the account email
    """
    # given
    entity = create_random_account

    new_email = "john.doe@email.com"

    old_email = entity.email.address

    # when
    entity.change_email(EmailAddress(new_email))

    # then
    assert entity.email.address != old_email
    assert entity.email.address == new_email
    assert entity.email.verified is False
    assert entity.email.verified_on is None


def test_account_generate_verification_code_method(create_random_account: Account):
    """
    should be able to generate a verification code for the account email
    """
    # given
    entity = create_random_account

    # when
    verification_code = entity.generate_verification_code()

    # then
    assert verification_code is not None
    assert entity.email.verification_code == verification_code
    assert entity.email.verification_code_sent_on is not None


def test_account_verify_email_method(create_random_account: Account):
    """
    should be able to verify the account email
    """
    # given
    entity = create_random_account

    code = entity.generate_verification_code()

    # when
    entity.verify_email(code)

    # then
    assert entity.email.verified is True
    assert entity.email.verified_on is not None


def test_account_verify_email_method_when_there_is_no_verification_code(
    create_random_account: Account,
):
    """
    should not be able to verify the account email when there is no verification code
    """
    # given
    entity = create_random_account

    false_code = VerificationCode("123456")

    # when / then
    with pytest.raises(CannotVerifyAccountEmailException):
        entity.verify_email(false_code)


def test_account_verify_email_method_when_there_is_no_verification_code_sent_on_date(
    create_random_account: Account,
):
    """
    should not be able to verify the account email when there is no verification code sent on date
    """
    # given
    entity = create_random_account

    code = entity.generate_verification_code()

    entity.email.verification_code_sent_on = None

    # when / then
    with pytest.raises(CannotVerifyAccountEmailException):
        entity.verify_email(code)


def test_account_verify_email_method_when_when_the_verification_code_has_expired(
    create_random_account: Account,
):
    """
    should not be able to verify the account email when the verification code has expired
    """
    # given
    entity = create_random_account

    code = entity.generate_verification_code()

    if entity.email.verification_code_sent_on is None:
        assert False

    entity.email.verification_code_sent_on.value = (
        entity.email.verification_code_sent_on.value - 3600
    )

    # when / then
    with pytest.raises(CannotVerifyAccountEmailException):
        entity.verify_email(code)


def test_account_verify_email_method_when_the_verification_code_is_not_the_same(
    create_random_account: Account,
):
    """
    should not be able to verify the account email when the verification code is not the same
    """
    # given
    entity = create_random_account

    entity.generate_verification_code()

    false_code = VerificationCode("123456")

    # when / then
    with pytest.raises(CannotVerifyAccountEmailException):
        entity.verify_email(false_code)


def test_account_is_email_verified_method(
    create_random_account: Account,
):
    """
    should be able to say if the account email is verified
    """
    # given
    entity = create_random_account

    verification_code = entity.generate_verification_code()

    entity.verify_email(verification_code)

    # when
    result = entity.is_email_verified()

    # then
    assert result is True


def test_account_generate_reset_password_code_method(create_random_account: Account):
    """
    should be able to generate a reset password code for the account
    """
    # given
    entity = create_random_account

    # when
    reset_password_code = entity.generate_reset_password_code()

    # then
    assert reset_password_code is not None
    assert entity.password.reset_verification_code == reset_password_code
    assert entity.password.reset_verification_code_sent_on is not None


def test_account_reset_password_method(create_random_account: Account):
    """
    should be able to reset the account password
    """
    # given
    entity = create_random_account

    new_password = "123456"

    old_password = entity.password.password

    reset_code = entity.generate_reset_password_code()

    # when
    entity.reset_password(Password(new_password), reset_code)

    # then
    assert entity.password.password != old_password
    assert entity.password.password == new_password
    assert entity.password.reset_verification_code is None
    assert entity.password.reset_verification_code_sent_on is not None


def test_account_reset_password_method_when_there_is_no_reset_verification_code(
    create_random_account: Account,
):
    """
    should not be able to reset the account password when there is no reset verification code
    """
    # given
    entity = create_random_account

    entity_password = entity.password.password

    false_code = VerificationCode("123456")

    # when / then
    with pytest.raises(CannotResetAccountPasswordException):
        entity.reset_password(entity_password, false_code)


def test_account_reset_password_method_when_there_is_no_reset_verification_code_sent_on_date(
    create_random_account: Account,
):
    """
    should not be able to reset the account password
    when there is no reset verification code sent on date
    """
    # given
    entity = create_random_account

    entity_password = entity.password.password

    reset_code = entity.generate_reset_password_code()

    entity.password.reset_verification_code_sent_on = None

    # when / then
    with pytest.raises(CannotResetAccountPasswordException):
        entity.reset_password(entity_password, reset_code)


def test_account_reset_password_method_when_when_the_reset_verification_code_has_expired(
    create_random_account: Account,
):
    """
    should not be able to reset the account password when the reset verification code has expired
    """
    # given
    entity = create_random_account

    entity_password = entity.password.password

    reset_code = entity.generate_reset_password_code()

    if entity.password.reset_verification_code_sent_on is None:
        assert False

    entity.password.reset_verification_code_sent_on.value = (
        entity.password.reset_verification_code_sent_on.value - 3600
    )

    # when / then
    with pytest.raises(CannotResetAccountPasswordException):
        entity.reset_password(entity_password, reset_code)


def test_account_reset_password_method_when_the_reset_verification_code_is_not_the_same(
    create_random_account: Account,
):
    """
    should not be able to reset the account password
    when the reset verification code is not the same
    """
    # given
    entity = create_random_account

    entity_password = entity.password.password

    reset_code = entity.generate_reset_password_code()

    false_code = VerificationCode("123456")

    assert reset_code != false_code

    # when / then
    with pytest.raises(CannotResetAccountPasswordException):
        entity.reset_password(entity_password, false_code)


def test_account_compare_password_method_when_equal():
    """
    should be able to compare the account password
    """
    # given
    name = "John Doe"
    email = "john.doe@email.com"
    password = "john.doe.password"

    entity = Account.create(
        AccountInputDto(
            name=Name(name),
            email=EmailAddress(email),
            password=Password(password),
        )
    )

    # when
    result = entity.compare_password(password)

    # then
    assert result is True


def test_account_compare_password_method_when_not_equal():
    """
    should be able to compare the account password
    """
    # given
    name = "John Doe"
    email = "john.doe@email.com"
    password = "john.doe.password"

    entity = Account.create(
        AccountInputDto(
            name=Name(name),
            email=EmailAddress(email),
            password=Password(password),
        )
    )

    # when
    result = entity.compare_password(password + "1")

    # then
    assert result is False


def test_account_activate_method(create_random_account: Account):
    """
    should be able to activate the account
    """
    # given
    entity = create_random_account

    verification_code = entity.generate_verification_code()

    entity.verify_email(verification_code)

    # when
    entity.activate()

    # then
    assert entity.active is True
    assert entity.activated_on is not None


def test_account_activate_method_when_email_is_not_verified(
    create_random_account: Account,
):
    """
    should not be able to activate the account when the email is not verified
    """
    # given
    entity = create_random_account

    # when
    with pytest.raises(AccountEmailMustBeVerifiedException):
        entity.activate()


def test_account_is_active_method(
    create_random_account: Account,
):
    """
    should be able to say if the account is active
    """
    # given
    entity = create_random_account

    verification_code = entity.generate_verification_code()

    entity.verify_email(verification_code)

    entity.activate()

    # when
    result = entity.is_active()

    # then
    assert result is True


def test_account_deactivate_method(create_random_account: Account):
    """
    should be able to deactivate the account
    """
    # given
    entity = create_random_account

    verification_code = entity.generate_verification_code()

    entity.verify_email(verification_code)

    entity.activate()

    # when
    entity.deactivate()

    # then
    assert entity.active is False
    assert entity.activated_on is None
