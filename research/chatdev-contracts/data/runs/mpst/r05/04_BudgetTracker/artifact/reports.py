'''
reports.py
Text-based reporting and simple ASCII charts for the Budget Tracker.
ReportGenerator turns the raw numbers produced by tracker.BudgetTracker
into human-friendly summaries, tables and bar charts that the CLI prints.
'''
from datetime import date
def _fmt_money(value):
    """Format a number as a dollar string, e.g. 1234.5 -> '$1,234.50'."""
    return f"${value:,.2f}"
def _bar(value, max_value, width=40):
    """Return a unicode bar of *width* cells proportional to value/max_value."""
    if max_value <= 0:
        return ""
    filled = int(round(value / max_value * width))
    filled = max(0, min(width, filled))
    return "█" * filled
class ReportGenerator:
    ...