"""Plans, regions and prices for Meridian Labs."""

PLANS = {"free": 0, "pro": 49, "enterprise": 499}
REGIONS = ["NA", "Europe", "APAC", "LATAM"]
TAX_RATES = {"NA": 0.07, "Europe": 0.20, "APAC": 0.10, "LATAM": 0.16}


def get_plan_price(plan):
    """Return the monthly list price for a plan."""
    return PLANS[plan]


def get_tax_rate(region):
    """Return the tax rate for a region."""
    return TAX_RATES[region]
