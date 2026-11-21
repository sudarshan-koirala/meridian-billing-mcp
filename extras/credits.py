"""Account credits."""
from meridian.billing.pricing import regional_price


def apply_credit(account_id, credit):
    """Price for one account after a credit."""
    return max(regional_price(account_id) - credit, 0)
