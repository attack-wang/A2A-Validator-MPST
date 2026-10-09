import tkinter as tk
from tkinter import messagebox

from game import MinesweeperGame, DIFFICULTIES

NUMBER_COLORS = {1: "blue", 2: "green", 3: "red", 4: "purple",
                 5: "maroon", 6: "teal", 7: "black", 8: "gray"}


class MinesweeperUI:
    def __init__(self, root):
        self.root = root
        root.title("Minesweeper")
        self.default_bg = None
        self.buttons = []
        self.build_top_bar()
        self.board_frame = tk.Frame(root, bd=3, relief="groove")
        self.board_frame.pack(padx=5, pady=5)
        self.new_game("Beginner")

    def build_top_bar(self):
        bar = tk.Frame(self.root)
        bar.pack(fill="x", padx=5, pady=5)
        self.mine_label = tk.Label(bar, text="Mines: 0", font=("Arial", 11, "bold"))
        self.mine_label.pack(side="left", padx=5)
        for name in DIFFICULTIES:
            tk.Button(bar, text=name,
                      command=lambda n=name: self.new_game(n)).pack(side="left", padx=2)
        self.status_label = tk.Label(bar, text="", font=("Arial", 11, "bold"))
        self.status_label.pack(side="right", padx=5)

    def new_game(self, level):
        rows, cols, mines = DIFFICULTIES[level]
        self.game = MinesweeperGame(rows, cols, mines)
        self.status_label.config(text="")
        self.build_board()
        self.update_display()

    def build_board(self):
        for w in self.board_frame.winfo_children():
            w.destroy()
        self.buttons = []
        for r in range(self.game.rows):
            row = []
            for c in range(self.game.cols):
                b = tk.Button(self.board_frame, width=3, height=1,
                              font=("Arial", 9, "bold"),
                              command=lambda r=r, c=c: self.on_left_click(r, c))
                b.grid(row=r, column=c)
                b.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                row.append(b)
            self.buttons.append(row)
        self.default_bg = self.buttons[0][0].cget("bg")

    def on_left_click(self, r, c):
        self.game.reveal(r, c)
        self.update_display()
        if self.game.game_over:
            self.end_game()

    def on_right_click(self, r, c):
        self.game.toggle_flag(r, c)
        self.update_display()

    def update_display(self):
        g = self.game
        self.mine_label.config(text="Mines: {}".format(g.mines - g.flags_used()))
        for r in range(g.rows):
            for c in range(g.cols):
                cell = g.cells[r][c]
                b = self.buttons[r][c]
                if cell.revealed:
                    if cell.mine:
                        b.config(text="*", bg="red", fg="white", relief="sunken")
                    else:
                        b.config(text=str(cell.adjacent) if cell.adjacent else "",
                                 bg="lightgray", relief="sunken",
                                 fg=NUMBER_COLORS.get(cell.adjacent, "black"))
                elif cell.flagged:
                    b.config(text="F", bg="yellow", fg="red", relief="raised")
                else:
                    b.config(text="", bg=self.default_bg, fg="black", relief="raised")

    def end_game(self):
        if self.game.won:
            self.status_label.config(text="You win!")
            messagebox.showinfo("Minesweeper", "Congratulations! You cleared the field.")
        else:
            self.game.reveal_all_mines()
            self.update_display()
            self.status_label.config(text="Game over!")
            messagebox.showinfo("Minesweeper", "Boom! You hit a mine.")