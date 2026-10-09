'''
charts.py
Chart-building helpers for the Budget Tracker application.
Each function draws onto a provided matplotlib Axes so the GUI can
embed multiple charts inside a single dashboard figure. Uses only
matplotlib primitives so no extra dependencies are required beyond
matplotlib itself.
'''
import matplotlib
matplotlib.use("Agg")  # Safe default; the GUI embeds figures via TkAgg canvas.
import matplotlib.pyplot as plt
# A pleasant, consistent color palette for charts.
PALETTE = [
    "#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
    "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC",
]
def plot_expense_pie(ax, category_totals):
    """Draw a pie chart of spending by category onto the given Axes."""
    ax.clear()
    if not category_totals:
        _draw_empty_state(ax, "No expenses recorded yet")
        return
    labels = list(category_totals.keys())
    values = list(category_totals.values())
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(labels))]
    ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 8},
    )
    ax.set_title("Expenses by Category", fontsize=10)
def plot_savings_line(ax, savings_points):
    """Draw a line chart of cumulative savings over recent months."""
    ax.clear()
    if not savings_points:
        _draw_empty_state(ax, "No savings data yet")
        return
    months = [p["month"] for p in savings_points]
    saved = [p["saved"] for p in savings_points]
    ax.plot(months, saved, marker="o", color="#59A14F", linewidth=2)
    ax.fill_between(months, saved, color="#59A14F", alpha=0.15)
    ax.set_title("Cumulative Savings Trend", fontsize=10)
    ax.set_ylabel("Amount", fontsize=8)
    ax.tick_params(axis="x", labelsize=8, rotation=45)
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(True, alpha=0.3)
def plot_monthly_bars(ax, trends):
    """Draw grouped bars comparing income vs. expenses per month."""
    ax.clear()
    if not trends:
        _draw_empty_state(ax, "No monthly data yet")
        return
    months = [t["month"] for t in trends]
    income = [t["income"] for t in trends]
    expenses = [t["expenses"] for t in trends]
    x = range(len(months))
    width = 0.38
    ax.bar([i - width / 2 for i in x], income, width, label="Income", color="#4E79A7")
    ax.bar([i + width / 2 for i in x], expenses, width, label="Expenses", color="#E15759")
    ax.set_xticks(list(x))
    ax.set_xticklabels(months, fontsize=8, rotation=45)
    ax.set_title("Income vs. Expenses by Month", fontsize=10)
    ax.legend(fontsize=8)
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(True, axis="y", alpha=0.3)
def plot_budget_bars(ax, budget_status):
    """Draw horizontal bars showing budget usage per category."""
    ax.clear()
    if not budget_status:
        _draw_empty_state(ax, "No budgets set yet")
        return
    categories = [s["category"] for s in budget_status]
    spent = [s["spent"] for s in budget_status]
    limits = [s["limit"] for s in budget_status]
    y = range(len(categories))
    ax.barh(y, limits, color="#BAB0AC", label="Budget limit")
    ax.barh(y, spent, color="#F28E2B", label="Spent")
    ax.set_yticks(list(y))
    ax.set_yticklabels(categories, fontsize=8)
    ax.invert_yaxis()
    ax.set_title("Budget Usage (Spent vs. Limit)", fontsize=10)
    ax.legend(fontsize=8)
    ax.tick_params(axis="x", labelsize=8)
    ax.grid(True, axis="x", alpha=0.3)
def _draw_empty_state(ax, message):
    """Show a friendly placeholder message when there is no data to chart."""
    ax.text(0.5, 0.5, message, ha="center", va="center",
            fontsize=10, color="#888888", transform=ax.transAxes)
    ax.set_axis_off()