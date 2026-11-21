"""The public entry points of the service."""
from meridian.accounts import create_account, deactivate_account
from meridian.billing.invoices import create_invoice, invoice_summary
from meridian.billing.refunds import refund_amount
from meridian.notifications.email import send_invoice_email
from meridian.reports.churn import churn_rate, revenue_at_risk
from meridian.reports.revenue import revenue_table
from meridian.support.sla import response_deadline
from meridian.support.tickets import open_ticket


def signup(account_id, name, plan, region):
    return create_account(account_id, name, plan, region)


def bill_customer(account_id):
    return send_invoice_email(account_id)


def cancel(account_id, days_used):
    deactivate_account(account_id)
    return refund_amount(account_id, days_used)


def new_ticket(account_id, subject, opened_hour):
    ticket = open_ticket(account_id, subject)
    return ticket, response_deadline(account_id, opened_hour)


def dashboard(regions):
    return {
        "revenue": revenue_table(regions),
        "churn": {r: churn_rate(r) for r in regions},
        "at_risk": {r: revenue_at_risk(r) for r in regions},
        "invoices": invoice_summary,
    }
