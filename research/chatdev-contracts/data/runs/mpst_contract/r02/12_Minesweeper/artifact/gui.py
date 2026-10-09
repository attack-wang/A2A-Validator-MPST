import tkinter as tk

import game

NUMBER_COLORS = {1: "#0000FF", 2: "#008000", 3: "#FF0000", 4: "#000080",
                 5: "#800000", 6: "#008080", 7: "#000000", 8: "#606060"}
FLAG_SYMBOL = "\u2691"
MINE_SYMBOL = "\u2739"
HIDDEN_BG = "#9E9E9E"
REVEALED_BG = "#E0E0E0"
FLAG_BG = "#FFD54F"
MINE_BG = "#EF5350"


class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        root.title("Minesweeper")
        root.resizable(False, False)
        top = tk.Frame(root)
        top.pack(pady=6, padx=8)
        self.mine_label = tk.Label(top, text="", font=("Arial", 12, "bold"),
                                   width=10, anchor="w")
        self.mine_label.pack(side=tk.LEFT, padx=6)
        self.difficulty = tk.StringVar(value="Beginner")
        tk.OptionMenu(top, self.difficulty, *game.DIFFICULTIES.keys(),
                      command=lambda _e: self.new_game()).pack(side=tk.LEFT, padx=6)
        tk.Button(top, text="New Game", command=self.new_game).pack(side=tk.LEFT, padx=6)
        self.status_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.status_label.pack()
        self.board_frame = tk.Frame(root, bd=3, relief=tk.GROOVE)
        self.board_frame.pack(padx=10, pady=6)
        tk.Label(root, text="Left-click: reveal   Right-click: flag",
                 fg="#555555").pack(pady=(0, 6))
        self.buttons = []
        self.new_game()

    def new_game(self):
        rows, cols, mines = game.DIFFICULTIES[self.difficulty.get()]
        self.logic = game.Minesweeper(rows, cols, mines)
        self.status_label.config(text="")
        for child in self.board_frame.winfo_children():
            child.destroy()
        self.buttons = []
        for r in range(rows):
            row = []
            for c in range(cols):
                btn = tk.Button(self.board_frame, width=3, height=1,
                                font=("Arial", 10, "bold"), bg=HIDDEN_BG,
                                relief=tk.RAISED,
                                command=lambda r=r, c=c: self.on_reveal(r, c))
                btn.grid(row=r, column=c)
                btn.bind("<Button-3>", lambda _e, r=r, c=c: self.on_flag(r, c))
                btn.bind("<Button-2>", lambda _e, r=r, c=c: self.on_flag(r, c))
                row.append(btn)
            self.buttons.append(row)
        self.refresh()

    def on_reveal(self, r, c):
        self.logic.reveal(r, c)
        self.refresh()

    def on_flag(self, r, c):
        self.logic.toggle_flag(r, c)
        self.refresh()

    def refresh(self):
        logic = self.logic
        for r in range(logic.rows):
            for c in range(logic.cols):
                cell = logic.board[r][c]
                btn = self.buttons[r][c]
                if cell.revealed and cell.mine and not cell.flagged:
                    btn.config(text=MINE_SYMBOL, bg=MINE_BG,
                               relief=tk.FLAT, fg="black")
                elif cell.revealed:
                    btn.config(text=str(cell.adjacent) if cell.adjacent else "",
                               bg=REVEALED_BG, relief=tk.FLAT,
                               fg=NUMBER_COLORS.get(cell.adjacent, "black"))
                elif cell.flagged:
                    btn.config(text=FLAG_SYMBOL, bg=FLAG_BG,
                               relief=tk.RAISED, fg="black")
                else:
                    btn.config(text="", bg=HIDDEN_BG,
                               relief=tk.RAISED, fg="black")
        self.mine_label.config(text="Mines: %d" % logic.remaining_mines())
        if logic.state == "won":
            self.status_label.config(text="You cleared the field. You win!",
                                     fg="green")
        elif logic.state == "lost":
            self.status_label.config(text="Boom! You uncovered a mine. Game over.",
                                     fg="red")