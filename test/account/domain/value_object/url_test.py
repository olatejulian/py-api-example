from src.account import Url


def test_url_when_is_valid():
    """
    should be able to create a valid url
    """
    # given
    valid_value = "https://www.google.com"

    # when
    url = Url(valid_value)

    # then
    assert url == valid_value
