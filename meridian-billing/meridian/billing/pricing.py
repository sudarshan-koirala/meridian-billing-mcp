"""Price calculation."""
from meridian.accounts import get_account
from meridian.config import get_plan_price
from meridian.utils.currency import legacy_apac_rounding, round_money


def apply_discount(price, percent):
    return round_money(price * (1 - percent / 100))


def regional_price(account_id, discount_percent=0):
    """Price for one account, after discount and regional rules."""
    account = get_account(account_id)
    price = apply_discount(get_plan_price(account.plan), discount_percent)
    if account.region == "APAC":
        return legacy_apac_rounding(price)
    return round_money(price)
