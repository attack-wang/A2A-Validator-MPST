import tkinter as tk

from game import Board, DIFFICULTIES

NUM_COLORS = {1: "#0000FF", 2: "#008000", 3: "#FF0000", 4: "#000080",
              5: "#800000", 6: "#008080", 7: "#000000", 8: "#808080"}


class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        root.title("Minesweeper")
        self.timer_id = None
        self.level = "Beginner"

        menubar = tk.Menu(root)
        diffmenu = tk.Menu(menubar, tearoff=0)
        for name in DIFFICULTIES:
            diffmenu.add_command(label=name, command=lambda n=name: self.new_game(n))
        menubar.add_cascade(label="Difficulty", menu=diffmenu)
        root.config(menu=menubar)

        top = tk.Frame(root, bg="#bdbdbd")
        top.pack(fill="x", padx=6, pady=4)
        self.mine_label = tk.Label(top, text="010", width=4, font=("Consolas", 14, "bold"),
                                   bg="black", fg="red")
        self.mine_label.pack(side="left")
        self.face = tk.Button(top, text="\U0001F642", width=3, font=("Arial", 14),
                              command=self.new_game)
        self.face.pack(side="left", padx=12)
        self.time_label = tk.Label(top, text="000", width=4, font=("Consolas", 14, "bold"),
                                   bg="black", fg="red")
        self.time_label.pack(side="right")

        self.board_frame = tk.Frame(root, bg="#bdbdbd", relief="groove", borderwidth=3)
        self.board_frame.pack(padx=6, pady=6)
        self.new_game("Beginner")

    def new_game(self, level=None):
        if level is None:
            level = self.level
        self.level = level
        rows, cols, mines = DIFFICULTIES[level]
        self.board = Board(rows, cols, mines)
        self.time = 0
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.face.config(text="\U0001F642")
        self.time_label.config(text="000")
        self.update_status()
        for w in self.board_frame.winfo_children():
            w.destroy()
        self.buttons = []
        for r in range(rows):
            row = []
            for c in range(cols):
                b = tk.Button(self.board_frame, width=2, height=1,
                              font=("Arial", 10, "bold"), bg="#bdbdbd", relief="raised")
                b.grid(row=r, column=c)
                b.bind("<Button-1>", lambda e, r=r, c=c: self.left_click(r, c))
                b.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))
                b.bind("<Button-2>", lambda e, r=r, c=c: self.right_click(r, c))
                row.append(b)
            self.buttons.append(row)
        self.root.geometry("")
        self.start_timer()

    def start_timer(self):
        def tick():
            if self.board.game_over:
                return
            self.time += 1
            self.time_label.config(text=f"{min(self.time, 999):03d}")
            self.timer_id = self.root.after(1000, tick)
        self.timer_id = self.root.after(1000, tick)

    def update_status(self):
        remaining = self.board.mines - self.board.flags_used
        if remaining >= 0:
            self.mine_label.config(text=f"{remaining:03d}")
        else:
            self.mine_label.config(text=f"-{min(-remaining, 99):02d}")

    def left_click(self, r, c):
        self.board.reveal(r, c)
        self.refresh()
        if self.board.game_over:
            self.end_game()

    def right_click(self, r, c):
        self.board.toggle_flag(r, c)
        self.update_status()
        self.refresh()

    def refresh(self):
        lost = self.board.game_over and not self.board.won
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                b = self.buttons[r][c]
                if cell.revealed:
                    b.config(relief="flat", bg="#d9d9d9", fg="black")
                    if cell.mine:
                        b.config(text="\U0001F4A5", bg="#FF0000")
                    elif cell.adjacent:
                        b.config(text=str(cell.adjacent), fg=NUM_COLORS[cell.adjacent])
                    else:
                        b.config(text="")
                elif cell.flagged:
                    if lost and not cell.mine:
                        b.config(text="\u274C", bg="#FFD700", relief="raised")
                    else:
                        b.config(text="\U0001F6A9", bg="#FFD700", relief="raised")
                else:
                    b.config(text="", bg="#bdbdbd", relief="raised")

    def end_game(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        if self.board.won:
            self.face.config(text="\U0001F60E")
            self.mine_label.config(text="000")
        else:
            self.face.config(text="\U0001F635")