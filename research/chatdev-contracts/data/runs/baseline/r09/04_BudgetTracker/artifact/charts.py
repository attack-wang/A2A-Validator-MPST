'''
charts.py
Chart builders for the Budget Tracker application.
build_pie_chart renders the spending mix per category and
build_line_chart renders the cumulative savings trend.
Both functions embed a matplotlib figure inside a tkinter frame;
if matplotlib is unavailable, a lightweight pure-tkinter canvas
fallback is used so the application keeps working.
'''
import math
import tkinter as tk
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
ACCENT = "#1F3B57"
PIE_COLORS = [
    "#1F3B57", "#F6AE2D", "#2F9C95", "#B71C1C", "#7B1FA2",
    "#E65100", "#388E3C", "#5D4037", "#0288D1", "#C2185B", "#78909C",
]
def build_pie_chart(parent, category_totals, title="Spending by Category"):
    """Create a pie chart frame from {category: total_spent} data."""
    if MATPLOTLIB_AVAILABLE:
        return _build_pie_matplotlib(parent, category_totals, title)
    return _build_pie_canvas(parent, category_totals, title)
def _build_pie_matplotlib(parent, category_totals, title):
    frame = tk.Frame(parent, bg="white")
    fig = Figure(figsize=(4.6, 3.4), dpi=100)
    ax = fig.add_subplot(111)
    if not category_totals:
        ax.text(0.5, 0.5, "No expense data yet", ha="center", va="center",
                fontsize=11, color="#888888")
        ax.axis("off")
    else:
        labels = list(category_totals.keys())
        values = list(category_totals.values())
        colors = [PIE_COLORS[i % len(PIE_COLORS)] for i in range(len(labels))]
        ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%",
               startangle=90, textprops={"fontsize": 8})
        ax.set_title(title, fontsize=10, color=ACCENT, fontweight="bold")
        ax.axis("equal")
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return frame
def _build_pie_canvas(parent, category_totals, title):
    """Fallback pie chart drawn with a plain tk.Canvas."""
    frame = tk.Frame(parent, bg="white")
    canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.bind("<Configure>", lambda event: _draw_pie_canvas(
        canvas, category_totals, title))
    return frame
def _draw_pie_canvas(canvas, category_totals, title):
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if width <= 1 or height <= 1:
        return
    canvas.create_text(width / 2, 18, text=title,
                       font=("Segoe UI", 11, "bold"), fill=ACCENT)
    if not category_totals:
        canvas.create_text(width / 2, height / 2, text="No expense data yet",
                           font=("Segoe UI", 10), fill="#888888")
        return
    total = sum(category_totals.values())
    if total <= 0:
        return
    cx, cy = width / 2, height / 2 + 14
    radius = min(width, height) / 2 - 40
    start = 90.0
    for i, (category, value) in enumerate(category_totals.items()):
        extent = value / total * 360.0
        color = PIE_COLORS[i % len(PIE_COLORS)]
        canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                          start=start, extent=-extent, fill=color,
                          outline="white", width=1, style="pieslice")
        mid = math.radians(start - extent / 2)
        lx = cx + (radius * 0.65) * math.cos(mid)
        ly = cy - (radius * 0.65) * math.sin(mid)
        pct = value / total * 100.0
        canvas.create_text(lx, ly, text=f"{pct:.1f}%",
                           font=("Segoe UI", 8, "bold"), fill="white")
        start -= extent
    # Legend
    legend_x = 10
    legend_y = height - 16 * len(category_totals) - 8
    ...