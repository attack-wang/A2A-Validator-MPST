def plot_savings_progress(self, goals, title="Savings Goals Progress", filename="savings_progress.png"):
    if not MATPLOTLIB_AVAILABLE or not goals:
        return self.text_savings_progress(goals, title)
    names = [g.name for g in goals]
    percents = [g.progress_percent for g in goals]
    fig, ax = plt.subplots(figsize=(8, max(3, 0.6 * len(goals) + 1.5)))
    bars = ax.barh(names, percents, color="#4169a1")
    ax.barh(names, [100 - p for p in percents], left=percents, color="#d9d9d9")
    for bar, goal in zip(bars, goals):
        ax.text(
            min(goal.progress_percent + 2, 70),
            bar.get_y() + bar.get_height() / 2,
            f"${goal.current_amount:,.0f} / ${goal.target_amount:,.0f} ({goal.progress_percent:.0f}%)",
            va="center", fontsize=9, color="black",
        )
    ax.set_xlim(0, 100)
    ax.set_xlabel("Progress (%)")
    ax.set_title(title)
    ax.invert_yaxis()
    return self._finish(fig, filename)