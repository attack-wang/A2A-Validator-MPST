"""
charts.py
Chart generation for the Budget Tracker application.
Provides the ChartGenerator class, which renders four chart types from
BudgetTracker data in separate Toplevel windows:
- Spending by Category (pie chart)
- Monthly Spending Trend (line chart with optional budget line)
- Spending vs Budget (bar chart, over-budget months highlighted)
- Savings Goals Progress (horizontal bar chart)
matplotlib is treated as an OPTIONAL dependency: all imports are wrapped
in try/except so the application starts and runs normally even when
matplotlib is not installed. In that case, chart buttons simply show a
friendly notice (via the notify callback) instead of raising
ModuleNotFoundError at import time.
"""
import tkinter as tk
from datetime import date
from typing import Callable, Optional
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    Figure = None
    FigureCanvasTkAgg = None
    NavigationToolbar2Tk = None
    MATPLOTLIB_AVAILABLE = False
class ChartGenerator:
    """Generates charts from BudgetTracker data using matplotlib."""
    def __init__(self, tracker, notify: Optional[Callable[[str, str], None]] = None):
        self.tracker = tracker
        self.notify = notify or self._default_notify
    @staticmethod
    def _default_notify(title: str, message: str) -> None:
        print(f"[{title}] {message}")
    def _require_matplotlib(self) -> bool:
        """Return True if matplotlib is available; otherwise show a notice."""
        if not MATPLOTLIB_AVAILABLE:
            self.notify(
                "Charts unavailable",
                "matplotlib is not installed. Run 'pip install matplotlib' to enable charts.",
            )
        return MATPLOTLIB_AVAILABLE
    def _show_figure(self, fig: "Figure", title: str, parent=None) -> None:
        """Display a matplotlib Figure in a new Toplevel window with a toolbar."""
        window = tk.Toplevel(master=parent)
        window.title(title)
        window.geometry("820x620")
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()
    def show_category_pie(self, start_date=None, end_date=None, parent=None) -> None:
        """Pie chart of spending by category."""
        if not self._require_matplotlib():
            return
        data = self.tracker.get_expenses_by_category(start_date=start_date, end_date=end_date)
        data = {k: v for k, v in data.items() if v > 0}
        if not data:
            self.notify("No data", "No expenses found for the selected period.")
            return
        fig = Figure(figsize=(7.5, 5.2), dpi=100)
        ax = fig.add_subplot(111)
        labels = list(data.keys())
        values = list(data.values())
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("Spending by Category")
        ax.axis("equal")
        total = sum(values)
        fig.suptitle(f"Total: ${total:,.2f}", y=0.95)
        self._show_figure(fig, "Spending by Category", parent)
    def show_monthly_trend(self, year=None, parent=None) -> None:
        """Line chart of total spending per month for a year."""
        if not self._require_matplotlib():
            return
        year = int(year) if year else date.today().year
        trend = self.tracker.get_monthly_trend(year)
        months = [date(year, m, 1).strftime("%b") for m in range(1, 13)]
        values = [trend[m] for m in range(1, 13)]
        fig = Figure(figsize=(7.5, 5.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(months, values, marker="o", color="#1f77b4", linewidth=2)
        ax.fill_between(range(12), values, alpha=0.15, color="#1f77b4")
        if self.tracker.monthly_budget > 0:
            ax.axhline(self.tracker.monthly_budget, color="red", linestyle="--",
                       label=f"Budget (${self.tracker.monthly_budget:,.2f})")
            ax.legend()
        ax.set_title(f"Monthly Spending Trend — {year}")
        ax.set_xlabel("Month")
        ax.set_ylabel("Spent ($)")
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis="x", rotation=45)
        self._show_figure(fig, "Monthly Spending Trend", parent)
    def show_comparison_chart(self, year=None, parent=None) -> None:
        """Bar chart comparing monthly spending against the monthly budget."""
        if not self._require_matplotlib():
            return
        year = int(year) if year else date.today().year
        trend = self.tracker.get_monthly_trend(year)
        months = [date(year, m, 1).strftime("%b") for m in range(1, 13)]
        values = [trend[m] for m in range(1, 13)]
        fig = Figure(figsize=(7.5, 5.2), dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.bar(months, values, color="#2ca02c", label="Spent")
        if self.tracker.monthly_budget > 0:
            ax.axhline(self.tracker.monthly_budget, color="red", linestyle="--",
                       label=f"Budget (${self.tracker.monthly_budget:,.2f})")
            for bar, value in zip(bars, values):
                if value > self.tracker.monthly_budget:
                    bar.set_color("#d62728")
        ax.set_title(f"Spending vs Budget — {year}")
        ax.set_xlabel("Month")
        ax.set_ylabel("Spent ($)")
        ax.legend()
        ax.grid(True, axis="y", alpha=0.3)
        ax.tick_params(axis="x", rotation=45)
        self._show_figure(fig, "Spending vs Budget", parent)
    def show_goals_chart(self, parent=None) -> None:
        """Horizontal bar chart of progress toward each savings goal."""
        if not self._require_matplotlib():
            return
        if not self.tracker.savings_goals:
            self.notify("No data", "No savings goals defined yet. Add one on the Savings tab.")
            return
        names = [g.name for g in self.tracker.savings_goals]
        progress = [g.progress * 100 for g in self.tracker.savings_goals]
        fig = Figure(figsize=(7.5, 5.2), dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.barh(names, progress, color="#1f77b4")
        for bar, goal in zip(bars, self.tracker.savings_goals):
            width = bar.get_width()
            label = f"${goal.saved_amount:,.2f} / ${goal.target_amount:,.2f}"
            ax.text(min(width + 1, 100), bar.get_y() + bar.get_height() / 2,
                    label, va="center", fontsize=9)
            if goal.is_complete:
                bar.set_color("#2ca02c")
        ax.set_xlim(0, 110)
        ax.set_xlabel("Progress (%)")
        ax.set_title("Savings Goals Progress")
        ax.grid(True, axis="x", alpha=0.3)
        ax.invert_yaxis()
        self._show_figure(fig, "Savings Goals Progress", parent)