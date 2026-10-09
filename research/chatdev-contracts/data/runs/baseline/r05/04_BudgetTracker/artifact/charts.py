'''
charts.py
Chart generation for the Budget Tracker using matplotlib.
...
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
CHART_COLORS = [...]
COLOR_INCOME = "#55A868"
COLOR_EXPENSE = "#C44E52"
COLOR_SAVINGS = "#4C72B0"
COLOR_NEUTRAL = "#8C8C8C"
class ChartGenerator:
    @staticmethod
    def expense_pie_chart(category_totals, title="Expense Breakdown"): ...
    @staticmethod
    def monthly_bar_chart(months, income_values, expense_values, title="Income vs Expenses (Last 6 Months)"):
        fig = Figure(figsize=(4.2, 3.4), dpi=100)
        ax = fig.add_subplot(111)
        if not months:
            ax.text(0.5, 0.5, "No data", ...)
            ax.set_axis_off()
            return fig
        x = range(len(months))
        width = 0.38
        ax.bar([i - width/2 for i in x], income_values, width=width, label="Income", color=COLOR_INCOME)
        ax.bar([i + width/2 for i in x], expense_values, width=width, label="Expenses", color=COLOR_EXPENSE)
        ax.set_xticks(list(x))
        ax.set_xticklabels(months, fontsize=7, rotation=30)
        ax.legend(fontsize=7)
        ax.set_title(title, fontsize=10)
        fig.tight_layout()
        return fig
    @staticmethod
    def savings_line_chart(months, values, title="Savings Growth (Last 6 Months)"):
        fig = Figure(figsize=(4.2, 3.4), dpi=100)
        ax = fig.add_subplot(111)
        if not months:
            ...
        ax.plot(months, values, marker="o", color=COLOR_SAVINGS, linewidth=2)
        ax.set_xticks(list(range(len(months))))  # hmm, the fragment shows ax.set_xticks
        ax.set_xticklabels(months, fontsize=7, rotation=30)
        ...
        return fig
    @staticmethod
    def goal_progress_chart(progress_rows, title="Savings Goal Progress"):
        # horizontal bar chart
        ...
    @staticmethod
    def embed_chart(figure, parent_widget):
        """Embed a matplotlib figure into a tkinter parent widget."""
        if not MATPLOTLIB_AVAILABLE:
            return None
        canvas = FigureCanvasTkAgg(figure, master=parent_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        return canvas