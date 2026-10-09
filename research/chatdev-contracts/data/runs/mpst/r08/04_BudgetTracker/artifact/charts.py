'''
Chart generation module for the Budget Tracker application.
Provides the ChartGenerator class, which embeds matplotlib figures
inside Tkinter frames to render pie, bar, and line charts for the
Reports tab (expenses by category, income vs expenses, savings trend).
'''
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class ChartGenerator:
    """Embeds a matplotlib chart inside a Tkinter parent widget."""
    def __init__(self, parent):
        """Create the figure and canvas inside the given parent widget."""
        self.figure = Figure(figsize=(4, 3), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self._show_empty_message("No data available")
    def _clear_figure(self):
        """Remove all axes from the figure."""
        self.figure.clf()
    def _show_empty_message(self, message):
        """Display a placeholder text when there is no data to plot."""
        self._clear_figure()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=10, color="gray")
        ax.set_xticks([])
        ax.set_yticks([])
        self.canvas.draw()
    def draw_pie(self, data, title="Expenses by Category"):
        """Draw a pie chart from a dict {category: amount}."""
        if not data:
            self._show_empty_message("No expense data for this period")
            return
        self._clear_figure()
        ax = self.figure.add_subplot(111)
        labels = list(data.keys())
        sizes = list(data.values())
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, textprops={"fontsize": 7})
        ax.set_title(title, fontsize=10)
        ax.axis("equal")
        self.figure.tight_layout()
        self.canvas.draw()
    def draw_bar(self, labels, income_values, expense_values, title="Monthly Income vs Expenses"):
        """Draw a grouped bar chart comparing income and expenses per month."""
        if not labels:
            self._show_empty_message("No trend data available")
            return
        self._clear_figure()
        ax = self.figure.add_subplot(111)
        x = range(len(labels))
        width = 0.35
        ax.bar([i - width / 2 for i in x], income_values, width, label="Income", color="#4caf50")
        ax.bar([i + width / 2 for i in x], expense_values, width, label="Expenses", color="#f44336")
        ax.set_xticks(list(x))
        ax.set_xticklabels(labels, fontsize=7)
        ax.set_title(title, fontsize=10)
        ax.legend(fontsize=7)
        ax.tick_params(axis="y", labelsize=7)
        self.figure.tight_layout()
        self.canvas.draw()
    def draw_line(self, labels, net_values, title="Net Savings Trend"):
        """Draw a line chart of net savings over months."""
        if not labels:
            self._show_empty_message("No trend data available")
            return
        self._clear_figure()
        ax = self.figure.add_subplot(111)
        ax.plot(labels, net_values, marker="o", color="#2196f3", linewidth=2)
        ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
        ax.set_title(title, fontsize=10)
        ax.tick_params(axis="x", labelsize=7)
        ax.tick_params(axis="y", labelsize=7)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=7)
        self.figure.tight_layout()
        self.canvas.draw()