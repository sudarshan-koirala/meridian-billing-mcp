"""Emails to customers."""
from meridian.accounts import get_account
from meridian.billing.invoices import create_invoice
from meridian.utils.currency import format_money


def send_email(address, subject, body):
    print(f"To: {address} | {subject} | {body}")


def send_invoice_email(account_id):
    account = get_account(account_id)
    invoice = create_invoice(account_id)
    send_email(account.name, "Your Meridian Labs invoice", format_money(invoice.total))
    return invoice
