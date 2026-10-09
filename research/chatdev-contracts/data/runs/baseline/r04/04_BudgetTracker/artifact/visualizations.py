'''
visualizations.py
Chart generation utilities for the Budget Tracker application.
Classes:
    ChartGenerator: Builds matplotlib Figure objects (pie, line, bar)
        that can be embedded directly into the tkinter GUI.
'''
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
class ChartGenerator:
    """Creates matplotlib figures for embedding in the GUI."""
    PIE_COLORS = [
        "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
        "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac",
    ]
    INCOME_COLOR = "#59a14f"
    EXPENSE_COLOR = "#e15759"
    SAVINGS_COLOR = "#4e79a7"
    @staticmethod
    def create_pie_chart(labels, values, title="Expenses by Category"):
        """Return a pie chart Figure showing the category breakdown."""
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        if not values:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            fig.suptitle(title)
            return fig
        colors = [ChartGenerator.PIE_COLORS[i % len(ChartGenerator.PIE_COLORS)] for i in range(len(values))]
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            counterclock=False,
            textprops={"fontsize": 8},
        )
        for autotext in autotexts:
            autotext.set_fontsize(8)
        ax.set_title(title, fontsize=11)
        fig.tight_layout()
        return fig
    @staticmethod
    def create_line_chart(x_labels, y_values, title="Savings Trend", xlabel="Month", ylabel="Cumulative Savings"):
        """Return a line chart Figure of the cumulative savings trend."""
        fig = Figure(figsize=(5.5, 4), dpi=100)
        ax = fig.add_subplot(111)
        if not x_labels:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            fig.suptitle(title)
            return fig
        ax.plot(x_labels, y_values, marker="o", color=ChartGenerator.SAVINGS_COLOR, linewidth=2)
        ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
        ax.set_title(title, fontsize=11)
        ax.set_xlabel(xlabel, fontsize=9)
        ax.set_ylabel(ylabel, fontsize=9)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.tick_params(axis="x", rotation=45, labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        fig.tight_layout()
        return fig
    @staticmethod
    def create_bar_chart(labels, income_values, expense_values, title="Income vs Expenses"):
        """Return a grouped bar chart Figure comparing income and expenses."""
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        if not labels:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            fig.suptitle(title)
            return fig
        x_positions = range(len(labels))
        bar_width = 0.38
        ax.bar([x - bar_width / 2 for x in x_positions], income_values, width=bar_width,
               label="Income", color=ChartGenerator.INCOME_COLOR)
        ax.bar([x + bar_width / 2 for x in x_positions], expense_values, width=bar_width,
               label="Expenses", color=ChartGenerator.EXPENSE_COLOR)
        ax.set_xticks(list(x_positions))
        ax.set_xticklabels(labels, rotation=45, fontsize=8)
        ax.set_title(title, fontsize=11)
        ax.set_ylabel("Amount", fontsize=9)
        ax.legend(fontsize=8)
        ax.grid(True, axis="y", linestyle=":", alpha=0.6)
        ax.tick_params(axis="y", labelsize=8)
        fig.tight_layout()
        return fig