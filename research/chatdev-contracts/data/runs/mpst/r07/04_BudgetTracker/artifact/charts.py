"""
charts.py
Chart generation for the Budget Tracker application.
Provides the ChartGenerator class, which renders four chart types from
BudgetTracker data in separate Toplevel windows:
- Spending by Category (pie chart)
- Monthly Spending Trend (line chart with optional budget line)
- Spending vs Budget (bar chart, over-budget months highlighted in red)
- Savings Goals Progress (horizontal bar chart)
matplotlib is treated as an OPTIONAL dependency: every matplotlib import
is wrapped in try/except so this module imports cleanly even when
matplotlib is not installed. When unavailable, chart methods show a
friendly notice through the notify callback instead of crashing the
application with ModuleNotFoundError at import time.
"""