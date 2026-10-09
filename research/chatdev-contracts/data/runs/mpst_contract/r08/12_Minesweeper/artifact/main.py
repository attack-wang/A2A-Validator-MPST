import tkinter as tk
import random

LEVELS = {"Beginner": (9, 9, 10), "Intermediate": (16, 16, 40), "Expert": (30, 16, 99)}
NUM_COLORS = {1: "blue", 2: "green", 3: "red", 4: "purple",
              5: "maroon", 6: "teal", 7: "black", 8: "gray"}


class Minesweeper:
    def __init__(self, root):
        self.root = root
        root.title("Minesweeper")
        top = tk.Frame(root)
        top.pack(pady=4)
        self.level_var = tk.StringVar(value="Beginner")
        for name in LEVELS:
            tk.Radiobutton(top, text=name, variable=self.level_var, value=name,
                           command=self.new_game).pack(side=tk.LEFT, padx=4)
        tk.Button(top, text="New Game", command=self.new_game).pack(side=tk.LEFT, padx=8)
        self.status = tk.Label(root, font=("Arial", 12, "bold"))
        self.status.pack()
        self.frame = tk.Frame(root)
        self.frame.pack(padx=8, pady=4)
        self.new_game()

    def new_game(self):
        self.cols, self.rows, self.mines = LEVELS[self.level_var.get()]
        self.over = False
        self.first_click = True
        self.mine_set = set()
        self.flags = set()
        self.revealed = set()
        self.status.config(text="Mines: %d" % self.mines, fg="black")
        for w in self.frame.winfo_children():
            w.destroy()
        self.cells = {}
        self.default_bg = None
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.frame, width=3, height=1, font=("Arial", 10, "bold"),
                                command=lambda r=r, c=c: self.reveal(r, c))
                if self.default_bg is None:
                    self.default_bg = btn.cget("bg")
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.toggle_flag(r, c))
                btn.grid(row=r, column=c)
                self.cells[(r, c)] = btn

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if (dr or dc) and 0 <= r + dr < self.rows and 0 <= c + dc < self.cols:
                    yield r + dr, c + dc

    def place_mines(self, safe):
        pool = [(r, c) for r in range(self.rows) for c in range(self.cols) if (r, c) not in safe]
        self.mine_set = set(random.sample(pool, self.mines))

    def adjacent(self, r, c):
        return sum(1 for n in self.neighbors(r, c) if n in self.mine_set)

    def reveal(self, r, c):
        if self.over or (r, c) in self.flags or (r, c) in self.revealed:
            return
        if self.first_click:
            self.place_mines({(r, c)})
            self.first_click = False
        if (r, c) in self.mine_set:
            self.lose(r, c)
            return
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            if (cr, cc) in self.revealed or (cr, cc) in self.flags:
                continue
            self.revealed.add((cr, cc))
            n = self.adjacent(cr, cc)
            self.cells[(cr, cc)].config(relief=tk.FLAT, bg="#e6e6e6",
                                        text=str(n) if n else "",
                                        fg=NUM_COLORS.get(n, "black"))
            if n == 0:
                stack.extend(self.neighbors(cr, cc))
        self.check_win()

    def toggle_flag(self, r, c):
        if self.over or (r, c) in self.revealed:
            return
        btn = self.cells[(r, c)]
        if (r, c) in self.flags:
            self.flags.discard((r, c))
            btn.config(text="", bg=self.default_bg)
        else:
            self.flags.add((r, c))
            btn.config(text="\U0001F6A9", bg="#ffd966", fg="red")
        self.status.config(text="Mines: %d" % (self.mines - len(self.flags)))

    def lose(self, r, c):
        self.over = True
        self.cells[(r, c)].config(text="\U0001F4A5", bg="red")
        for m in self.mine_set:
            if m != (r, c):
                self.cells[m].config(text="\U0001F4A3", bg="#cccccc")
        self.status.config(text="Game Over - you hit a mine!", fg="red")

    def check_win(self):
        if len(self.revealed) == self.rows * self.cols - self.mines:
            self.over = True
            for m in self.mine_set:
                self.cells[m].config(text="\U0001F6A9", bg="#90ee90")
            self.status.config(text="You Win - all mines located!", fg="green")


if __name__ == "__main__":
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()