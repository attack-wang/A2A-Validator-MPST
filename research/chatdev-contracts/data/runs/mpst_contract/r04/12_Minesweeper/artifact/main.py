import random
import time
import tkinter as tk

LEVELS = {"Beginner": (9, 9, 10), "Intermediate": (16, 16, 40), "Expert": (30, 16, 99)}
NUM_COLORS = ["#000000", "#0000ff", "#008000", "#ff0000", "#000080", "#800000", "#008080", "#000000", "#808080"]


class Cell:
    __slots__ = ("mine", "adj", "revealed", "flagged")

    def __init__(self):
        self.mine = False
        self.adj = 0
        self.revealed = False
        self.flagged = False


class Minesweeper:
    def __init__(self, root):
        self.root = root
        root.title("Minesweeper")
        top = tk.Frame(root)
        top.pack(pady=4)
        self.mine_label = tk.Label(top, font=("Arial", 14, "bold"), fg="#b00000", width=6)
        self.mine_label.pack(side="left", padx=8)
        self.face = tk.Button(top, text=":-)", width=4, font=("Arial", 11, "bold"), command=self.reset)
        self.face.pack(side="left", padx=8)
        self.time_label = tk.Label(top, font=("Arial", 14, "bold"), width=6)
        self.time_label.pack(side="left", padx=8)
        menu = tk.Frame(root)
        menu.pack(pady=2)
        for name in LEVELS:
            tk.Button(menu, text=name, command=lambda n=name: self.new_game(n)).pack(side="left", padx=4)
        self.board = tk.Frame(root)
        self.board.pack(padx=6, pady=6)
        self.new_game("Beginner")
        self.tick()

    def new_game(self, level):
        self.level = level
        self.cols, self.rows, self.mines = LEVELS[level]
        self.reset()

    def reset(self):
        self.cells = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.first = True
        self.over = False
        self.flags = 0
        self.start_time = None
        self.face.config(text=":-)")
        self.time_label.config(text="0")
        self.update_labels()
        for w in self.board.winfo_children():
            w.destroy()
        self.btns = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                b = tk.Button(self.board, width=2, height=1, bg="#bdbdbd",
                              relief="raised", font=("Arial", 10, "bold"),
                              command=lambda r=r, c=c: self.reveal(r, c))
                b.bind("<Button-3>", lambda e, r=r, c=c: self.toggle_flag(r, c))
                b.grid(row=r, column=c)
                row.append(b)
            self.btns.append(row)

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr or dc:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        yield nr, nc

    def place_mines(self, sr, sc):
        safe = {(sr, sc)} | set(self.neighbors(sr, sc))
        spots = [(r, c) for r in range(self.rows) for c in range(self.cols) if (r, c) not in safe]
        random.shuffle(spots)
        for r, c in spots[:self.mines]:
            self.cells[r][c].mine = True
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].adj = sum(self.cells[nr][nc].mine for nr, nc in self.neighbors(r, c))

    def reveal(self, r, c):
        if self.over:
            return
        cell = self.cells[r][c]
        if cell.flagged or cell.revealed:
            return
        if self.first:
            self.place_mines(r, c)
            self.first = False
            self.start_time = time.time()
        if cell.mine:
            self.game_over(r, c)
            return
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            cl = self.cells[cr][cc]
            if cl.revealed or cl.flagged:
                continue
            cl.revealed = True
            self.paint(cr, cc)
            if cl.adj == 0:
                for nr, nc in self.neighbors(cr, cc):
                    if not self.cells[nr][nc].revealed:
                        stack.append((nr, nc))
        self.check_win()

    def paint(self, r, c):
        cell = self.cells[r][c]
        b = self.btns[r][c]
        if cell.mine:
            b.config(text="\u2739", bg="#ff6666", relief="sunken")
        else:
            b.config(text=str(cell.adj) if cell.adj else "", bg="#e0e0e0",
                     relief="sunken", fg=NUM_COLORS[cell.adj])

    def toggle_flag(self, r, c):
        if self.over:
            return
        cell = self.cells[r][c]
        if cell.revealed:
            return
        cell.flagged = not cell.flagged
        self.flags += 1 if cell.flagged else -1
        if cell.flagged:
            self.btns[r][c].config(text="\u2691", bg="#ffb347", fg="#b00000")
        else:
            self.btns[r][c].config(text="", bg="#bdbdbd", fg="#000000")
        self.update_labels()

    def game_over(self, r, c):
        self.over = True
        self.face.config(text="X-(")
        for rr in range(self.rows):
            for cc in range(self.cols):
                cell = self.cells[rr][cc]
                if cell.mine and not cell.flagged:
                    self.btns[rr][cc].config(text="\u2739", relief="sunken",
                                             bg="#ff0000" if (rr, cc) == (r, c) else "#f2b0b0")
                elif not cell.mine and cell.flagged:
                    self.btns[rr][cc].config(text="\u2717", bg="#ffff66")

    def check_win(self):
        hidden = sum(1 for row in self.cells for cl in row if not cl.revealed)
        if hidden == self.mines:
            self.over = True
            self.face.config(text="8-)")
            for rr in range(self.rows):
                for cc in range(self.cols):
                    cl = self.cells[rr][cc]
                    if cl.mine and not cl.flagged:
                        self.btns[rr][cc].config(text="\u2691", bg="#ffb347", fg="#b00000")

    def update_labels(self):
        self.mine_label.config(text="\u2739 " + str(self.mines - self.flags))

    def tick(self):
        if self.start_time and not self.over:
            self.time_label.config(text=str(int(time.time() - self.start_time)))
        self.root.after(500, self.tick)


if __name__ == "__main__":
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()