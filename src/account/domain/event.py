from src.core.shared import Event

from .value_object import EmailAddress, Id, Name


class AccountCreated(Event):
    __event_name = "account.created"

    def __init__(self, account_id: Id, name: Name, email_address: EmailAddress):
        self.account_id = account_id
        self.name = name
        self.email_address = email_address

    @classmethod
    def get_event_name(cls) -> str:
        return cls.__event_name
