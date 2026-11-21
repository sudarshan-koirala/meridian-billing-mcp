"""Support tickets."""
from dataclasses import dataclass

from meridian.accounts import get_account
from meridian.db import Database


@dataclass
class Ticket:
    account_id: str
    subject: str
    priority: str


def open_ticket(account_id, subject):
    account = get_account(account_id)
    priority = "high" if account.plan == "enterprise" else "normal"
    ticket = Ticket(account.account_id, subject, priority)
    Database().save_ticket(ticket)
    return ticket


def ticket_count(account_id):
    return len(Database().tickets_for(account_id))
