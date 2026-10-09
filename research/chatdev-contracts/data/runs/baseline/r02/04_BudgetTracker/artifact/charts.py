'''
charts.py
Chart builders for the Budget Tracker application.
Uses matplotlib (if installed) to create Figure objects that are embedded
into the Tkinter GUI via FigureCanvasTkAgg. If matplotlib is not available
the module degrades gracefully: MATPLOTLIB_AVAILABLE is False and the GUI
shows a friendly notice instead of charts.
'''
MATPLOTLIB_AVAILABLE = True
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except Exception:
    MATPLOTLIB_AVAILABLE = False
from typing import List, Tuple
# Colors used consistently across all charts.
COLOR_INCOME = "#2e7d32"
COLOR_EXPENSE = "#c62828"
COLOR_BALANCE = "#1565c0"
PIE_COLORS = ("#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
              "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac")
def make_trend_figure(series: List[Tuple[str, float, float]]) -> "Figure":
    """Line chart: monthly income vs expenses.
    `series` is a list of (month, income, expenses) tuples as returned by
    Database.get_monthly_series().
    """
    fig = Figure(figsize=(4.6, 3.4), dpi=100)
    ax = fig.add_subplot(111)
    if not series:
        ax.text(0.5, 0.5, "No data yet.\nAdd some transactions to see the trend.",
                ha="center", va="center", fontsize=10, color="gray")
        ax.set_axis_off()
        return fig
    months = [s[0] for s in series]
    income = [s[1] for s in series]
    expenses = [s[2] for s in series]
    ax.plot(months, income, marker="o", label="Income", color=COLOR_INCOME)
    ax.plot(months, expenses, marker="o", label="Expenses", color=COLOR_EXPENSE)
    ax.set_title("Monthly income vs. expenses")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig