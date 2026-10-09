def create_cumulative_savings_chart(transactions, title="Cumulative Savings Over Time"):
    points = cumulative_savings(transactions)
    if not points:
        return None
    dates = [p[0] for p in points]
    balances = [p[1] for p in points]
    figure = Figure(figsize=(7.2, 4.6), dpi=100)
    axes = figure.add_subplot(111)
    x_positions = range(len(dates))
    axes.plot(x_positions, balances, color=ACCENT, linewidth=2, marker="o", markersize=3)
    axes.fill_between(x_positions, balances, alpha=0.15, color=ACCENT)
    step = max(len(dates) // 8, 1)
    axes.set_xticks(list(range(0, len(dates), step)))
    axes.set_xticklabels(dates[::step], rotation=45, ha="right", fontsize=8)
    axes.axhline(0, color="grey", linewidth=0.8)
    axes.set_title(title, fontsize=12, fontweight="bold")
    axes.set_ylabel("Balance ($)")
    _style_axes(axes)
    figure.tight_layout()
    return figure