import tkinter as tk
from tkinter import messagebox

from game import Minesweeper, DIFFICULTIES

NUM_COLORS = {1: "#0000FF", 2: "#008000", 3: "#FF0000", 4: "#000080",
              5: "#800000", 6: "#008080", 7: "#000000", 8: "#808080"}
HIDDEN_BG = "#BDBDBD"
REVEALED_BG = "#E8E8E8"
FLAG_BG = "#FFD966"
MINE_BG = "#FF5555"


class MinesweeperGUI:
    """Tkinter front-end for Minesweeper."""

    def __init__(self, root):
        self.root = root
        root.title("Minesweeper")
        top = tk.Frame(root)
        top.pack(pady=4)
        self.mine_label = tk.Label(top, text="Mines: 0",
                                   font=("Arial", 12, "bold"), width=10)
        self.mine_label.pack(side="left", padx=8)
        for name in DIFFICULTIES:
            tk.Button(top, text=name,
                      command=lambda n=name: self.new_game(n)).pack(side="left", padx=3)
        self.status = tk.Label(root, text="", font=("Arial", 12))
        self.status.pack(pady=2)
        self.board = tk.Frame(root)
        self.board.pack(padx=8, pady=8)
        self.buttons = []
        self.game = None
        self.new_game("Beginner")

    def new_game(self, level):
        rows, cols, mines = DIFFICULTIES[level]
        self.game = Minesweeper(rows, cols, mines)
        for w in self.board.winfo_children():
            w.destroy()
        self.buttons = []
        for r in range(rows):
            row = []
            for c in range(cols):
                btn = tk.Button(self.board, width=2, height=1,
                                font=("Arial", 11, "bold"), bg=HIDDEN_BG)
                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.bind("<Button-1>", lambda e, rr=r, cc=c: self.on_left(rr, cc))
                btn.bind("<Button-3>", lambda e, rr=r, cc=c: self.on_right(rr, cc))
                btn.bind("<Button-2>", lambda e, rr=r, cc=c: self.on_right(rr, cc))
                row.append(btn)
            self.buttons.append(row)
        self.status.config(text=f"{level} - Left-click: uncover | Right-click: flag")
        self.update_all()

    def on_left(self, r, c):
        if self.game.game_over:
            return
        changed = self.game.reveal(r, c)
        if not changed:
            return
        self.update_all()
        if self.game.won:
            self.status.config(text="You win! All mines flagged.")
            messagebox.showinfo("Minesweeper", "Congratulations, you cleared the board!")
        elif self.game.grid[r][c].mine:
            self.status.config(text="Boom! You hit a mine. Game over.")
            messagebox.showerror("Minesweeper", "You hit a mine. Game over!")

    def on_right(self, r, c):
        if self.game.toggle_flag(r, c):
            self.paint(r, c)
            self.update_mine_label()

    def paint(self, r, c):
        cell = self.game.grid[r][c]
        btn = self.buttons[r][c]
        if cell.revealed:
            if cell.mine:
                btn.config(text="*", bg=MINE_BG, relief="sunken", fg="#000000")
            else:
                btn.config(text=str(cell.adjacent) if cell.adjacent else "",
                           bg=REVEALED_BG, relief="sunken",
                           fg=NUM_COLORS.get(cell.adjacent, "#000000"))
        elif cell.flagged:
            wrong = self.game.game_over and not self.game.won and not cell.mine
            btn.config(text="F", bg=FLAG_BG, relief="raised",
                       fg="#CC0000" if wrong else "#006400")
        else:
            if self.game.game_over and not self.game.won and cell.mine:
                btn.config(text="*", bg="#FF9999", relief="raised", fg="#000000")
            else:
                btn.config(text="", bg=HIDDEN_BG, relief="raised", fg="#000000")

    def update_all(self):
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                self.paint(r, c)
        self.update_mine_label()

    def update_mine_label(self):
        self.mine_label.config(text=f"Mines: {self.game.mines - self.game.flags_used}")