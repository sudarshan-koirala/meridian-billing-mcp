"""Tax calculation."""
from meridian.accounts import get_account
from meridian.config import get_tax_rate
from meridian.utils.currency import round_money


def calculate_tax(account_id, amount):
    account = get_account(account_id)
    return round_money(amount * get_tax_rate(account.region))
