'''
Utility helpers for the Budget Tracker application.
Provides currency formatting, input validation, and the shared
MONTH_NAMES constant used by the GUI and database layers.
'''
from datetime import datetime
MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
def format_currency(amount):
    """Format a numeric amount as a US dollar currency string."""
    return f"${amount:,.2f}"
def validate_amount(amount_str):
    """Validate that a string is a positive number. Returns float or None."""
    try:
        value = float(amount_str)
        if value <= 0:
            return None
        return value
    except (ValueError, TypeError):
        return None
def validate_date(date_str):
    """Validate a date string in YYYY-MM-DD format. Returns the string or None."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except (ValueError, TypeError):
        return None
def month_name(month_number):
    """Return the English month name for a month number (1-12)."""
    if 1 <= month_number <= 12:
        return MONTH_NAMES[month_number - 1]
    return "Unknown"