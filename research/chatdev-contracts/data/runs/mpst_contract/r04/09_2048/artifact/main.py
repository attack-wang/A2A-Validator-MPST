import random
import tkinter as tk

CELL, GAP = 100, 10
SIZE = CELL * 4 + GAP * 5

COLORS = {
    0: ("#cdc1b4", "#cdc1b4"), 2: ("#eee4da", "#776e65"), 4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"), 16: ("#f59563", "#f9f6f2"), 32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"), 128: ("#edcf72", "#f9f6f2"), 256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"), 1024: ("#edc53f", "#f9f6f2"), 2048: ("#edc22e", "#f9f6f2"),
}
KEYS = ("Left", "Right", "Up", "Down")


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
    return out + [0] * (4 - len(out)), gained


class Game:
    def __init__(self):
        self.board = [0] * 16
        self.score = 0
        self.best = 0
        self.over = False
        self.add_tile()
        self.add_tile()
        self.best = max(self.board)

    def add_tile(self):
        empty = [i for i, v in enumerate(self.board) if not v]
        if empty:
            self.board[random.choice(empty)] = 2 if random.random() < 0.9 else 4

    def move(self, d):
        changed = gained = 0
        b = self.board
        for k in range(4):
            if d in (0, 1):
                idx = [k * 4 + j for j in range(4)]
            else:
                idx = [j * 4 + k for j in range(4)]
            row = [b[i] for i in idx]
            if d in (1, 3):
                row = row[::-1]
            new, g = slide(row)
            gained += g
            if d in (1, 3):
                new = new[::-1]
            for pos, i in enumerate(idx):
                if b[i] != new[pos]:
                    changed = 1
                b[i] = new[pos]
        if changed:
            self.score += gained
            self.best = max(self.best, max(b))
            self.add_tile()
            if not self.can_move():
                self.over = True
        return changed

    def can_move(self):
        b = self.board
        if any(not v for v in b):
            return True
        for r in range(4):
            for c in range(4):
                v = b[r * 4 + c]
                if c < 3 and b[r * 4 + c + 1] == v:
                    return True
                if r < 3 and b[(r + 1) * 4 + c] == v:
                    return True
        return False


class App:
    def __init__(self, root):
        self.root = root
        root.title("2048")
        root.resizable(False, False)
        self.game = Game()
        self.status = tk.Label(root, font=("Helvetica", 14, "bold"), bg="#faf8ef", fg="#776e65")
        self.status.pack(fill="x", pady=4)
        self.canvas = tk.Canvas(root, width=SIZE, height=SIZE, bg="#bbada0", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self.rects = [[None] * 4 for _ in range(4)]
        self.texts = [[None] * 4 for _ in range(4)]
        for r in range(4):
            for c in range(4):
                x = GAP + c * (CELL + GAP)
                y = GAP + r * (CELL + GAP)
                self.rects[r][c] = self.canvas.create_rectangle(
                    x, y, x + CELL, y + CELL, fill="#cdc1b4", outline="")
                self.texts[r][c] = self.canvas.create_text(
                    x + CELL / 2, y + CELL / 2, text="", fill="#776e65",
                    font=("Helvetica", 26, "bold"))
        hint = tk.Label(root, text="Arrow keys to move  |  R to restart",
                        font=("Helvetica", 10), bg="#faf8ef", fg="#776e65")
        hint.pack(pady=(0, 8))
        self.draw()
        for i, key in enumerate(KEYS):
            root.bind("<%s>" % key, lambda e, d=i: self.step(d))
        for k in ("r", "R"):
            root.bind("<%s>" % k, lambda e: self.restart())

    def step(self, d):
        if self.game.over:
            return
        if self.game.move(d):
            if self.game.over:
                self.draw(msg="Game Over!  Press R to restart")
            else:
                self.draw()

    def restart(self):
        self.game = Game()
        self.draw()

    def draw(self, msg=None):
        b = self.game.board
        for r in range(4):
            for c in range(4):
                v = b[r * 4 + c]
                fill, fg = COLORS.get(v, ("#3c3a32", "#f9f6f2"))
                self.canvas.itemconfig(self.rects[r][c], fill=fill)
                self.canvas.itemconfig(self.texts[r][c],
                                       text=str(v) if v else "", fill=fg,
                                       font=("Helvetica", 26 if v < 1024 else 20, "bold"))
        self.status.config(text="Score: %d        Highest tile: %d" % (self.game.score, self.game.best))
        self.canvas.delete("msg")
        if msg:
            self.canvas.create_rectangle(GAP, SIZE / 2 - 40, SIZE - GAP, SIZE / 2 + 40,
                                         fill="#eee4da", outline="", tag="msg")
            self.canvas.create_text(SIZE / 2, SIZE / 2, text=msg,
                                    font=("Helvetica", 20, "bold"), fill="#776e65", tag="msg")


def main():
    root = tk.Tk()
    root.configure(bg="#faf8ef")
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()