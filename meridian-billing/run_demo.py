"""Run this file to see the APAC billing gap: python run_demo.py"""
from meridian.api import signup
from meridian.billing.invoices import create_invoice
from meridian.config import REGIONS, get_plan_price

COMPANIES = ["Northwind", "Helix", "Brightpath", "Quanta", "Solvio"]
PLANS = ["pro", "pro", "enterprise", "pro", "enterprise"]
DISCOUNT = 15  # every demo account has the 15% annual discount


def main():
    for region in REGIONS:
        for number, (company, plan) in enumerate(zip(COMPANIES, PLANS), start=1):
            signup(f"{region}-{number}", f"{company} {region}", plan, region)

    print("Region   Invoiced   Expected   Gap")
    for region in REGIONS:
        invoiced = 0.0
        expected = 0.0
        for number, plan in enumerate(PLANS, start=1):
            invoice = create_invoice(f"{region}-{number}", DISCOUNT)
            invoiced += invoice.subtotal
            expected += round(get_plan_price(plan) * (1 - DISCOUNT / 100), 2)
        print(f"{region:<8} {invoiced:>8.2f}   {expected:>8.2f}   {expected - invoiced:>5.2f}")


if __name__ == "__main__":
    main()
