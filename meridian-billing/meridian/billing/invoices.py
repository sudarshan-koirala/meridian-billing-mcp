"""Invoices."""
from dataclasses import dataclass

from meridian.accounts import get_account
from meridian.billing.pricing import regional_price
from meridian.billing.tax import calculate_tax
from meridian.db import Database
from meridian.utils.currency import format_money


@dataclass
class Invoice:
    account_id: str
    subtotal: float
    tax: float
    total: float


def create_invoice(account_id, discount_percent=0):
    """Build and save the monthly invoice for one account."""
    account = get_account(account_id)
    subtotal = regional_price(account.account_id, discount_percent)
    tax = calculate_tax(account.account_id, subtotal)
    invoice = Invoice(account.account_id, subtotal, tax, subtotal + tax)
    Database().save_invoice(invoice)
    return invoice


def invoice_summary(account_id):
    invoices = Database().invoices_for(account_id)
    return [format_money(i.total) for i in invoices]
