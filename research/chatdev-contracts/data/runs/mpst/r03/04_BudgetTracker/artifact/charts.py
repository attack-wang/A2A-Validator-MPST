'''
charts.py
...
'''
import calendar
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    import matplotlib.ticker as mticker
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
PALETTE = [...]
def make_category_pie(category_totals, title="Expenses by Category"):
    ... (as before, complete)
def make_monthly_bar(monthly_summary, title="Monthly Income / Expenses / Savings"):
    if not MATPLOTLIB_AVAILABLE:
        return None
    data = {m: v for m, v in (monthly_summary or {}).items()
            if v.get("income", 0) or v.get("expenses", 0) or v.get("savings", 0)}
    if not data:
        return None
    months = sorted(data.keys())
    income = [data[m].get("income", 0.0) for m in months]
    expenses = [data[m].get("expenses", 0.0) for m in months]
    savings = [data[m].get("savings", 0.0) for m in months]
    fig = Figure(figsize=(7.0, 4.2), dpi=100)
    ax = fig.add_subplot(111)
    x_positions = list(range(len(months)))
    width = 0.27
    ax.bar([i - width for i in x_positions], income, width,
           label="Income", color="#2e7d32")
    ax.bar(x_positions, expenses, width,
           label="Expenses", color="#c62828")
    ax.bar([i + width for i in x_positions], savings, width,
           label="Savings", color="#1565c0")
    ax.set_xticks(x_positions)
    ax.set_xticklabels([calendar.month_abbr[m] for m in months])
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda value, _pos: f"{value:,.0f}"))
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    return fig