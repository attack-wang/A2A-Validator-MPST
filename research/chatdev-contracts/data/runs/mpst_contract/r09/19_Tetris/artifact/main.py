import tkinter as tk
import random

W, H, CELL = 10, 20, 30
SHAPES = {
    'I': [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
    'J': [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
    'L': [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
    'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
    'T': [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
    'Z': [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
}
COLORS = {'I': '#00f0f0', 'J': '#0000f0', 'L': '#f0a000', 'O': '#f0f000',
          'S': '#00f000', 'T': '#a000f0', 'Z': '#f00000'}
LINE_SCORES = [0, 100, 300, 500, 800]


def rot(m):
    return [list(r) for r in zip(*m)][::-1]


class Tetris:
    def __init__(self, root):
        self.root = root
        root.title('Tetris')
        self.cv = tk.Canvas(root, width=W * CELL, height=H * CELL, bg='#111111', highlightthickness=0)
        self.cv.pack()
        self.info = tk.Label(root, font=('Arial', 12), fg='white', bg='#111111')
        self.info.pack(fill='x')
        root.bind('<Left>', lambda e: self.move(-1))
        root.bind('<Right>', lambda e: self.move(1))
        root.bind('<Down>', lambda e: self.soft_drop())
        root.bind('<Up>', lambda e: self.rotate())
        root.bind('<space>', lambda e: self.hard_drop())
        for k in ('p', 'P'):
            root.bind(k, lambda e: self.toggle_pause())
        for k in ('r', 'R'):
            root.bind(k, lambda e: self.reset())
        self.reset()
        self.tick()

    def reset(self):
        self.board = [[None] * W for _ in range(H)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.over = False
        self.paused = False
        self.next = self.new_piece()
        self.spawn()
        self.draw()

    def new_piece(self):
        k = random.choice(list(SHAPES))
        return [k, SHAPES[k]]

    def collides(self, m, x, y):
        for r, row in enumerate(m):
            for c, v in enumerate(row):
                if v:
                    nx, ny = x + c, y + r
                    if nx < 0 or nx >= W or ny >= H or (ny >= 0 and self.board[ny][nx]):
                        return True
        return False

    def spawn(self):
        self.kind, self.m = self.next
        self.next = self.new_piece()
        self.x = (W - len(self.m[0])) // 2
        self.y = 0
        if self.collides(self.m, self.x, self.y):
            self.over = True

    def move(self, dx):
        if self.over or self.paused:
            return
        if not self.collides(self.m, self.x + dx, self.y):
            self.x += dx
        self.draw()

    def rotate(self):
        if self.over or self.paused:
            return
        rm = rot(self.m)
        for k in (0, -1, 1, -2, 2):
            if not self.collides(rm, self.x + k, self.y):
                self.m, self.x = rm, self.x + k
                break
        self.draw()

    def soft_drop(self):
        if self.over or self.paused:
            return
        if not self.collides(self.m, self.x, self.y + 1):
            self.y += 1
            self.score += 1
        else:
            self.lock()
        self.draw()

    def hard_drop(self):
        if self.over or self.paused:
            return
        while not self.collides(self.m, self.x, self.y + 1):
            self.y += 1
            self.score += 2
        self.lock()
        self.draw()

    def lock(self):
        for r, row in enumerate(self.m):
            for c, v in enumerate(row):
                if v:
                    self.board[self.y + r][self.x + c] = self.kind
        full = [r for r in range(H) if all(self.board[r])]
        for r in full:
            del self.board[r]
            self.board.insert(0, [None] * W)
        if full:
            self.lines += len(full)
            self.score += LINE_SCORES[len(full)] * self.level
            self.level = self.lines // 10 + 1
        self.spawn()

    def tick(self):
        if not self.over and not self.paused:
            if not self.collides(self.m, self.x, self.y + 1):
                self.y += 1
            else:
                self.lock()
            self.draw()
        delay = max(100, 800 - (self.level - 1) * 70)
        self.root.after(delay, self.tick)

    def toggle_pause(self):
        self.paused = not self.paused
        self.draw()

    def draw(self):
        self.cv.delete('all')
        for r in range(H):
            for c in range(W):
                k = self.board[r][c]
                if k:
                    self.cell(c, r, COLORS[k])
        if not self.over:
            for r, row in enumerate(self.m):
                for c, v in enumerate(row):
                    if v:
                        self.cell(self.x + c, self.y + r, COLORS[self.kind])
        status = 'GAME OVER - press R' if self.over else ('PAUSED - press P' if self.paused else '')
        self.info.config(text='Score: %d   Lines: %d   Level: %d   %s' %
                             (self.score, self.lines, self.level, status))

    def cell(self, c, r, color):
        self.cv.create_rectangle(c * CELL + 1, r * CELL + 1,
                                 (c + 1) * CELL - 1, (r + 1) * CELL - 1,
                                 fill=color, outline='')


if __name__ == '__main__':
    root = tk.Tk()
    Tetris(root)
    root.mainloop()