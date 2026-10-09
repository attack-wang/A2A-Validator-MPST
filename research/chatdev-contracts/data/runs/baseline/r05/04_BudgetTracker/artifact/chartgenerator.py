'''
charts.py
Chart generation for the Budget Tracker using matplotlib.
Provides the ChartGenerator class with methods to build:
- a pie chart of expenses by category,
- a bar chart comparing monthly income vs expenses,
- a line chart of savings growth over time,
- a horizontal bar chart of savings goal progress,
and a helper to embed any generated figure into a tkinter widget.
If matplotlib is not installed, MATPLOTLIB_AVAILABLE is False and the GUI
falls back to text summaries instead of charts.
'''
import tkinter as tk
MATPLOTLIB_AVAILABLE = False
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    pass
# Palette used consistently across charts
CHART_COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
                "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]
# Reusable semantic colors
COLOR_INCOME = "#55A868"
COLOR_EXPENSE = "#C44E52"
COLOR_SAVINGS = "#4C72B0"
COLOR_NEUTRAL = "#8C8C8C"
class ChartGenerator:
    """Builds matplotlib figures for the Budget Tracker dashboard."""
    # ---------------------------------------------------------------- #
    # Expense breakdown
    # ---------------------------------------------------------------- #
    @staticmethod
    def expense_pie_chart(category_totals, title="Expense Breakdown"):
        """Return a Figure with a pie chart of expenses per category."""
        fig = Figure(figsize=(4.2, 3.4), dpi=100)
        ax = fig.add_subplot(111)
        # Keep only positive values; pie charts cannot show negatives.
        clean = {cat: round(float(v), 2)
                 for cat, v in (category_totals or {}).items()
                 if float(v) > 0}
        if not clean:
            ax.text(0.5, 0.5, "No expense data", ha="center", va="center",
                    fontsize=9, color=COLOR_NEUTRAL)
            ax.set_axis_off()
            return fig
        labels = list(clean.keys())
        values = list(clean.values())
        colors = [CHART_COLORS[i % len(CHART_COLORS)]
                  for i in range(len(labels))]
        ax.pie(values, labels=labels, autopct="%1.1f%%",
               colors=colors, startangle=90,
               textprops={"fontsize": 8})
        ax.set_title(title, fontsize=10)
        fig.tight_layout()
        return fig