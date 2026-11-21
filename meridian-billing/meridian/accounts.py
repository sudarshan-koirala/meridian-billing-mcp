"""Customer accounts."""
from dataclasses import dataclass

from meridian.db import Database


@dataclass
class Account:
    account_id: str
    name: str
    plan: str
    region: str
    active: bool = True


def get_account(account_id):
    """Load one account. Almost every feature starts here."""
    return Database().load_account(account_id)


def create_account(account_id, name, plan, region):
    account = Account(account_id, name, plan, region)
    Database().save_account(account)
    return account


def deactivate_account(account_id):
    account = get_account(account_id)
    account.active = False
    Database().save_account(account)
    return account


def list_accounts_by_region(region):
    return [a for a in Database().all_accounts() if a.region == region]
