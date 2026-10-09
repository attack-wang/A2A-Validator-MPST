"""Tkinter front end for the 2048 game: rendering, arrow-key input, score display."""
import tkinter as tk

from game import Game2048

TILE_COLORS = {
    0: ("#cdc1b4", "#cdc1b4"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}
DEFAULT_COLOR = ("#3c3a32", "#f9f6f2")


class GameGUI:
    CELL = 90
    PAD = 8

    def __init__(self, master):
        self.game = Game2048()
        self.master = master
        master.title("2048")
        master.resizable(False, False)
        self.score_var = tk.StringVar(value="0")
        self.highest_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(value="Use arrow keys to play")
        self._build_widgets()
        self._bind_keys()
        self.refresh()

    def _build_widgets(self):
        header = tk.Frame(self.master)
        header.pack(pady=(10, 4))
        tk.Label(header, text="2048", font=("Helvetica", 32, "bold"),
                 fg="#776e65").pack(side="left", padx=10)
        for label, var in (("SCORE", self.score_var), ("BEST TILE", self.highest_var)):
            box = tk.Frame(header, bg="#bbada0", padx=12, pady=4)
            box.pack(side="left", padx=5)
            tk.Label(box, text=label, font=("Helvetica", 10, "bold"),
                     bg="#bbada0", fg="#eee4da").pack()
            tk.Label(box, textvariable=var, font=("Helvetica", 18, "bold"),
                     bg="#bbada0", fg="white").pack()
        tk.Label(self.master, textvariable=self.status_var,
                 font=("Helvetica", 11), fg="#776e65").pack()
        board = tk.Frame(self.master, bg="#bbada0", padx=self.PAD, pady=self.PAD)
        board.pack(padx=10, pady=10)
        self.cells = []
        for r in range(Game2048.SIZE):
            row = []
            for c in range(Game2048.SIZE):
                frame = tk.Frame(board, width=self.CELL, height=self.CELL, bg="#cdc1b4")
                frame.grid(row=r, column=c, padx=self.PAD, pady=self.PAD)
                frame.pack_propagate(False)
                label = tk.Label(frame, text="", font=("Helvetica", 28, "bold"))
                label.place(relx=0.5, rely=0.5, anchor="center")
                row.append(label)
            self.cells.append(row)
        tk.Button(self.master, text="New Game", command=self.new_game,
                  font=("Helvetica", 12, "bold"), bg="#8f7a66", fg="white",
                  activebackground="#9f8b77", activeforeground="white",
                  bd=0, padx=12, pady=6).pack(pady=(0, 12))

    def _bind_keys(self):
        key_map = {"Left": "left", "Right": "right", "Up": "up", "Down": "down"}
        for key, direction in key_map.items():
            self.master.bind("<%s>" % key,
                             lambda event, d=direction: self.handle_move(d))

    def handle_move(self, direction):
        if self.game.over:
            return
        if self.game.move(direction):
            self.refresh()

    def new_game(self):
        self.game.reset()
        self.status_var.set("Use arrow keys to play")
        self.refresh()

    def refresh(self):
        for r in range(Game2048.SIZE):
            for c in range(Game2048.SIZE):
                value = self.game.grid[r][c]
                label = self.cells[r][c]
                bg, fg = TILE_COLORS.get(value, DEFAULT_COLOR)
                text = str(value) if value else ""
                size = 28
                if len(text) == 3:
                    size = 22
                elif len(text) >= 4:
                    size = 18
                label.master.config(bg=bg)
                label.config(text=text, bg=bg, fg=fg,
                             font=("Helvetica", size, "bold"))
        self.score_var.set(str(self.game.score))
        self.highest_var.set(str(self.game.highest))
        if self.game.over:
            self.status_var.set("Game over! No moves left. Press New Game to restart.")