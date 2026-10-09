"""Tkinter GUI for Minesweeper: board rendering, clicks, flags, status."""
import tkinter as tk
from tkinter import messagebox

from game import MinesweeperGame, DIFFICULTIES

NUMBER_COLORS = {1: "#0000FF", 2: "#008000", 3: "#FF0000", 4: "#000080",
                 5: "#800000", 6: "#008080", 7: "#000000", 8: "#808080"}
COVERED_BG = "#BDBDBD"
REVEALED_BG = "#E0E0E0"
FLAG_BG = "#FFD700"
FLAG_FG = "#CC0000"
MINE_BG = "#FF6666"


class MinesweeperUI:
    def __init__(self, root):
        self.root = root
        root.title("Minesweeper")
        self.finished = False
        self.diff_var = tk.StringVar(value="Beginner")
        self.build_menu()
        self.new_game()

    def build_menu(self):
        bar = tk.Frame(self.root)
        bar.pack(fill=tk.X, pady=2)
        tk.Label(bar, text="Difficulty:").pack(side=tk.LEFT, padx=4)
        for name in DIFFICULTIES:
            tk.Radiobutton(bar, text=name, variable=self.diff_var, value=name,
                           command=self.new_game).pack(side=tk.LEFT)
        tk.Button(bar, text="New Game", command=self.new_game).pack(side=tk.LEFT, padx=8)
        self.status_label = tk.Label(bar, text="", font=("Arial", 10, "bold"))
        self.status_label.pack(side=tk.RIGHT, padx=8)

    def new_game(self):
        rows, cols, mines = DIFFICULTIES[self.diff_var.get()]
        self.game = MinesweeperGame(rows, cols, mines)
        self.finished = False
        self.build_board()
        self.refresh()

    def build_board(self):
        if hasattr(self, "frame"):
            self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=4, pady=4)
        self.buttons = []
        for r in range(self.game.rows):
            row = []
            for c in range(self.game.cols):
                btn = tk.Button(self.frame, width=2, height=1, bg=COVERED_BG,
                                font=("Arial", 10, "bold"),
                                command=lambda r=r, c=c: self.on_left_click(r, c))
                btn.grid(row=r, column=c)
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                row.append(btn)
            self.buttons.append(row)

    def on_left_click(self, r, c):
        self.game.reveal(r, c)
        self.refresh()
        if self.game.game_over and not self.finished:
            self.finished = True
            self.end_game()

    def on_right_click(self, r, c):
        self.game.toggle_flag(r, c)
        self.refresh()

    def refresh(self):
        """Redraw the whole board with updated markings after each move."""
        g = self.game
        for r in range(g.rows):
            for c in range(g.cols):
                btn = self.buttons[r][c]
                if g.revealed[r][c]:
                    v = g.board[r][c]
                    if v == -1:
                        btn.config(text="*", bg=MINE_BG, relief=tk.SUNKEN, fg="black")
                    else:
                        btn.config(text=str(v) if v else "", bg=REVEALED_BG,
                                   relief=tk.SUNKEN, fg=NUMBER_COLORS.get(v, "black"))
                elif g.flagged[r][c]:
                    btn.config(text="F", bg=FLAG_BG, fg=FLAG_FG, relief=tk.RAISED)
                elif g.game_over and not g.won and g.board[r][c] == -1:
                    btn.config(text="*", bg=MINE_BG, relief=tk.SUNKEN, fg="black")
                else:
                    btn.config(text="", bg=COVERED_BG, relief=tk.RAISED, fg="black")
        remaining = g.mines - g.flags_used()
        self.status_label.config(text="Mines left: {}".format(remaining))

    def end_game(self):
        if self.game.won:
            messagebox.showinfo("Minesweeper", "You won! Congratulations!")
        else:
            messagebox.showinfo("Minesweeper", "Boom! You hit a mine. Game over.")