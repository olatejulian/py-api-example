from src.shared import Event

from .value_object import EmailAddress, Id, Name


class AccountCreated(Event):
    def __init__(self, account_id: Id, name: Name, email_address: EmailAddress):
        self.account_id = account_id
        self.name = name
        self.email_address = email_address
