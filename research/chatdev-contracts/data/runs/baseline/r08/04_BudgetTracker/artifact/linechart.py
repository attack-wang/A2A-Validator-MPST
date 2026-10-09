class LineChart(tk.Canvas):
    def __init__(self, master, width=560, height=260, **kwargs):
        super().__init__(master, width=width, height=height,
                         bg="white", highlightthickness=0, **kwargs)
        ...
    def render(self, data):
        """data: list of (label, value) in chronological order."""
        self.delete("all")
        if not data:
            self._draw_empty("No data yet")
            return
        # margins
        left, right, top, bottom = 60, 20, 25, 40
        w = self.width - left - right
        h = self.height - top - bottom
        values = [v for _, v in data]
        vmin, vmax = min(values), max(values)
        if vmin == vmax:
            vmin -= 1; vmax += 1
        # padding
        span = vmax - vmin
        vmin -= span * 0.1
        vmax += span * 0.1
        def xy(i, v):
            x = left + (w * i / max(1, len(data) - 1))
            y = top + h * (1 - (v - vmin) / (vmax - vmin))
            return x, y
        # axes
        self.create_line(left, top, left, top + h, fill="#888")
        self.create_line(left, top + h, left + w, top + h, fill="#888")
        # zero line if in range
        ...
        # gridlines + y labels
        for frac in (0, 0.25, 0.5, 0.75, 1.0):
            y = top + h * (1 - frac)
            self.create_line(left, y, left + w, y, fill="#eee")
            val = vmin + (vmax - vmin) * frac
            self.create_text(left - 6, y, anchor="e", text=f"{val:,.0f}", font=...)
        # line + points
        pts = [xy(i, v) for i, (_, v) in enumerate(data)]
        if len(pts) == 1:
            self.create_oval(pts[0][0]-3, pts[0][1]-3, pts[0][0]+3, pts[0][1]+3, fill="#4E79A7", outline="")
        else:
            self.create_line(*[c for p in pts for c in p], fill="#4E79A7", width=2, smooth=True)
        for (x, y), (label, v) in zip(pts, data):
            self.create_oval(x-3, y-3, x+3, y+3, fill="#4E79A7", outline="white")
            self.create_text(x, top + h + 12, text=label, font=("Segoe UI", 8), angle=...)