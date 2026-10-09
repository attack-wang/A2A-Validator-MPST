import tkinter as tk
from tkinter import messagebox
import random

LEVELS = {"Beginner": (9, 9, 10), "Intermediate": (16, 16, 40), "Expert": (16, 30, 99)}
NUM_COLORS = {1: "#0000FF", 2: "#008000", 3: "#FF0000", 4: "#000080",
              5: "#800000", 6: "#008080", 7: "#000000", 8: "#808080"}
DEFAULT_BG = "#d9d9d9"


class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self._timer_id = None
        self._gen = 0
        menubar = tk.Menu(root)
        gmenu = tk.Menu(menubar, tearoff=0)
        for name in LEVELS:
            gmenu.add_command(label=name, command=lambda n=name: self.new_game(n))
        menubar.add_cascade(label="Game", menu=gmenu)
        root.config(menu=menubar)
        self.status = tk.Label(root, font=("Arial", 12))
        self.status.pack(pady=2)
        self.board = tk.Frame(root)
        self.board.pack()
        self.new_game("Beginner")

    def new_game(self, level):
        self._gen += 1
        if self._timer_id is not None:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
        self.level = level
        self.rows, self.cols, self.mines = LEVELS[level]
        self.first = True
        self.over = False
        self.flags = 0
        self.revealed = 0
        self.time = 0
        self.timer_on = False
        for w in self.board.winfo_children():
            w.destroy()
        self.cells = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                b = tk.Button(self.board, width=2, height=1,
                              font=("Arial", 10, "bold"), bg=DEFAULT_BG)
                b.grid(row=r, column=c)
                b.bind("<Button-1>", lambda e, r=r, c=c: self.uncover(r, c))
                b.bind("<Button-3>", lambda e, r=r, c=c: self.toggle_flag(r, c))
                row.append({"btn": b, "mine": False, "open": False,
                            "flag": False, "n": 0})
            self.cells.append(row)
        self.update_status()

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr or dc:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        yield nr, nc

    def place_mines(self, sr, sc):
        spots = [(r, c) for r in range(self.rows) for c in range(self.cols)
                 if (r, c) != (sr, sc)]
        for r, c in random.sample(spots, self.mines):
            self.cells[r][c]["mine"] = True
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c]["n"] = sum(
                    self.cells[nr][nc]["mine"] for nr, nc in self.neighbors(r, c))

    def uncover(self, r, c):
        if self.over:
            return
        cell = self.cells[r][c]
        if cell["flag"] or cell["open"]:
            return
        if self.first:
            self.place_mines(r, c)
            self.first = False
            self.timer_on = True
            self.tick()
        if cell["mine"]:
            self.game_over(False, r, c)
            return
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            cur = self.cells[cr][cc]
            if cur["open"] or cur["flag"]:
                continue
            cur["open"] = True
            self.revealed += 1
            n = cur["n"]
            cur["btn"].config(text=str(n) if n else "", relief=tk.SUNKEN,
                              bg="#e0e0e0", fg=NUM_COLORS.get(n, "black"))
            if n == 0:
                stack.extend(self.neighbors(cr, cc))
        if self.revealed == self.rows * self.cols - self.mines:
            self.game_over(True)

    def toggle_flag(self, r, c):
        if self.over:
            return
        cell = self.cells[r][c]
        if cell["open"]:
            return
        cell["flag"] = not cell["flag"]
        self.flags += 1 if cell["flag"] else -1
        cell["btn"].config(text="F" if cell["flag"] else "",
                           bg="#FF6B6B" if cell["flag"] else DEFAULT_BG,
                           fg="white" if cell["flag"] else "black")
        self.update_status()

    def update_status(self):
        self.status.config(
            text="%s  |  Mines left: %d  |  Time: %ds"
                 % (self.level, self.mines - self.flags, self.time))

    def tick(self):
        gen = self._gen
        if self.over or not self.timer_on:
            return
        self.time += 1
        self.update_status()
        self._timer_id = self.root.after(
            1000, lambda: self.tick_if_current(gen))

    def tick_if_current(self, gen):
        if gen == self._gen:
            self._timer_id = None
            self.tick()

    def game_over(self, won, hit=None):
        self.over = True
        self.timer_on = False
        if self._timer_id is not None:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.cells[r][c]
                if cell["mine"] and not cell["flag"]:
                    cell["btn"].config(text="*", fg="black",
                                       bg="#FF4444" if (r, c) == hit else "#FFB3B3")
                elif cell["flag"] and not cell["mine"]:
                    cell["btn"].config(text="X", fg="red")
        if won:
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.cells[r][c]
                    if cell["mine"] and not cell["flag"]:
                        cell["btn"].config(text="F", bg="#FF6B6B", fg="white")
            msg = "You win! All safe cells uncovered in %ds." % self.time
        else:
            msg = "Boom! You uncovered a mine. Game over."
        messagebox.showinfo("Minesweeper", msg)


if __name__ == "__main__":
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()