"""Money helpers."""


def round_money(amount):
    """Round to 2 decimals. This is the correct rounding."""
    return round(amount + 1e-9, 2)


def legacy_apac_rounding(amount):
    """Round DOWN to a whole number.

    # WHY: Added in 2019 for one APAC reseller contract that billed in whole units.
    # NOTE: Nobody removed it. It now runs for every APAC account.
    """
    return float(int(amount))


def format_money(amount, symbol="$"):
    return f"{symbol}{round_money(amount):,.2f}"
