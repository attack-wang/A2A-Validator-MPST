# gui.py
'''
Tkinter GUI for the 2048 game.
'''
import tkinter as tk
# Colors
BG_COLOR = "#faf8ef"
EMPTY_COLOR = "#cdc1b4"
GRID_BG = "#bbada0"
SCORE_BG = "#bbada0"
SCORE_FG = "#776e65"
TEXT_COLOR = "#776e65"
TILE_COLORS = {
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
DEFAULT_TILE_COLOR = ("#3c3a32", "#f9f6f2")  # for tiles > 2048
class Game2048GUI:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.cell_size = 100
        self.padding = 10
        master.title("2048")
        master.resizable(False, False)
        master.configure(bg=BG_COLOR)
        self._build_ui()
        self.update_display()
    def _build_ui(self):
        # Header: title, score, highest tile, new game button
        header = tk.Frame(self.master, bg=BG_COLOR)
        header.pack(pady=(15, 5), padx=15, fill="x")
        title = tk.Label(header, text="2048", font=("Helvetica", 40, "bold"), bg=BG_COLOR, fg="#776e65")
        title.pack(side="left")
        scores = tk.Frame(header, bg=BG_COLOR)
        scores.pack(side="right")
        self.score_var = tk.StringVar(value="0")
        self.highest_var = tk.StringVar(value="0")
        score_box = tk.Frame(scores, bg=SCORE_BG, padx=15, pady=5)
        score_box.pack(side="left", padx=5)
        tk.Label(score_box, text="SCORE", font=("Helvetica", 10, "bold"), bg=SCORE_BG, fg="#eee4da").pack()
        tk.Label(score_box, textvariable=self.score_var, font=("Helvetica", 16, "bold"), bg=SCORE_BG, fg="white").pack()
        highest_box = ...
        new_game_btn = tk.Button(...)
        # Grid
        self.grid_frame = tk.Frame(self.master, bg=GRID_BG)
        self.grid_frame.pack(padx=15, pady=10)
        self.cell_labels = []
        for r in range(self.game.size):
            row_labels = []
            for c in range(self.game.size):
                cell = tk.Label(self.grid_frame, text="", width=4, height=2, font=("Helvetica", 28, "bold"), bg=EMPTY_COLOR)
                cell.grid(row=r, column=c, padx=5, pady=5)
                row_labels.append(cell)
            self.cell_labels.append(row_labels)
        # Instructions
        instructions = tk.Label(self.master, text="Use arrow keys to slide tiles. Merge equal tiles to reach 2048!", ...)
        # Key bindings
        self.master.bind("<Key>", self.on_key)
        # Or specific arrow bindings
    def on_key(self, event):
        key = event.keysym
        direction_map = {
            "Up": "up", "Down": "down", "Left": "left", "Right": "right",
            "w": "up", "s": "down", "a": "left", "d": "right",
            "W": "up", "S": "down", "A": "left", "D": "right",
        }
        if key in direction_map:
            moved = self.game.move(direction_map[key])
            if moved:
                self.update_display()
                if self.game.game_over:
                    self.show_game_over()
            return "break"
    def update_display(self):
        for r in range(self.game.size):
            for c in range(self.game.size):
                value = self.game.board[r][c]
                label = self.cell_labels[r][c]
                if value == 0:
                    label.config(text="", bg=EMPTY_COLOR, fg=EMPTY_COLOR)
                else:
                    bg, fg = TILE_COLORS.get(value, DEFAULT_TILE_COLOR)
                    label.config(text=str(value), bg=bg, fg=fg)
        self.score_var.set(str(self.game.score))
        self.highest_var.set(str(self.game.highest_tile))
    def show_game_over(self):
        overlay = tk.Frame(self.grid_frame, bg="#eee4da")
        # place over grid
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(overlay, text="Game Over!", ...).pack()
        tk.Button(overlay, text="Try Again", command=self.restart).pack()
    def restart(self):
        self.game.reset()
        self.update_display()
        # remove overlay