import tkinter as tk

from game import Board, DIFFICULTIES

NUMBER_COLORS = {1: "#0000FF", 2: "#008000", 3: "#FF0000", 4: "#000080",
                 5: "#800000", 6: "#008080", 7: "#000000", 8: "#808080"}


class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        root.title("Minesweeper")
        self.cell_size = 28
        top = tk.Frame(root)
        top.pack(fill="x", padx=4, pady=4)
        self.mine_label = tk.Label(top, font=("Arial", 12, "bold"))
        self.mine_label.pack(side="left")
        self.diff_var = tk.StringVar(value="Beginner")
        tk.OptionMenu(top, self.diff_var, *DIFFICULTIES.keys(),
                      command=lambda _d: self.new_game()).pack(side="left", padx=8)
        tk.Button(top, text="New Game", command=self.new_game).pack(side="left")
        self.status_label = tk.Label(top, font=("Arial", 12, "bold"), width=12)
        self.status_label.pack(side="right")
        self.canvas = tk.Canvas(root, bg="#bdbdbd", highlightthickness=0)
        self.canvas.pack(padx=4, pady=4)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Button-2>", self.on_right_click)
        self.new_game()

    def new_game(self):
        rows, cols, mines = DIFFICULTIES[self.diff_var.get()]
        self.board = Board(rows, cols, mines)
        self.canvas.config(width=cols * self.cell_size,
                           height=rows * self.cell_size)
        self.status_label.config(text="", fg="black")
        self.draw()

    def cell_at(self, event):
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        if self.board.in_bounds(r, c):
            return r, c
        return None

    def on_left_click(self, event):
        pos = self.cell_at(event)
        if pos:
            self.board.reveal(*pos)
            self.draw()

    def on_right_click(self, event):
        pos = self.cell_at(event)
        if pos:
            self.board.toggle_flag(*pos)
            self.draw()

    def draw(self):
        self.canvas.delete("all")
        cs = self.cell_size
        board = self.board
        for r in range(board.rows):
            for c in range(board.cols):
                x, y = c * cs, r * cs
                cell = board.cells[r][c]
                if cell.revealed:
                    fill = "#ff6666" if cell.mine else "#e0e0e0"
                    self.canvas.create_rectangle(x, y, x + cs, y + cs,
                                                 fill=fill, outline="#9e9e9e")
                    if cell.mine:
                        self.canvas.create_oval(x + cs * 0.3, y + cs * 0.3,
                                                x + cs * 0.7, y + cs * 0.7,
                                                fill="black", outline="black")
                    elif cell.adjacent:
                        self.canvas.create_text(
                            x + cs / 2, y + cs / 2, text=str(cell.adjacent),
                            font=("Arial", 12, "bold"),
                            fill=NUMBER_COLORS[cell.adjacent])
                else:
                    self.canvas.create_rectangle(x, y, x + cs, y + cs,
                                                 fill="#c0c0c0",
                                                 outline="#f5f5f5", width=2)
                    if cell.flagged:
                        self.draw_flag(x, y, cs)
        remaining = board.mine_count - board.flags_used()
        self.mine_label.config(text="Mines left: %d" % remaining)
        if board.game_over:
            if board.won:
                self.status_label.config(text="YOU WIN!", fg="green")
            else:
                self.status_label.config(text="GAME OVER", fg="red")

    def draw_flag(self, x, y, cs):
        canvas = self.canvas
        px, py = x + cs * 0.38, y + cs * 0.2
        canvas.create_line(px, py, px, y + cs * 0.8, fill="black", width=2)
        canvas.create_polygon(px, py, x + cs * 0.72, y + cs * 0.36,
                              px, y + cs * 0.52,
                              fill="red", outline="darkred")
        canvas.create_line(x + cs * 0.22, y + cs * 0.8,
                           x + cs * 0.58, y + cs * 0.8,
                           fill="black", width=2)