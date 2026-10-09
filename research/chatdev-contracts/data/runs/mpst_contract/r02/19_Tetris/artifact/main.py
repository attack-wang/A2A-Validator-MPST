import tkinter as tk
import random

W, H, S = 10, 20, 26
SHAPES = {
    'I': [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
    'S': [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
    'Z': [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
    'J': [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
    'L': [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
}
COLORS = {'I': 'cyan', 'O': 'yellow', 'T': 'purple', 'S': 'green',
          'Z': 'red', 'J': 'blue', 'L': 'orange'}


def rot(m):
    n = len(m)
    return [[m[n - 1 - j][i] for j in range(n)] for i in range(n)]


class Tetris:
    def __init__(self, root):
        self.root = root
        self.cv = tk.Canvas(root, width=W * S, height=H * S, bg='black')
        self.cv.pack()
        self.info = tk.Label(root, text='')
        self.info.pack()
        root.bind('<Left>', lambda e: self.move(-1))
        root.bind('<Right>', lambda e: self.move(1))
        root.bind('<Down>', lambda e: self.drop())
        root.bind('<Up>', lambda e: self.rotate())
        root.bind('<space>', lambda e: self.hard_drop())
        self.reset()
        self.tick()

    def reset(self):
        self.board = [[(0, '') for _ in range(W)] for _ in range(H)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.over = False
        self.new_piece()
        self.draw()

    def new_piece(self):
        self.shape = random.choice(list(SHAPES))
        self.m = [r[:] for r in SHAPES[self.shape]]
        self.x = (W - len(self.m[0])) // 2
        self.y = 0
        if self.hit(self.x, self.y, self.m):
            self.over = True

    def cells(self, m):
        return [(x, y) for y, row in enumerate(m) for x, v in enumerate(row) if v]

    def hit(self, x, y, m):
        for cx, cy in self.cells(m):
            bx, by = x + cx, y + cy
            if bx < 0 or bx >= W or by >= H or (by >= 0 and self.board[by][bx][0]):
                return True
        return False

    def move(self, dx):
        if not self.over and not self.hit(self.x + dx, self.y, self.m):
            self.x += dx
        self.draw()

    def rotate(self):
        if self.over:
            return
        r = rot(self.m)
        for k in (0, -1, 1, -2, 2):
            if not self.hit(self.x + k, self.y, r):
                self.m = r
                self.x += k
                break
        self.draw()

    def drop(self):
        if self.over:
            return
        if not self.hit(self.x, self.y + 1, self.m):
            self.y += 1
        else:
            self.lock()
        self.draw()

    def hard_drop(self):
        if self.over:
            return
        dist = 0
        while not self.hit(self.x, self.y + 1, self.m):
            self.y += 1
            dist += 1
        self.score += 2 * dist
        self.lock()
        self.draw()

    def lock(self):
        for cx, cy in self.cells(self.m):
            self.board[self.y + cy][self.x + cx] = (1, COLORS[self.shape])
        cleared = 0
        nb = []
        for row in self.board:
            if all(c[0] for c in row):
                cleared += 1
            else:
                nb.append(row)
        for _ in range(cleared):
            nb.insert(0, [(0, '') for _ in range(W)])
        self.board = nb
        self.lines += cleared
        self.score += [0, 100, 300, 500, 800][cleared] * self.level
        self.level = 1 + self.lines // 10
        self.new_piece()

    def tick(self):
        if not self.over:
            self.drop()
        speed = max(100, 1000 - 100 * (self.level - 1))
        self.root.after(speed, self.tick)

    def draw(self):
        self.cv.delete('all')
        for y in range(H):
            for x in range(W):
                c = self.board[y][x]
                if c[0]:
                    self.cv.create_rectangle(x * S, y * S, (x + 1) * S, (y + 1) * S,
                                             fill=c[1], outline='gray')
        if not self.over:
            for cx, cy in self.cells(self.m):
                self.cv.create_rectangle((self.x + cx) * S, (self.y + cy) * S,
                                         (self.x + cx + 1) * S, (self.y + cy + 1) * S,
                                         fill=COLORS[self.shape], outline='white')
        else:
            self.cv.create_text(W * S // 2, H * S // 2, text='GAME OVER',
                                fill='white', font=('Arial', 24, 'bold'))
        self.info.config(text='Score: %d   Lines: %d   Level: %d' %
                         (self.score, self.lines, self.level))


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Tetris')
    root.resizable(False, False)
    Tetris(root)
    root.mainloop()