"""Tkinter front end: grid of clickable cells, flags, timer, mine counter."""
import time
import tkinter as tk
from tkinter import messagebox

from board import Board, DIFFICULTIES

NUMBER_COLORS = {1: "#0000FF", 2: "#008000", 3: "#FF0000", 4: "#000080",
                 5: "#800000", 6: "#008080", 7: "#000000", 8: "#808080"}
FLAG = "\U0001F6A9"
MINE = "\U0001F4A3"


class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        root.title("Minesweeper")
        self.timer_id = None
        top = tk.Frame(root)
        top.pack(pady=4)
        self.mine_label = tk.Label(top, font=("Arial", 12, "bold"))
        self.mine_label.pack(side="left", padx=8)
        self.time_label = tk.Label(top, font=("Arial", 12, "bold"))
        self.time_label.pack(side="left", padx=8)
        self.diff_var = tk.StringVar(value="Beginner")
        tk.OptionMenu(top, self.diff_var, *DIFFICULTIES,
                      command=lambda _v: self.new_game()).pack(side="left", padx=8)
        tk.Button(top, text="New Game", command=self.new_game).pack(side="left", padx=8)
        self.frame = tk.Frame(root)
        self.frame.pack(padx=8, pady=8)
        self.new_game()

    def new_game(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        rows, cols, mines = DIFFICULTIES[self.diff_var.get()]
        self.board = Board(rows, cols, mines)
        self.start_time = None
        self.elapsed = 0
        for w in self.frame.winfo_children():
            w.destroy()
        self.buttons = []
        for r in range(rows):
            row = []
            for c in range(cols):
                b = tk.Button(self.frame, width=3, relief="raised",
                              bg="#C0C0C0", font=("Arial", 10, "bold"))
                b.grid(row=r, column=c, padx=1, pady=1)
                b.bind("<Button-1>", lambda _e, r=r, c=c: self.click(r, c))
                for seq in ("<Button-2>", "<Button-3>", "<Control-Button-1>"):
                    b.bind(seq, lambda _e, r=r, c=c: self.flag(r, c))
                row.append(b)
            self.buttons.append(row)
        self.time_label.config(text="Time: 0")
        self.refresh()
        self.tick()

    def tick(self):
        if self.start_time and not self.board.game_over:
            self.elapsed = int(time.time() - self.start_time)
            self.time_label.config(text=f"Time: {self.elapsed}")
        self.timer_id = self.root.after(500, self.tick)

    def click(self, r, c):
        if self.board.game_over:
            return
        if not self.board.mines_placed:
            self.start_time = time.time()
        self.board.reveal(r, c)
        self.refresh()
        if self.board.game_over:
            self.end_game()

    def flag(self, r, c):
        if self.board.game_over:
            return
        self.board.toggle_flag(r, c)
        self.refresh()

    def refresh(self):
        """Redraw every cell so the board reflects the latest move."""
        lost = self.board.game_over and not self.board.won
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.cells[r][c]
                b = self.buttons[r][c]
                if cell.revealed:
                    if cell.mine:
                        b.config(relief="flat", text=MINE, fg="black", bg="#FF3333")
                    else:
                        b.config(relief="flat", bg="#E0E0E0",
                                 text=str(cell.adjacent) if cell.adjacent else "",
                                 fg=NUMBER_COLORS.get(cell.adjacent, "black"))
                elif cell.flagged:
                    b.config(relief="raised", text=FLAG, bg="#FFD700", fg="black")
                elif cell.mine and lost:
                    b.config(relief="flat", text=MINE, bg="#FF9999", fg="black")
                else:
                    b.config(relief="raised", text="", bg="#C0C0C0", fg="black")
        self.mine_label.config(
            text=f"Mines: {self.board.mine_count - self.board.flags_used()}")

    def end_game(self):
        if self.board.won:
            msg = f"You cleared the board in {self.elapsed}s! Play again?"
        else:
            msg = "Boom! You hit a mine. Play again?"
        if messagebox.askyesno("Minesweeper", msg):
            self.new_game()