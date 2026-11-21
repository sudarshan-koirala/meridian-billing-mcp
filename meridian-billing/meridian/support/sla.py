"""Support response targets."""
from meridian.accounts import get_account
from meridian.utils.dates import add_business_hours

SLA_HOURS = {"free": 48, "pro": 24, "enterprise": 4}


def response_deadline(account_id, opened_hour):
    account = get_account(account_id)
    return add_business_hours(opened_hour, SLA_HOURS[account.plan])
