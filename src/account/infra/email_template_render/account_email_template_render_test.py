from bs4 import BeautifulSoup

from src.core.account.domain import AccountEmailTemplateRender, Name, Url


def test_account_template_render_render_email_verification_template(
    account_email_template_render: AccountEmailTemplateRender,
):
    """
    should be able to render a template with the provided URL.
    """
    render = account_email_template_render

    email_verification_url = Url(
        "https://a-wonderful-webapp-name.com/verifiy/123456789"
    )

    account_name = Name("John Doe)")

    template = render.render_email_verification_code_template(
        account_name=account_name,
        email_verification_url=email_verification_url,
    )

    html = template.html_content.value

    soup = BeautifulSoup(html, "html.parser")

    account_name_in_template = soup.find("b", {"class": "account-name"})

    assert account_name_in_template is not None

    assert account_name_in_template.text == account_name

    email_verification_url_in_template = soup.find_all(
        "a", {"class": "email-verification-url"}
    )

    for tag in email_verification_url_in_template:
        assert tag["href"] == email_verification_url
