"""Churn reports."""
from meridian.accounts import list_accounts_by_region
from meridian.reports.revenue import monthly_revenue
from meridian.support.tickets import ticket_count
from meridian.utils.currency import round_money


def churn_rate(region):
    accounts = list_accounts_by_region(region)
    if not accounts:
        return 0.0
    lost = [a for a in accounts if not a.active]
    return round_money(100 * len(lost) / len(accounts))


def revenue_at_risk(region):
    """Revenue from accounts with many open tickets."""
    accounts = list_accounts_by_region(region)
    risky = [a for a in accounts if ticket_count(a.account_id) >= 3]
    share = len(risky) / len(accounts) if accounts else 0
    return round_money(monthly_revenue(region) * share)
