'''
charts.py
Chart rendering for the Budget Tracker application.
``ChartGenerator`` builds matplotlib figures and embeds them into a
tkinter frame using the TkAgg backend. Three chart types are provided:
* pie   -- expense distribution per category
* line  -- cumulative savings over time
* bar   -- income vs expense per month
The module degrades gracefully: if matplotlib is not installed
``MATPLOTLIB_AVAILABLE`` is set to False and the GUI can inform the
user instead of crashing.
'''
import tkinter as tk
from tkinter import ttk
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:  # pragma: no cover
    MATPLOTLIB_AVAILABLE = False
from models import format_currency
class ChartGenerator:
    """Builds matplotlib charts embedded inside tkinter containers."""
    COLOR_CYCLE = ("#4C72B0", "#DD8452", "#55A868", "#C44E52",
                   "#8172B3", "#937860", "#DA8BC3", "#8C8C8C",
                   "#CCB974", "#64B5CD")
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.canvas = None
    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _clear(self):
        """Remove any previously drawn chart or message from the frame."""
        for child in self.parent.winfo_children():
            child.destroy()
        self.canvas = None
    def _finish(self, figure, title):
        """Embed ``figure`` into the parent frame and draw it."""
        self.canvas = FigureCanvasTkAgg(figure, master=self.parent)
        self.canvas.draw()
        widget = self.canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)
        return widget
    # ------------------------------------------------------------------
    # Public chart builders
    # ------------------------------------------------------------------
    def pie_expenses(self, category_totals, title="Expense Breakdown"):
        """Draw a pie chart of ``{category: total}`` expense data."""
        self._clear()
        if not MATPLOTLIB_AVAILABLE:
            return self._no_matplotlib()
        if not category_totals:
            return self._empty("No expense data to display yet.")
        figure = Figure(figsize=(6, 4.4), dpi=100)
        axis = figure.add_subplot(111)
        labels = list(category_totals.keys())
        values = list(category_totals.values())
        colors = [self.COLOR_CYCLE[i % len(self.COLOR_CYCLE)]
                  for i in range(len(labels))]
        axis.pie(values, labels=labels, colors=colors,
                 autopct=lambda pct: self._pct_autolabel(pct, values),
                 startangle=90, counterclock=False)
        axis.set_title(title)
        figure.tight_layout()
        return self._finish(figure, title)
    def line_savings(self, timeline, title="Cumulative Savings"):
        """Draw a line chart of ``[(YYYY-MM, cumulative_net), ...]``."""
        self._clear()
        if not MATPLOTLIB_AVAILABLE:
            return self._no_matplotlib()
        if not timeline:
            return self._empty("No data to display yet.")
        figure = Figure(figsize=(6, 4.4), dpi=100)
        axis = figure.add_subplot(111)
        months = [point[0] for point in timeline]
        values = [point[1] for point in timeline]
        axis.plot(months, values, marker="o", color="#4C72B0",
                  linewidth=2, markersize=5)
        axis.axhline(0, color="#8C8C8C", linewidth=0.8, linestyle="--")
        axis.set_title(title)
        axis.set_xlabel("Month")
        axis.set_ylabel("Cumulative Net Savings")
        axis.grid(True, linestyle=":", alpha=0.6)
        # Rotate month labels for readability (autofmt_xdate is meant
        # for datetime axes, so plain tick rotation is used here).
        axis.tick_params(axis="x", labelrotation=45)
        figure.tight_layout()
        return self._finish(figure, title)
    def bar_monthly(self, monthly_summary, title="Monthly Income vs Expense"):
        """Draw grouped bars from ``monthly_summary`` (see analytics)."""
        self._clear()
        if not MATPLOTLIB_AVAILABLE:
            return self._no_matplotlib()
        if not monthly_summary:
            return self._empty("No data to display yet.")
        figure = Figure(figsize=(6, 4.4), dpi=100)
        axis = figure.add_subplot(111)
        months = list(monthly_summary.keys())
        income = [monthly_summary[m]["income"] for m in months]
        expense = [monthly_summary[m]["expense"] for m in months]
        positions = range(len(months))
        width = 0.38
        axis.bar([p - width / 2 for p in positions], income,
                 width=width, label="Income", color="#55A868")
        axis.bar([p + width / 2 for p in positions], expense,
                 width=width, label="Expense", color="#C44E52")
        axis.set_xticks(list(positions))
        axis.set_xticklabels(months, rotation=45, ha="right")
        axis.set_title(title)
        axis.set_xlabel("Month")
        axis.set_ylabel("Amount")
        axis.legend()
        axis.grid(True, axis="y", linestyle=":", alpha=0.6)
        figure.tight_layout()
        return self._finish(figure, title)
    # ------------------------------------------------------------------
    # Placeholder panels
    # ------------------------------------------------------------------
    def _no_matplotlib(self):
        """Show guidance when matplotlib is missing."""
        label = ttk.Label(
            self.parent, wraplength=380, justify="center",
            text="matplotlib is required for charts.\n"
                 "Install it with:  pip install matplotlib")
        label.pack(expand=True)
        return label
    def _empty(self, message):
        """Show a friendly message when there is nothing to plot."""
        label = ttk.Label(self.parent, text=message, justify="center")
        label.pack(expand=True)
        return label
    @staticmethod
    def _pct_autolabel(pct, values):
        """Pie label callback showing percentage and absolute value."""
        total = sum(values)
        value = pct / 100.0 * total
        return "{:.1f}%\n({})".format(pct, format_currency(value))