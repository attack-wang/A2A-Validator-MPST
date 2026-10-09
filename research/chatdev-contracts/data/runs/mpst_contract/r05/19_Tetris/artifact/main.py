import random
import tkinter as tk

CELL, COLS, ROWS = 30, 10, 20
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'Z': [[1, 1, 0], [0, 1, 1]],
}
COLORS = {'I': '#00e5ff', 'J': '#2962ff', 'L': '#ff9100', 'O': '#ffea00',
          'S': '#00e676', 'T': '#d500f9', 'Z': '#ff1744'}


def rot(m):
    return [list(r) for r in zip(*m[::-1])]


class Tetris:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=COLS * CELL, height=ROWS * CELL,
                                bg='#101018', highlightthickness=0)
        self.canvas.pack()
        self.info = tk.Label(root, font=('Consolas', 11), fg='white', bg='#101018')
        self.info.pack(fill='x')
        root.bind('<Key>', self.on_key)
        self.new_game()
        self.tick()

    def new_game(self):
        self.board = [[None] * COLS for _ in range(ROWS)]
        self.score = self.lines = 0
        self.level = 1
        self.over = self.paused = False
        self.bag = []
        self.spawn()
        self.draw()

    def spawn(self):
        if not self.bag:
            self.bag = random.sample(list(SHAPES), 7)
        name = self.bag.pop()
        m = SHAPES[name]
        self.piece = [name, m, (COLS - len(m[0])) // 2, 0]
        if self.hits(m, self.piece[2], 0):
            self.over = True

    def hits(self, m, px, py):
        for y, row in enumerate(m):
            for x, v in enumerate(row):
                if v:
                    bx, by = px + x, py + y
                    if bx < 0 or bx >= COLS or by >= ROWS or (by >= 0 and self.board[by][bx]):
                        return True
        return False

    def move(self, dx, dy):
        _, m, x, y = self.piece
        if self.hits(m, x + dx, y + dy):
            return False
        self.piece[2] += dx
        self.piece[3] += dy
        return True

    def rotate(self):
        _, m, x, y = self.piece
        r = rot(m)
        for dx in (0, -1, 1, -2, 2):
            if not self.hits(r, x + dx, y):
                self.piece[1], self.piece[2] = r, x + dx
                return

    def lock(self):
        name, m, x, y = self.piece
        for j, row in enumerate(m):
            for i, v in enumerate(row):
                if v and y + j >= 0:
                    self.board[y + j][x + i] = name
        kept = [r for r in self.board if any(c is None for c in r)]
        cleared = ROWS - len(kept)
        self.board = [[None] * COLS for _ in range(cleared)] + kept
        if cleared:
            self.lines += cleared
            self.score += (0, 100, 300, 500, 800)[cleared] * self.level
            self.level = self.lines // 10 + 1
        self.spawn()

    def hard_drop(self):
        n = 0
        while self.move(0, 1):
            n += 1
        self.score += 2 * n
        self.lock()

    def on_key(self, e):
        k = e.keysym.lower()
        if self.over:
            if k == 'r':
                self.new_game()
            return
        if k == 'p':
            self.paused = not self.paused
        elif not self.paused:
            if k == 'left':
                self.move(-1, 0)
            elif k == 'right':
                self.move(1, 0)
            elif k == 'down':
                if self.move(0, 1):
                    self.score += 1
            elif k == 'up':
                self.rotate()
            elif k == 'space':
                self.hard_drop()
        self.draw()

    def interval(self):
        return max(120, 800 - (self.level - 1) * 70)

    def tick(self):
        if not (self.paused or self.over):
            if not self.move(0, 1):
                self.lock()
            self.draw()
        self.root.after(self.interval(), self.tick)

    def draw(self):
        c = self.canvas
        c.delete('all')
        for y in range(ROWS):
            for x in range(COLS):
                n = self.board[y][x]
                if n:
                    self.cell(x, y, COLORS[n])
        if not self.over:
            _, m, x, y = self.piece
            for j, row in enumerate(m):
                for i, v in enumerate(row):
                    if v and y + j >= 0:
                        self.cell(x + i, y + j, COLORS[self.piece[0]])
        s = f'Score: {self.score}   Lines: {self.lines}   Level: {self.level}'
        if self.over:
            s += '   GAME OVER - R to restart'
        elif self.paused:
            s += '   PAUSED (P)'
        self.info.config(text=s)

    def cell(self, x, y, color):
        self.canvas.create_rectangle(x * CELL + 1, y * CELL + 1,
                                     (x + 1) * CELL - 1, (y + 1) * CELL - 1,
                                     fill=color, outline='')


def main():
    root = tk.Tk()
    root.title('Tetris')
    Tetris(root)
    root.mainloop()


if __name__ == '__main__':
    main()