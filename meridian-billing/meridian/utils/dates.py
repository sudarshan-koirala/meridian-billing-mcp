"""Date helpers."""
from datetime import date, timedelta


def month_start(day):
    return day.replace(day=1)


def days_between(first, second):
    return (second - first).days


def add_business_hours(start_hour, hours):
    return start_hour + hours


def today():
    return date.today()


def last_month(day):
    return month_start(day) - timedelta(days=1)
