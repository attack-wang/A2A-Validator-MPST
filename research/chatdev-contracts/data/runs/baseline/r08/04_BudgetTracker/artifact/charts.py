'''
charts.py
Lightweight chart widgets drawn directly on tkinter Canvas objects,
so the application runs with no third-party dependencies.
Contains:
    - PieChart:   category breakdown of expenses.
    - LineChart:  monthly net-savings trend.
    - BarChart:   income vs. expense comparison per month.
'''
import tkinter as tk
import math
PALETTE = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
           "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC"]
class PieChart(tk.Canvas):
    def __init__(self, master, width=380, height=280, **kwargs):
        super().__init__(master, width=width, height=height,
                         bg="white", highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
    def render(self, data):
        """data: dict label -> value (only positive values are drawn)."""
        self.delete("all")
        items = [(k, v) for k, v in data.items() if v > 0]
        if not items:
            self._draw_empty("No expense data yet")
            return
        total = sum(v for _, v in items)
        cx, cy = self.width * 0.36, self.height / 2
        radius = min(self.width * 0.32, self.height * 0.42)
        start = 90.0  # start at 12 o'clock, going clockwise
        for idx, (label, value) in enumerate(items):
            extent = (value / total) * 360.0
            color = PALETTE[idx % len(PALETTE)]
            self.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                            start=start, extent=-extent, fill=color,
                            outline="white", width=1)
            start -= extent
        self._draw_legend(items, total, cx + radius + 20)