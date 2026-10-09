import random
import tkinter as tk

LEVELS = {"Beginner": (9, 9, 10), "Intermediate": (16, 16, 40), "Expert": (30, 16, 99)}
NUM_COLORS = {1: "#0000ff", 2: "#008000", 3: "#ff0000", 4: "#000080",
              5: "#800000", 6: "#008080", 7: "#000000", 8: "#696969"}
HIDDEN_BG = "#c6c6c6"
REVEALED_BG = "#e6e6e6"
FLAG_BG = "#ffe08a"
FLAG_FG = "#d40000"


class Cell:
    __slots__ = ("mine", "revealed", "flag", "adj", "btn")

    def __init__(self):
        self.mine = False
        self.revealed = False
        self.flag = False
        self.adj = 0
        self.btn = None


class Minesweeper:
    def __init__(self, root):
        self.root = root
        root.title("Minesweeper")
        root.resizable(False, False)
        top = tk.Frame(root)
        top.pack(pady=4)
        self.level_var = tk.StringVar(value="Beginner")
        for name in LEVELS:
            tk.Radiobutton(top, text=name, variable=self.level_var,
                           value=name, command=self.new_game).pack(side="left", padx=4)
        tk.Button(top, text="New Game", command=self.new_game).pack(side="left", padx=10)
        self.status = tk.Label(root, font=("Arial", 12, "bold"))
        self.status.pack(pady=2)
        self.frame = tk.Frame(root, bd=3, relief="sunken")
        self.frame.pack(padx=8, pady=8)
        self.new_game()

    def new_game(self):
        self.cols, self.rows, self.mines = LEVELS[self.level_var.get()]
        self.over = False
        self.first = True
        self.cells = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        for w in self.frame.winfo_children():
            w.destroy()
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.frame, width=2, height=1, relief="raised",
                                bg=HIDDEN_BG, font=("Arial", 10, "bold"))
                btn.grid(row=r, column=c)
                btn.bind("<Button-1>", lambda e, r=r, c=c: self.reveal(r, c))
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.toggle_flag(r, c))
                btn.bind("<Button-2>", lambda e, r=r, c=c: self.toggle_flag(r, c))
                self.cells[r][c].btn = btn
        self.set_status("Left-click: reveal   Right-click: flag")

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr or dc:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        yield nr, nc

    def place_mines(self, sr, sc):
        safe = {(sr, sc)} | set(self.neighbors(sr, sc))
        spots = [(r, c) for r in range(self.rows) for c in range(self.cols)
                 if (r, c) not in safe]
        random.shuffle(spots)
        for r, c in spots[:self.mines]:
            self.cells[r][c].mine = True
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].adj = sum(self.cells[nr][nc].mine
                                           for nr, nc in self.neighbors(r, c))

    def reveal(self, r, c):
        if self.over:
            return
        cell = self.cells[r][c]
        if cell.revealed or cell.flag:
            return
        if self.first:
            self.place_mines(r, c)
            self.first = False
        if cell.mine:
            self.game_over(cell)
            return
        self.flood(r, c)
        self.check_win()

    def flood(self, r, c):
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            cell = self.cells[cr][cc]
            if cell.revealed or cell.flag or cell.mine:
                continue
            cell.revealed = True
            cell.btn.config(relief="flat", bg=REVEALED_BG,
                            text=str(cell.adj) if cell.adj else "",
                            fg=NUM_COLORS.get(cell.adj, "#000000"))
            if cell.adj == 0:
                stack.extend((nr, nc) for nr, nc in self.neighbors(cr, cc)
                             if not self.cells[nr][nc].revealed)

    def toggle_flag(self, r, c):
        if self.over:
            return
        cell = self.cells[r][c]
        if cell.revealed:
            return
        cell.flag = not cell.flag
        if cell.flag:
            cell.btn.config(text="⚑", fg=FLAG_FG, bg=FLAG_BG)
        else:
            cell.btn.config(text="", fg="#000000", bg=HIDDEN_BG)
        self.set_status()

    def game_over(self, hit):
        self.over = True
        for row in self.cells:
            for cell in row:
                if cell.mine and not cell.flag:
                    cell.btn.config(text="●", fg="#000000",
                                    bg="#ff6b6b" if cell is hit else "#9e9e9e")
                elif not cell.mine and cell.flag:
                    cell.btn.config(text="✗", fg="#ff0000")
        self.set_status("BOOM! You hit a mine — Game Over")

    def check_win(self):
        hidden = sum(1 for row in self.cells for cell in row if not cell.revealed)
        if hidden != self.mines:
            return
        self.over = True
        for row in self.cells:
            for cell in row:
                if cell.mine and not cell.flag:
                    cell.btn.config(text="⚑", fg=FLAG_FG, bg="#88dd88")
        self.set_status("You win! All mines located!")

    def set_status(self, msg=None):
        flags = sum(1 for row in self.cells for cell in row if cell.flag)
        text = "Mines left: {}".format(self.mines - flags)
        if msg:
            text += "    |    " + msg
        self.status.config(text=text)


def main():
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()


if __name__ == "__main__":
    main()