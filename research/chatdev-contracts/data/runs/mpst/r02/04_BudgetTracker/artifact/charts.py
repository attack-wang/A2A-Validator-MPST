'''Chart rendering utilities implemented with pure Tkinter Canvas.
This module draws pie, line, and bar charts directly on a Tkinter Canvas,
removing the external matplotlib dependency so the application runs on any
standard Python installation (Tkinter ships with the standard library).
'''
import math
import tkinter as tk
# Color palette for chart series (cycled when there are many categories).
PALETTE = [
    "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
    "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac",
]
EXPENSE_COLOR = "#d9534f"
INCOME_COLOR = "#5cb85c"
BUDGET_COLOR = "#5bc0de"
GRID_COLOR = "#dddddd"
AXIS_COLOR = "#444444"
def clear_frame(frame: tk.Frame) -> None:
    """Destroy all child widgets of the given frame."""
    for widget in frame.winfo_children():
        widget.destroy()
def _show_empty_message(frame: tk.Frame, message: str) -> None:
    """Display a friendly message when there is no data to chart."""
    tk.Label(frame, text=message, fg="#666666",
             font=("Helvetica", 12, "italic")).pack(expand=True)
def _new_canvas(parent: tk.Frame) -> tk.Canvas:
    """Create a white canvas that fills the parent frame."""
    canvas = tk.Canvas(parent, bg="white", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    return canvas
def _fmt(value: float) -> str:
    """Format a monetary value for axis/legend labels."""
    return f"{value:,.2f}"
def _nice_ceiling(value: float) -> float:
    """Round a maximum value up to a 'nice' axis ceiling (1/2/2.5/5 x 10^n)."""
    if value <= 0:
        return 1.0
    base = 10.0 ** math.floor(math.log10(value))
    for multiplier in (1.0, 2.0, 2.5, 5.0, 10.0):
        ceiling = base * multiplier
        if ceiling >= value:
            return ceiling
    return base * 10.0
def _draw_axes(canvas, left, top, right, bottom, nice_max):
    """Draw y-gridlines, y tick labels, and the x/y axes."""
    plot_h = bottom - top
    for k in range(6):
        y = bottom - (k / 5.0) * plot_h
        if k:
            canvas.create_line(left, y, right, y, fill=GRID_COLOR)
        canvas.create_text(left - 6, y, text=_fmt(nice_max * k / 5.0),
                           anchor="e", font=("Helvetica", 7), fill="#333333")
    canvas.create_line(left, top, left, bottom, fill=AXIS_COLOR)
    canvas.create_line(left, bottom, right, bottom, fill=AXIS_COLOR)
def _draw_title(canvas, title, width):
    canvas.create_text(width / 2, 16, text=title,
                       font=("Helvetica", 11, "bold"), fill="#222222")