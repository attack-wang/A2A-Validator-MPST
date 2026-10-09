"""Tkinter GUI for Minesweeper."""
import tkinter as tk
from game import Board, DIFFICULTIES

NUMBER_COLORS = {1: "#0000FF", 2: "#008000", 3: "#FF0000", 4: "#000080",
                 5: "#800000", 6: "#008080", 7: "#000000", 8: "#808080"}
HIDDEN_BG = "#BDBDBD"
REVEALED_BG = "#E0E0E0"
FLAG_BG = "#FFD966"
MINE_BG = "#F0F0F0"
HIT_BG = "#FF5555"


class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        root.title("Minesweeper")
        root.resizable(False, False)
        top = tk.Frame(root)
        top.pack(fill="x", padx=6, pady=4)
        self.mine_label = tk.Label(top, font=("Arial", 13, "bold"), fg="#B30000")
        self.mine_label.pack(side="left")
        self.new_button = tk.Button(top, text="New Game", command=self.new_game)
        self.new_button.pack(side="left", padx=10)
        self.status_label = tk.Label(top, font=("Arial", 13, "bold"))
        self.status_label.pack(side="left")
        self.time_label = tk.Label(top, font=("Arial", 13, "bold"), width=4)
        self.time_label.pack(side="right")
        self.diff_var = tk.StringVar(value="Beginner")
        tk.OptionMenu(top, self.diff_var, *DIFFICULTIES,
                      command=lambda _e: self.new_game()).pack(side="right")
        self.board_frame = tk.Frame(root, bd=3, relief="groove")
        self.board_frame.pack(padx=6, pady=6)
        self.buttons = []
        self.timer_id = None
        self.time = 0
        self.new_game()

    def new_game(self):
        rows, cols, mines = DIFFICULTIES[self.diff_var.get()]
        self.board = Board(rows, cols, mines)
        self._stop_timer()
        self.time = 0
        self.time_label.config(text="000")
        self.status_label.config(text="")
        self._build_grid()
        self._refresh()

    def _build_grid(self):
        for w in self.board_frame.winfo_children():
            w.destroy()
        self.buttons = []
        for r in range(self.board.rows):
            row = []
            for c in range(self.board.cols):
                btn = tk.Button(self.board_frame, width=2, height=1,
                                font=("Arial", 11, "bold"), bg=HIDDEN_BG,
                                relief="raised")
                btn.grid(row=r, column=c)
                btn.bind("<Button-1>", lambda _e, r=r, c=c: self._uncover(r, c))
                btn.bind("<Button-3>", lambda _e, r=r, c=c: self._flag(r, c))
                btn.bind("<Button-2>", lambda _e, r=r, c=c: self._flag(r, c))
                row.append(btn)
            self.buttons.append(row)

    def _start_timer(self):
        if self.timer_id is None:
            self._tick()

    def _tick(self):
        self.time += 1
        self.time_label.config(text=str(min(self.time, 999)).zfill(3))
        self.timer_id = self.root.after(1000, self._tick)

    def _stop_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def _uncover(self, r, c):
        if self.board.game_over:
            return
        if not self.board.started:
            self._start_timer()
        self.board.reveal(r, c)
        self._refresh()
        if self.board.game_over:
            self._stop_timer()
            self.status_label.config(
                text="You Win! 🎉" if self.board.won else "Boom! Game Over 💥",
                fg="#008000" if self.board.won else "#B30000")

    def _flag(self, r, c):
        if self.board.game_over:
            return
        if not self.board.started:
            self._start_timer()
        self.board.toggle_flag(r, c)
        self._refresh()

    def _refresh(self):
        b = self.board
        self.mine_label.config(text=f"💣 {b.mines - b.flags}")
        for r in range(b.rows):
            for c in range(b.cols):
                cell = b.grid[r][c]
                btn = self.buttons[r][c]
                if cell.revealed:
                    if cell.mine:
                        btn.config(text="💣",
                                   bg=HIT_BG if b.hit == (r, c) else MINE_BG,
                                   relief="sunken")
                    else:
                        n = cell.adjacent
                        btn.config(text=str(n) if n else "", bg=REVEALED_BG,
                                   fg=NUMBER_COLORS.get(n, "#000000"),
                                   relief="sunken")
                elif cell.flagged:
                    lost = b.game_over and not b.won and not cell.mine
                    btn.config(text="❌" if lost else "🚩", bg=FLAG_BG,
                               relief="raised")
                else:
                    btn.config(text="", bg=HIDDEN_BG, relief="raised")