from src.account.domain import AccessTokenDto, AccountAuthenticator, EmailAddress
from src.shared import Query, QueryHandler, QueryResponse


class GetAccessToken(Query):
    def __init__(self, email: EmailAddress, plain_password: str):
        self.email = email
        self.plain_password = plain_password


class GetAccessTokenHandler(QueryHandler):
    def __init__(self, authenticator: AccountAuthenticator):
        self.authenticator = authenticator

    async def handle(self, query: GetAccessToken) -> QueryResponse[AccessTokenDto]:
        access_token = await self.authenticator.authenticate(
            email=query.email,
            plain_password=query.plain_password,
        )

        return QueryResponse[AccessTokenDto](data=access_token)
