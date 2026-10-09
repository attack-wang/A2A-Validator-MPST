import random
import tkinter as tk

SIZE = 8
TYPES = 6
CELL = 56
START_MOVES = 30
COLORS = ["#e74c3c", "#f39c12", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6"]


class CandyGame:
    def __init__(self, root):
        self.root = root
        root.title("Candy Match 3")
        root.resizable(False, False)
        self.score_var = tk.StringVar(value="Score: 0")
        self.moves_var = tk.StringVar(value="Moves: %d" % START_MOVES)
        self.status_var = tk.StringVar(value="Swap adjacent candies to match 3+")
        bar = tk.Frame(root)
        bar.pack(fill="x", padx=10, pady=(8, 0))
        tk.Label(bar, textvariable=self.score_var, font=("Arial", 13, "bold")).pack(side="left")
        tk.Label(bar, textvariable=self.moves_var, font=("Arial", 13, "bold")).pack(side="right")
        tk.Label(root, textvariable=self.status_var, fg="#555555").pack(pady=2)
        self.canvas = tk.Canvas(root, width=SIZE * CELL, height=SIZE * CELL,
                                bg="#20232b", highlightthickness=0)
        self.canvas.pack(padx=10, pady=8)
        self.canvas.bind("<Button-1>", self.on_click)
        tk.Button(root, text="New Game", command=self.new_game).pack(pady=(0, 8))
        self.new_game()

    def new_game(self):
        while True:
            self.board = [[random.randrange(TYPES) for _ in range(SIZE)] for _ in range(SIZE)]
            if not self.find_matches() and self.has_any_move():
                break
        self.score = 0
        self.moves = START_MOVES
        self.selected = None
        self.busy = False
        self.status_var.set("Swap adjacent candies to match 3+")
        self.update_labels()
        self.draw()

    def update_labels(self):
        self.score_var.set("Score: %d" % self.score)
        self.moves_var.set("Moves: %d" % self.moves)

    def find_matches(self):
        found = set()
        for r in range(SIZE):
            for c in range(SIZE - 2):
                v = self.board[r][c]
                if v is not None and v == self.board[r][c + 1] == self.board[r][c + 2]:
                    found.update((r, c + k) for k in range(3))
        for c in range(SIZE):
            for r in range(SIZE - 2):
                v = self.board[r][c]
                if v is not None and v == self.board[r + 1][c] == self.board[r + 2][c]:
                    found.update((r + k, c) for k in range(3))
        return found

    def on_click(self, event):
        if self.busy:
            return
        r, c = event.y // CELL, event.x // CELL
        if not (0 <= r < SIZE and 0 <= c < SIZE):
            return
        if self.selected is None:
            self.selected = (r, c)
            self.draw()
            return
        sr, sc = self.selected
        if (r, c) == (sr, sc):
            self.selected = None
            self.draw()
            return
        if abs(r - sr) + abs(c - sc) != 1:
            self.selected = (r, c)
            self.draw()
            return
        self.try_swap(sr, sc, r, c)

    def try_swap(self, r1, c1, r2, c2):
        self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]
        if self.find_matches():
            self.moves -= 1
            self.selected = None
            self.busy = True
            self.update_labels()
            self.draw()
            self.resolve(1)
        else:
            self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]
            self.selected = None
            self.status_var.set("No match - swap reverted")
            self.draw()

    def resolve(self, chain):
        matches = self.find_matches()
        if not matches:
            self.busy = False
            self.after_move()
            return
        gained = len(matches) * 30 * chain
        self.score += gained
        self.status_var.set("Cleared %d candies! Chain x%d (+%d)" % (len(matches), chain, gained))
        for r, c in matches:
            self.board[r][c] = None
        self.update_labels()
        self.draw(matches)
        self.root.after(280, lambda: self.drop(chain))

    def drop(self, chain):
        for c in range(SIZE):
            col = [self.board[r][c] for r in range(SIZE) if self.board[r][c] is not None]
            missing = SIZE - len(col)
            col = [random.randrange(TYPES) for _ in range(missing)] + col
            for r in range(SIZE):
                self.board[r][c] = col[r]
        self.draw()
        self.root.after(280, lambda: self.resolve(chain + 1))

    def after_move(self):
        if self.moves <= 0:
            self.game_over()
            return
        if not self.has_any_move():
            self.busy = True
            self.status_var.set("No valid moves - shuffling board")
            self.root.after(600, self.shuffle)
        else:
            self.status_var.set("Moves left: %d" % self.moves)

    def has_any_move(self):
        for r in range(SIZE):
            for c in range(SIZE):
                for dr, dc in ((0, 1), (1, 0)):
                    r2, c2 = r + dr, c + dc
                    if r2 < SIZE and c2 < SIZE:
                        self.board[r][c], self.board[r2][c2] = self.board[r2][c2], self.board[r][c]
                        ok = bool(self.find_matches())
                        self.board[r][c], self.board[r2][c2] = self.board[r2][c2], self.board[r][c]
                        if ok:
                            return True
        return False

    def shuffle(self):
        cells = [self.board[r][c] for r in range(SIZE) for c in range(SIZE)]
        while True:
            random.shuffle(cells)
            it = iter(cells)
            self.board = [[next(it) for _ in range(SIZE)] for _ in range(SIZE)]
            if not self.find_matches() and self.has_any_move():
                break
        self.busy = False
        self.draw()

    def game_over(self):
        self.busy = True
        self.status_var.set("Game over! Press New Game to play again.")
        w = SIZE * CELL
        self.canvas.create_rectangle(w * 0.12, w * 0.32, w * 0.88, w * 0.68,
                                     fill="#111318", outline="#888888", width=2)
        self.canvas.create_text(w / 2, w * 0.44, text="GAME OVER",
                                fill="#ffffff", font=("Arial", 22, "bold"))
        self.canvas.create_text(w / 2, w * 0.58, text="Final score: %d" % self.score,
                                fill="#ffd700", font=("Arial", 16))

    def draw(self, highlight=()):
        self.canvas.delete("all")
        for r in range(SIZE):
            for c in range(SIZE):
                x1, y1 = c * CELL, r * CELL
                if (r + c) % 2 == 0:
                    self.canvas.create_rectangle(x1, y1, x1 + CELL, y1 + CELL,
                                                 fill="#2a2e39", width=0)
                v = self.board[r][c]
                if v is None:
                    continue
                m = 7
                self.canvas.create_oval(x1 + m, y1 + m, x1 + CELL - m, y1 + CELL - m,
                                        fill=COLORS[v], outline="")
                self.canvas.create_oval(x1 + m + 8, y1 + m + 8, x1 + m + 16, y1 + m + 16,
                                        fill="#ffffff", outline="", stipple="gray50")
                if (r, c) in highlight:
                    self.canvas.create_oval(x1 + 3, y1 + 3, x1 + CELL - 3, y1 + CELL - 3,
                                            outline="#ffffff", width=3)
                if self.selected == (r, c):
                    self.canvas.create_rectangle(x1 + 2, y1 + 2, x1 + CELL - 2, y1 + CELL - 2,
                                                 outline="#ffffff", width=3)


def main():
    root = tk.Tk()
    CandyGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()