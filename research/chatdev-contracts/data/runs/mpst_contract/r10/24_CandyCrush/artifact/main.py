import random
import tkinter as tk

SIZE, TYPES, MOVES, CELL = 8, 6, 30, 56
COLORS = ["#e74c3c", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6", "#e67e22"]
SYMBOLS = ["●", "■", "▲", "★", "◆", "♥"]


class Match3:
    def __init__(self, root):
        self.root = root
        root.title("Candy Match 3")
        self.status = tk.Label(root, font=("Arial", 13, "bold"))
        self.status.pack(pady=4)
        self.canvas = tk.Canvas(root, width=SIZE * CELL, height=SIZE * CELL,
                                bg="#22223b", highlightthickness=0)
        self.canvas.pack()
        tk.Button(root, text="New Game", command=self.new_game).pack(pady=4)
        self.canvas.bind("<Button-1>", self.on_click)
        self.new_game()

    def new_game(self):
        while True:
            board = [[random.randrange(TYPES) for _ in range(SIZE)] for _ in range(SIZE)]
            if not self.find_matches(board) and self.has_moves(board):
                break
        self.board = board
        self.score = 0
        self.moves = MOVES
        self.sel = None
        self.busy = False
        self.over = False
        self.update_status()
        self.draw()

    def find_matches(self, board):
        matches = set()
        for r in range(SIZE):
            c = 0
            while c < SIZE - 2:
                v = board[r][c]
                if v == board[r][c + 1] == board[r][c + 2]:
                    while c < SIZE and board[r][c] == v:
                        matches.add((r, c))
                        c += 1
                else:
                    c += 1
        for c in range(SIZE):
            r = 0
            while r < SIZE - 2:
                v = board[r][c]
                if v == board[r + 1][c] == board[r + 2][c]:
                    while r < SIZE and board[r][c] == v:
                        matches.add((r, c))
                        r += 1
                else:
                    r += 1
        return matches

    def collapse(self, board):
        for c in range(SIZE):
            col = [board[r][c] for r in range(SIZE) if board[r][c] is not None]
            col = [random.randrange(TYPES) for _ in range(SIZE - len(col))] + col
            for r in range(SIZE):
                board[r][c] = col[r]

    def has_moves(self, board):
        for r in range(SIZE):
            for c in range(SIZE):
                for dr, dc in ((0, 1), (1, 0)):
                    nr, nc = r + dr, c + dc
                    if nr < SIZE and nc < SIZE:
                        board[r][c], board[nr][nc] = board[nr][nc], board[r][c]
                        ok = bool(self.find_matches(board))
                        board[r][c], board[nr][nc] = board[nr][nc], board[r][c]
                        if ok:
                            return True
        return False

    def shuffle(self):
        vals = [v for row in self.board for v in row]
        while True:
            random.shuffle(vals)
            it = iter(vals)
            board = [[next(it) for _ in range(SIZE)] for _ in range(SIZE)]
            if not self.find_matches(board) and self.has_moves(board):
                self.board = board
                return

    def on_click(self, event):
        if self.over:
            self.new_game()
            return
        if self.busy:
            return
        c, r = event.x // CELL, event.y // CELL
        if not (0 <= r < SIZE and 0 <= c < SIZE):
            return
        if self.sel is None or self.sel == (r, c):
            self.sel = None if self.sel == (r, c) else (r, c)
        elif abs(self.sel[0] - r) + abs(self.sel[1] - c) == 1:
            sr, sc = self.sel
            b = self.board
            b[sr][sc], b[r][c] = b[r][c], b[sr][sc]
            if self.find_matches(b):
                self.moves -= 1
                self.busy = True
                self.sel = None
                self.update_status()
                self.draw()
                self.root.after(250, self.step, 0)
                return
            b[sr][sc], b[r][c] = b[r][c], b[sr][sc]
            self.sel = (r, c)
        else:
            self.sel = (r, c)
        self.draw()

    def step(self, chain):
        matches = self.find_matches(self.board)
        if not matches:
            if not self.has_moves(self.board):
                self.shuffle()
            self.busy = False
            if self.moves <= 0:
                self.over = True
            self.update_status()
            self.draw()
            return
        chain += 1
        self.score += len(matches) * 10 * chain
        for r, c in matches:
            self.board[r][c] = None
        self.update_status()
        self.draw()
        self.root.after(220, self.fall, chain)

    def fall(self, chain):
        self.collapse(self.board)
        self.draw()
        self.root.after(220, self.step, chain)

    def update_status(self):
        self.status.config(text=f"Score: {self.score}    Moves left: {self.moves}")

    def draw(self):
        cv = self.canvas
        cv.delete("all")
        for r in range(SIZE):
            for c in range(SIZE):
                x, y = c * CELL, r * CELL
                cv.create_rectangle(x, y, x + CELL, y + CELL,
                                    fill="#2b2d42", outline="#191927")
                v = self.board[r][c]
                if v is not None:
                    p = 7
                    cv.create_oval(x + p, y + p, x + CELL - p, y + CELL - p,
                                   fill=COLORS[v], outline="")
                    cv.create_text(x + CELL // 2, y + CELL // 2, text=SYMBOLS[v],
                                   font=("Arial", 18), fill="#000000")
                if self.sel == (r, c):
                    cv.create_rectangle(x + 2, y + 2, x + CELL - 2, y + CELL - 2,
                                        outline="#ffffff", width=3)
        if self.over:
            cv.create_rectangle(0, SIZE * CELL // 2 - 45, SIZE * CELL,
                                SIZE * CELL // 2 + 45, fill="#000000",
                                stipple="gray50", outline="")
            cv.create_text(SIZE * CELL // 2, SIZE * CELL // 2,
                           text=f"Game Over\nFinal score: {self.score}\nClick board for a new game",
                           fill="#ffffff", font=("Arial", 15, "bold"), justify="center")


def main():
    root = tk.Tk()
    Match3(root)
    root.mainloop()


if __name__ == "__main__":
    main()