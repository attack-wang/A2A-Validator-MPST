import random
import tkinter as tk

SIZE = 4
CELL = 90
GAP = 10
PAD = 10
WIDTH = SIZE * CELL + (SIZE + 1) * GAP
COLORS = {
    0: ("#cdc1b4", "#cdc1b4"), 2: ("#eee4da", "#776e65"), 4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"), 16: ("#f59563", "#f9f6f2"), 32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"), 128: ("#edcf72", "#f9f6f2"), 256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"), 1024: ("#edc53f", "#f9f6f2"), 2048: ("#edc22e", "#f9f6f2"),
}
FALLBACK = ("#3c3a32", "#f9f6f2")


class Game2048:
    def __init__(self, root):
        self.root = root
        root.title("2048")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIDTH, height=WIDTH,
                                bg="#bbada0", highlightthickness=0)
        self.canvas.pack(padx=PAD, pady=(PAD, 4))
        self.score_var = tk.StringVar(value="Score: 0")
        self.best_var = tk.StringVar(value="Best tile: 0")
        bar = tk.Frame(root)
        bar.pack(pady=(0, 2))
        tk.Label(bar, textvariable=self.score_var, font=("Helvetica", 14, "bold"),
                 fg="#776e65").pack(side="left", padx=12)
        tk.Label(bar, textvariable=self.best_var, font=("Helvetica", 14, "bold"),
                 fg="#776e65").pack(side="left", padx=12)
        tk.Label(root, text="Arrow keys to move - R to restart",
                 fg="#776e65").pack(pady=(0, PAD))
        root.bind("<Key>", self.on_key)
        self.reset()

    def reset(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.best_tile = 0
        self.won = False
        self.over = False
        self.add_tile()
        self.add_tile()
        self.draw()

    def add_tile(self):
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if self.grid[r][c] == 0]
        if not empty:
            return
        r, c = random.choice(empty)
        self.grid[r][c] = 2 if random.random() < 0.9 else 4

    @staticmethod
    def slide(row):
        vals = [v for v in row if v]
        out, gained, i = [], 0, 0
        while i < len(vals):
            if i + 1 < len(vals) and vals[i] == vals[i + 1]:
                m = vals[i] * 2
                out.append(m)
                gained += m
                i += 2
            else:
                out.append(vals[i])
                i += 1
        return out + [0] * (SIZE - len(out)), gained

    def move(self, direction):
        if self.over:
            return
        g = self.grid
        lines = [list(r) for r in g] if direction in ("left", "right") \
            else [list(c) for c in zip(*g)]
        rev = direction in ("right", "down")
        if rev:
            lines = [l[::-1] for l in lines]
        gained = 0
        merged = []
        for line in lines:
            nl, gn = self.slide(line)
            gained += gn
            merged.append(nl)
        if rev:
            merged = [l[::-1] for l in merged]
        new = merged if direction in ("left", "right") else [list(c) for c in zip(*merged)]
        if new == g:
            return
        self.grid = new
        self.score += gained
        self.add_tile()
        hi = max(max(r) for r in self.grid)
        self.best_tile = max(self.best_tile, hi)
        if hi >= 2048:
            self.won = True
        if not self.can_move():
            self.over = True
        self.draw()

    def can_move(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.grid[r][c] == 0:
                    return True
                if c + 1 < SIZE and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r + 1 < SIZE and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False

    def draw(self):
        self.score_var.set("Score: %d" % self.score)
        self.best_var.set("Best tile: %d" % self.best_tile)
        cv = self.canvas
        cv.delete("all")
        for r in range(SIZE):
            for c in range(SIZE):
                x1 = GAP + c * (CELL + GAP)
                y1 = GAP + r * (CELL + GAP)
                x2, y2 = x1 + CELL, y1 + CELL
                v = self.grid[r][c]
                fill, fg = COLORS.get(v, FALLBACK)
                cv.create_rectangle(x1, y1, x2, y2, fill=fill, outline="")
                if v:
                    font = ("Helvetica", 26 if v < 1000 else 20, "bold")
                    cv.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(v),
                                   fill=fg, font=font)
        if self.over:
            cv.create_rectangle(GAP, GAP, WIDTH - GAP, WIDTH - GAP,
                                fill="#bbada0", stipple="gray50", outline="")
            cv.create_text(WIDTH // 2, WIDTH // 2, text="Game Over!",
                           fill="#776e65", font=("Helvetica", 30, "bold"))
        elif self.won:
            cv.create_text(WIDTH // 2, 24, text="You reached 2048!",
                           fill="#776e65", font=("Helvetica", 16, "bold"))

    def on_key(self, event):
        key = event.keysym.lower()
        dirs = {"up": "up", "w": "up", "down": "down", "s": "down",
                "left": "left", "a": "left", "right": "right", "d": "right"}
        if key in dirs:
            self.move(dirs[key])
        elif key == "r":
            self.reset()


def main():
    root = tk.Tk()
    Game2048(root)
    root.mainloop()


if __name__ == "__main__":
    main()