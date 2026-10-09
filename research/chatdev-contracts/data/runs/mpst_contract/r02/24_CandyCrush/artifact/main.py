import random
import tkinter as tk

SIZE, TYPES, CELL, GAP = 8, 6, 56, 4
START_MOVES = 30
COLORS = ["#ff5252", "#ffd740", "#7c4dff", "#69f0ae", "#40c4ff", "#ff4081"]
GLYPHS = ["\u25cf", "\u25a0", "\u25b2", "\u25c6", "\u2b22", "\u2605"]


def find_matches(g):
    m = set()
    for r in range(SIZE):
        c = 0
        while c < SIZE:
            k = c
            while k < SIZE and g[r][k] == g[r][c]:
                k += 1
            if k - c >= 3:
                m.update((r, i) for i in range(c, k))
            c = k
    for c in range(SIZE):
        r = 0
        while r < SIZE:
            k = r
            while k < SIZE and g[k][c] == g[r][c]:
                k += 1
            if k - r >= 3:
                m.update((i, c) for i in range(r, k))
            r = k
    return m


def has_move(g):
    for r in range(SIZE):
        for c in range(SIZE):
            for dr, dc in ((0, 1), (1, 0)):
                r2, c2 = r + dr, c + dc
                if r2 < SIZE and c2 < SIZE:
                    g[r][c], g[r2][c2] = g[r2][c2], g[r][c]
                    ok = bool(find_matches(g))
                    g[r][c], g[r2][c2] = g[r2][c2], g[r][c]
                    if ok:
                        return True
    return False


def fresh_board():
    while True:
        g = [[random.randrange(TYPES) for _ in range(SIZE)] for _ in range(SIZE)]
        if not find_matches(g) and has_move(g):
            return g


def gravity(g):
    for c in range(SIZE):
        col = [g[r][c] for r in range(SIZE) if g[r][c] is not None]
        col = [None] * (SIZE - len(col)) + col
        for r in range(SIZE):
            g[r][c] = col[r]


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Candy Match 3")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=SIZE * CELL + 2 * GAP,
                                height=SIZE * CELL + 2 * GAP,
                                bg="#1b2631", highlightthickness=0)
        self.canvas.pack()
        self.status = tk.Label(root, font=("Helvetica", 13, "bold"),
                               bg="#1b2631", fg="#ecf0f1", pady=6)
        self.status.pack(fill="x")
        self.canvas.bind("<Button-1>", self.on_click)
        self.new_game()

    def new_game(self):
        self.g = fresh_board()
        self.score = 0
        self.moves = START_MOVES
        self.combo = 1
        self.sel = None
        self.busy = False
        self.over = False
        self.flash = None
        self.msg = ""
        self.draw()

    def set_msg(self, text, ms=1600):
        self.msg = text
        self.draw()
        self.root.after(ms, self._clear_msg)

    def _clear_msg(self):
        self.msg = ""
        self.draw()

    def _clear_flash(self):
        self.flash = None
        self.draw()

    def on_click(self, e):
        if self.over:
            self.new_game()
            return
        if self.busy:
            return
        c = int((e.x - GAP) // CELL)
        r = int((e.y - GAP) // CELL)
        if not (0 <= r < SIZE and 0 <= c < SIZE):
            return
        cell = (r, c)
        if self.sel is None:
            self.sel = cell
        elif self.sel == cell:
            self.sel = None
        elif abs(self.sel[0] - r) + abs(self.sel[1] - c) == 1:
            self.try_swap(self.sel, cell)
        else:
            self.sel = cell
        self.draw()

    def try_swap(self, a, b):
        g = self.g
        g[a[0]][a[1]], g[b[0]][b[1]] = g[b[0]][b[1]], g[a[0]][a[1]]
        if find_matches(g):
            self.moves -= 1
            self.sel = None
            self.combo = 1
            self.busy = True
            self.draw()
            self.root.after(220, self.resolve)
        else:
            g[a[0]][a[1]], g[b[0]][b[1]] = g[b[0]][b[1]], g[a[0]][a[1]]
            self.flash = (a, b)
            self.root.after(220, self._clear_flash)
        self.draw()

    def resolve(self):
        m = find_matches(self.g)
        if not m:
            self.busy = False
            if not has_move(self.g):
                self.g = fresh_board()
                self.set_msg("No moves available - board shuffled!")
            if self.moves <= 0:
                self.over = True
            self.draw()
            return
        self.score += 10 * len(m) * self.combo
        for r, c in m:
            self.g[r][c] = None
        self.combo += 1
        gravity(self.g)
        for r in range(SIZE):
            for c in range(SIZE):
                if self.g[r][c] is None:
                    self.g[r][c] = random.randrange(TYPES)
        self.draw()
        self.root.after(220, self.resolve)

    def _outline(self, cell, color):
        r, c = cell
        x, y = GAP + c * CELL, GAP + r * CELL
        self.canvas.create_rectangle(x + 2, y + 2, x + CELL - 2, y + CELL - 2,
                                     outline=color, width=3)

    def draw(self):
        cv = self.canvas
        cv.delete("all")
        for r in range(SIZE):
            for c in range(SIZE):
                x, y = GAP + c * CELL, GAP + r * CELL
                cv.create_rectangle(x, y, x + CELL, y + CELL, fill="#2c3e50", outline="")
                t = self.g[r][c]
                cv.create_oval(x + 6, y + 6, x + CELL - 6, y + CELL - 6,
                               fill=COLORS[t], outline="")
                cv.create_text(x + CELL / 2, y + CELL / 2, text=GLYPHS[t],
                               fill="#1b2631", font=("Helvetica", 17, "bold"))
        if self.sel:
            self._outline(self.sel, "#ffffff")
        if self.flash:
            for cell in self.flash:
                self._outline(cell, "#ff5252")
        if self.busy and self.combo > 1:
            cv.create_text(GAP + SIZE * CELL / 2, GAP + 14,
                           text="Combo x%d" % self.combo, fill="#ffd740",
                           font=("Helvetica", 13, "bold"))
        if self.msg:
            cv.create_text(GAP + SIZE * CELL / 2, GAP + SIZE * CELL - 16,
                           text=self.msg, fill="#ecf0f1",
                           font=("Helvetica", 12, "bold"))
        if self.over:
            cv.create_rectangle(GAP, GAP, GAP + SIZE * CELL, GAP + SIZE * CELL,
                                fill="#000000", stipple="gray50", outline="")
            cv.create_text(GAP + SIZE * CELL / 2, GAP + SIZE * CELL / 2 - 14,
                           text="Game Over\nScore: %d" % self.score, fill="#ffffff",
                           font=("Helvetica", 18, "bold"), justify="center")
            cv.create_text(GAP + SIZE * CELL / 2, GAP + SIZE * CELL / 2 + 26,
                           text="Click to play again", fill="#bdc3c7",
                           font=("Helvetica", 11))
        self.status.config(text="Score: %d    Moves left: %d"
                           % (self.score, max(self.moves, 0)))


if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()