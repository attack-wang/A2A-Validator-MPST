import random
import tkinter as tk

ROWS, COLS = 8, 8
CELL = 56
COLORS = ["#ff5b5b", "#ffa64d", "#ffe14d", "#6bd66b", "#5b8cff", "#c15bff"]
START_MOVES = 30


class Match3Game:
    def __init__(self, root):
        self.root = root
        root.title("Candy Match 3")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=COLS * CELL, height=ROWS * CELL,
                                bg="#1e1e2e", highlightthickness=0)
        self.canvas.pack()
        self.status = tk.Label(root, font=("Arial", 13, "bold"),
                               bg="#1e1e2e", fg="white")
        self.status.pack(fill="x")
        self.canvas.bind("<Button-1>", self.on_click)
        self.new_game()

    def new_game(self):
        self.score = 0
        self.moves = START_MOVES
        self.sel = None
        self.busy = False
        self.over = False
        self.random_board()
        self.draw()

    def random_board(self):
        while True:
            self.board = [[random.randrange(len(COLORS)) for _ in range(COLS)]
                          for _ in range(ROWS)]
            if not self.find_matches() and self.has_moves():
                return

    def find_matches(self):
        found = set()
        for r in range(ROWS):
            for c in range(COLS - 2):
                v = self.board[r][c]
                if v is not None and self.board[r][c + 1] == v and self.board[r][c + 2] == v:
                    found.update({(r, c), (r, c + 1), (r, c + 2)})
        for c in range(COLS):
            for r in range(ROWS - 2):
                v = self.board[r][c]
                if v is not None and self.board[r + 1][c] == v and self.board[r + 2][c] == v:
                    found.update({(r, c), (r + 1, c), (r + 2, c)})
        return found

    def has_moves(self):
        for r in range(ROWS):
            for c in range(COLS):
                for dr, dc in ((0, 1), (1, 0)):
                    nr, nc = r + dr, c + dc
                    if nr < ROWS and nc < COLS:
                        self.board[r][c], self.board[nr][nc] = \
                            self.board[nr][nc], self.board[r][c]
                        ok = bool(self.find_matches())
                        self.board[r][c], self.board[nr][nc] = \
                            self.board[nr][nc], self.board[r][c]
                        if ok:
                            return True
        return False

    def reshuffle(self):
        cells = [v for row in self.board for v in row]
        while True:
            random.shuffle(cells)
            it = iter(cells)
            self.board = [[next(it) for _ in range(COLS)] for _ in range(ROWS)]
            if not self.find_matches() and self.has_moves():
                return

    def on_click(self, event):
        if self.over:
            self.new_game()
            return
        if self.busy:
            return
        r, c = event.y // CELL, event.x // CELL
        if not (0 <= r < ROWS and 0 <= c < COLS):
            self.sel = None
            self.draw()
            return
        if self.sel is None or self.sel == (r, c):
            self.sel = None if self.sel == (r, c) else (r, c)
        elif abs(self.sel[0] - r) + abs(self.sel[1] - c) == 1:
            first, self.sel = self.sel, None
            self.try_swap(first, (r, c))
            return
        else:
            self.sel = (r, c)
        self.draw()

    def try_swap(self, a, b):
        (r1, c1), (r2, c2) = a, b
        self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]
        if self.find_matches():
            self.moves -= 1
            self.busy = True
            self.resolve(1)
        else:
            self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]
            self.draw()

    def resolve(self, chain):
        matches = self.find_matches()
        if not matches:
            self.busy = False
            if not self.has_moves():
                self.reshuffle()
            if self.moves <= 0:
                self.over = True
            self.draw()
            return
        self.score += 10 * len(matches) * chain
        for r, c in matches:
            self.board[r][c] = None
        self.apply_gravity()
        self.draw()
        self.root.after(260, lambda: self.resolve(chain + 1))

    def apply_gravity(self):
        for c in range(COLS):
            kept = [self.board[r][c] for r in range(ROWS) if self.board[r][c] is not None]
            fill = ROWS - len(kept)
            for r in range(ROWS):
                self.board[r][c] = (random.randrange(len(COLORS)) if r < fill
                                    else kept[r - fill])

    def draw(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x, y = c * CELL, r * CELL
                self.canvas.create_rectangle(x, y, x + CELL, y + CELL, outline="#33334a")
                v = self.board[r][c]
                if v is not None:
                    p = 7
                    self.canvas.create_oval(x + p, y + p, x + CELL - p, y + CELL - p,
                                            fill=COLORS[v], outline="#000000")
        if self.sel:
            r, c = self.sel
            self.canvas.create_rectangle(c * CELL + 2, r * CELL + 2,
                                         (c + 1) * CELL - 2, (r + 1) * CELL - 2,
                                         outline="white", width=3)
        if self.over:
            self.status.config(text="Game Over!  Final Score: %d  -  click board to play again"
                               % self.score)
        else:
            self.status.config(text="Score: %d    Moves left: %d" % (self.score, self.moves))


if __name__ == "__main__":
    root = tk.Tk()
    Match3Game(root)
    root.mainloop()