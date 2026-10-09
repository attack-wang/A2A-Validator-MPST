'''
Chart rendering module for the Budget Tracker application.
Builds matplotlib pie and line charts embedded in Tkinter frames.
'''
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
PIE_COLORS = [
    "#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#9b59b6",
    "#1abc9c", "#e67e22", "#34495e", "#95a5a6", "#d35400",
]
def create_pie_chart(parent, labels, values):
    """Render a pie chart of expenses by category inside *parent* (a Tk widget).
    Returns the FigureCanvasTkAgg instance, or None if matplotlib is
    unavailable or there is no data to plot.
    """
    if not MATPLOTLIB_AVAILABLE:
        return _fallback_label(parent, "matplotlib is not installed — pie chart unavailable")
    if not values or sum(values) <= 0:
        return _fallback_label(parent, "No expense data yet")
    for child in parent.winfo_children():
        child.destroy()
    fig = Figure(figsize=(4.6, 3.4), dpi=100)
    ax = fig.add_subplot(111)
    colors = [PIE_COLORS[i % len(PIE_COLORS)] for i in range(len(labels))]
    total = sum(values)
    wedges, _, autotexts = ax.pie(
        values,
        colors=colors,
        autopct=lambda pct: f"{pct:.0f}%" if pct >= 4 else "",
        startangle=90,
        counterclock=False,
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
        textprops={"fontsize": 8},
    )
    ax.set_aspect("equal")
    legend_labels = [f"{label} (${value:,.2f})" for label, value in zip(labels, values)]
    ax.legend(wedges, legend_labels, loc="center left",
              bbox_to_anchor=(0.98, 0.5), fontsize=7)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas
def create_line_chart(parent, months, expense_values, saving_values):
    """Render a line chart of monthly expenses vs savings inside *parent*.
    Returns the FigureCanvasTkAgg instance, or None if matplotlib is
    unavailable or there is no data to plot.
    """
    if not MATPLOTLIB_AVAILABLE:
        return _fallback_label(parent, "matplotlib is not installed — line chart unavailable")
    if not months:
        return _fallback_label(parent, "No data yet")
    for child in parent.winfo_children():
        child.destroy()
    fig = Figure(figsize=(4.6, 3.4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(months, expense_values, marker="o", color="#e74c3c", label="Expenses")
    ax.plot(months, saving_values, marker="s", color="#2ecc71", label="Savings")
    ax.set_ylabel("Amount ($)", fontsize=8)
    ax.set_xlabel("Month", fontsize=8)
    ax.tick_params(axis="x", rotation=45, labelsize=7)
    ax.tick_params(axis="y", labelsize=7)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(fontsize=8)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas
def _fallback_label(parent, message):
    """Show a plain Tk message when matplotlib or data is unavailable."""
    for child in parent.winfo_children():
        child.destroy()
    label = tk.Label(parent, text=message, fg="#7f8c8d")
    label.pack(expand=True)
    return None