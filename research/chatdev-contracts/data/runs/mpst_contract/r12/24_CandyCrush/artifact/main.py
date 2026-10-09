import time
import tkinter as tk

from game import Board, COLORS

CELL = 56
PAD = 4
SIZE = 8
MAX_MOVES = 30


class App:
    def __init__(self, root):
        self.root = root
        root.title("Candy Match")
        root.resizable(False, False)
        self.status = tk.Label(root, font=("Helvetica", 13, "bold"), pady=6)
        self.status.pack()
        self.canvas = tk.Canvas(root, width=SIZE * CELL, height=SIZE * CELL,
                                bg="#1e1e2e", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        tk.Button(root, text="New Game", command=self.new_game, pady=4).pack(pady=6)
        self.new_game()
        self._tick()

    def new_game(self):
        self.board = Board(SIZE)
        if not self.board.has_moves() and not self.board.shuffle():
            self.board = Board(SIZE)
        self.sel = None
        self.over = False
        self.start = None
        self.elapsed = 0.0
        self.draw()

    def on_click(self, e):
        if self.over:
            return
        c, r = e.x // CELL, e.y // CELL
        if not self.board.in_bounds(r, c):
            return
        if self.sel is None:
            self.sel = (r, c)
            self.draw()
            return
        r0, c0 = self.sel
        if abs(r0 - r) + abs(c0 - c) == 1:
            self.sel = None
            if self.board.try_swap(r0, c0, r, c):
                if self.start is None:
                    self.start = time.time()
                self.board.resolve()
                if not self.board.has_moves():
                    if not self.board.shuffle():
                        self.board.grid = Board(SIZE).grid
                    self.board.resolve()
                if self.board.moves >= MAX_MOVES:
                    self.over = True
        else:
            self.sel = (r, c)
        self.draw()

    def draw(self):
        cv = self.canvas
        cv.delete("all")
        for r in range(SIZE):
            for c in range(SIZE):
                k = self.board.grid[r][c]
                x, y = c * CELL + PAD, r * CELL + PAD
                s = CELL - 2 * PAD
                cv.create_oval(x, y, x + s, y + s, fill=COLORS[k], outline="")
        if self.sel:
            r, c = self.sel
            cv.create_rectangle(c * CELL + 2, r * CELL + 2, (c + 1) * CELL - 2,
                                (r + 1) * CELL - 2, outline="white", width=3)
        self.update_status()

    def update_status(self):
        if self.start is not None and not self.over:
            self.elapsed = time.time() - self.start
        mm, ss = divmod(int(self.elapsed), 60)
        text = (f"Score: {self.board.score}    "
                f"Moves: {self.board.moves}/{MAX_MOVES}    "
                f"Time: {mm:02d}:{ss:02d}")
        if self.over:
            text = "GAME OVER  |  " + text
        self.status.config(text=text)

    def _tick(self):
        self.update_status()
        self.root.after(500, self._tick)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()