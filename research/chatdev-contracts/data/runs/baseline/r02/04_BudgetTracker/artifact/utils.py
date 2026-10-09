'''
utils.py
Small shared helpers used across the Budget Tracker application.
Provides date parsing/formatting helpers and a currency formatter so
that every module presents dates and money in a consistent way.
'''
from datetime import date, datetime
DATE_FORMAT = "%Y-%m-%d"
def format_currency(value: float) -> str:
    """Format a number as a currency string, e.g. 1234.5 -> '$1,234.50'."""
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.2f}"
def parse_date(text: str) -> str:
    """Validate a 'YYYY-MM-DD' string and return it unchanged.
    Raises ValueError with a friendly message if the text is empty or
    not a valid calendar date in the expected format.
    """
    text = (text or "").strip()
    if not text:
        raise ValueError("Date cannot be empty (expected YYYY-MM-DD).")
    try:
        datetime.strptime(text, DATE_FORMAT)
    except ValueError:
        raise ValueError(f"'{text}' is not a valid date (expected YYYY-MM-DD).")
    return text
def today_str() -> str:
    """Return today's date as a 'YYYY-MM-DD' string."""
    return date.today().strftime(DATE_FORMAT)
def month_str(date_text: str) -> str:
    """Return the 'YYYY-MM' part of a 'YYYY-MM-DD' string."""
    return date_text[:7]
def month_label(month: str) -> str:
    """Convert '2024-05' to 'May 2024' for display purposes."""
    try:
        return datetime.strptime(month, "%Y-%m").strftime("%B %Y")
    except ValueError:
        return month