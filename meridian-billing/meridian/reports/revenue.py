"""Revenue reports."""
from meridian.accounts import list_accounts_by_region
from meridian.billing.pricing import regional_price
from meridian.utils.currency import format_money, round_money


def monthly_revenue(region):
    """Monthly recurring revenue for one region."""
    accounts = list_accounts_by_region(region)
    return round_money(sum(regional_price(a.account_id) for a in accounts if a.active))


def revenue_table(regions):
    return {r: format_money(monthly_revenue(r)) for r in regions}
