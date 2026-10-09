'''
ui.py
Interactive menu handlers for the Budget Tracker: all user prompts,
input validation, and dispatch between the console and the
BudgetTracker / ReportGenerator / Visualizer components.
'''
from datetime import datetime
from models import Transaction
from visualizer import MATPLOTLIB_AVAILABLE
def prompt_float(message):
    """Keep asking until the user enters a valid non-negative number."""
    while True:
        raw = input(message).strip()
        try:
            value = float(raw)
        except ValueError:
            print("  Please enter a valid number.")
            continue
        if value < 0:
            print("  Value must be non-negative.")
            continue
        return value
def prompt_positive_float(message):
    """Keep asking until the user enters a number greater than zero."""
    while True:
        value = prompt_float(message)
        if value <= 0:
            print("  Value must be greater than zero.")
            continue
        return value
def prompt_month(message):
    """Ask for a 'YYYY-MM' month; blank input returns the current month."""
    raw = input(message).strip()
    if not raw:
        return datetime.now().strftime("%Y-%m")
    try:
        datetime.strptime(raw, "%Y-%m")
        return raw
    except ValueError:
        print("  Invalid format, using the current month.")
        return datetime.now().strftime("%Y-%m")
def prompt_date(message):
    """Ask for a 'YYYY-MM-DD' date; blank input returns today's date."""
    raw = input(message).strip()
    if not raw:
        return datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(raw, "%Y-%m-%d")
        return raw
    except ValueError:
        print("  Invalid format, using today's date.")
        return datetime.now().strftime("%Y-%m-%d")