"""Tkinter graphical interface for the 2048 game."""
import tkinter as tk

BG = "#bbada0"
EMPTY_BG = "#cdc1b4"
EMPTY_FG = "#776e65"
TILE_COLORS = {
    2: ("#eee4da", "#776e65"), 4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"), 16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"), 64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"), 256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"), 1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}
DEFAULT_TILE = ("#3c3a32", "#f9f6f2")


class GameUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        root.title("2048")
        root.configure(bg=BG)
        root.resizable(False, False)

        header = tk.Frame(root, bg=BG)
        header.pack(pady=(12, 4), padx=12, fill="x")
        tk.Label(header, text="2048", font=("Helvetica", 32, "bold"),
                 bg=BG, fg="#776e65").pack(side="left")
        self.score_var = tk.StringVar(value="0")
        self.best_var = tk.StringVar(value="0")
        for text, var in (("SCORE", self.score_var), ("BEST TILE", self.best_var)):
            box = tk.Frame(header, bg=BG)
            box.pack(side="right", padx=5)
            tk.Label(box, text=text, font=("Helvetica", 10, "bold"),
                     bg=BG, fg="#eee4da").pack()
            tk.Label(box, textvariable=var, font=("Helvetica", 14, "bold"),
                     bg=BG, fg="white").pack()

        controls = tk.Frame(root, bg=BG)
        controls.pack(fill="x", padx=12)
        tk.Button(controls, text="New Game", command=self.restart).pack(side="right")
        self.status_var = tk.StringVar()
        tk.Label(controls, textvariable=self.status_var, font=("Helvetica", 11),
                 bg=BG, fg="#776e65").pack(side="left")

        board = tk.Frame(root, bg=BG)
        board.pack(padx=12, pady=12)
        self.cells = []
        for r in range(game.size):
            row = []
            for c in range(game.size):
                lbl = tk.Label(board, text="", width=5, height=2,
                               font=("Helvetica", 22, "bold"),
                               bg=EMPTY_BG, fg=EMPTY_FG)
                lbl.grid(row=r, column=c, padx=5, pady=5)
                row.append(lbl)
            self.cells.append(row)

        self.update()
        for key in ("Left", "Right", "Up", "Down"):
            root.bind("<%s>" % key, lambda e, d=key.lower(): self.handle_move(d))
        root.bind("<Key-r>", lambda e: self.restart())

    def handle_move(self, direction):
        if self.game.move(direction):
            self.update()

    def update(self):
        g = self.game
        for r in range(g.size):
            for c in range(g.size):
                v = g.grid[r][c]
                lbl = self.cells[r][c]
                if v == 0:
                    lbl.config(text="", bg=EMPTY_BG, fg=EMPTY_FG)
                else:
                    bg, fg = TILE_COLORS.get(v, DEFAULT_TILE)
                    lbl.config(text=str(v), bg=bg, fg=fg)
        self.score_var.set(str(g.score))
        self.best_var.set(str(g.highest))
        if g.over:
            self.status_var.set("Game over! Press 'r' or New Game to restart.")
        elif g.highest >= 2048:
            self.status_var.set("2048 reached! Keep going or press 'r' to restart.")
        else:
            self.status_var.set("Arrow keys to move")

    def restart(self):
        self.game.reset()
        self.update()