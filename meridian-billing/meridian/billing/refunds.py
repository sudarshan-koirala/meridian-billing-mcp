"""Refunds."""
from meridian.accounts import get_account
from meridian.billing.pricing import regional_price
from meridian.utils.currency import round_money


def refund_amount(account_id, days_used, days_in_month=30):
    """Refund the unused part of the month."""
    get_account(account_id)
    price = regional_price(account_id)
    return round_money(price * (days_in_month - days_used) / days_in_month)
