import tkinter as tk
import random

CELL, COLS, ROWS = 30, 10, 20
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[1, 1, 1], [0, 1, 0]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
}
COLORS = {'I': '#00c8c8', 'O': '#c8c800', 'T': '#a000c8', 'S': '#00c800',
          'Z': '#c80000', 'J': '#0000c8', 'L': '#c87800'}


class Tetris:
    def __init__(self, root):
        self.root = root
        root.title('Tetris')
        self.cv = tk.Canvas(root, width=COLS * CELL + 170, height=ROWS * CELL,
                            bg='#141420', highlightthickness=0)
        self.cv.pack()
        root.bind('<Key>', self.on_key)
        self.reset()
        self.render()
        self.tick()
        root.mainloop()

    def reset(self):
        self.board = [[None] * COLS for _ in range(ROWS)]
        self.bag = []
        self.score = self.lines = self.level = 0
        self.over = False
        self.next_kind = self.draw_kind()
        self.spawn()

    def draw_kind(self):
        if not self.bag:
            self.bag = random.sample(list(SHAPES), 7)
        return self.bag.pop()

    def spawn(self):
        kind = self.next_kind
        self.next_kind = self.draw_kind()
        m = [r[:] for r in SHAPES[kind]]
        self.piece = [kind, m, (COLS - len(m[0])) // 2, 0]
        if not self.valid(m, self.piece[2], 0):
            self.over = True

    def valid(self, m, x, y):
        for r, row in enumerate(m):
            for c, v in enumerate(row):
                if v:
                    nx, ny = x + c, y + r
                    if nx < 0 or nx >= COLS or ny >= ROWS or (ny >= 0 and self.board[ny][nx]):
                        return False
        return True

    def on_key(self, e):
        if self.over:
            if e.keysym == 'r':
                self.reset()
                self.render()
            return
        kind, m, x, y = self.piece
        if e.keysym == 'Left' and self.valid(m, x - 1, y):
            self.piece[2] -= 1
        elif e.keysym == 'Right' and self.valid(m, x + 1, y):
            self.piece[2] += 1
        elif e.keysym == 'Down' and self.valid(m, x, y + 1):
            self.piece[3] += 1
        elif e.keysym == 'Up':
            r = [list(row) for row in zip(*m[::-1])]
            if self.valid(r, x, y):
                self.piece[1] = r
        elif e.keysym == 'space':
            while self.valid(m, x, y + 1):
                y += 1
            self.piece[3] = y
            self.lock()
        self.render()

    def lock(self):
        kind, m, x, y = self.piece
        for r, row in enumerate(m):
            for c, v in enumerate(row):
                if v:
                    self.board[y + r][x + c] = kind
        kept = [row for row in self.board if any(cell is None for cell in row)]
        cleared = ROWS - len(kept)
        self.board = [[None] * COLS for _ in range(cleared)] + kept
        self.score += [0, 100, 300, 500, 800][cleared] * (self.level + 1)
        self.lines += cleared
        self.level = self.lines // 10
        self.spawn()

    def tick(self):
        if not self.over:
            kind, m, x, y = self.piece
            if self.valid(m, x, y + 1):
                self.piece[3] += 1
            else:
                self.lock()
        self.render()
        self.root.after(max(100, 800 - self.level * 70), self.tick)

    def cell(self, x, y, color):
        self.cv.create_rectangle(x * CELL + 1, y * CELL + 1, (x + 1) * CELL - 1,
                                 (y + 1) * CELL - 1, fill=color, outline='')

    def render(self):
        cv = self.cv
        cv.delete('all')
        cv.create_rectangle(0, 0, COLS * CELL, ROWS * CELL, outline='#464650')
        for y in range(ROWS):
            for x in range(COLS):
                if self.board[y][x]:
                    self.cell(x, y, COLORS[self.board[y][x]])
        if not self.over:
            kind, m, x, y = self.piece
            for r, row in enumerate(m):
                for c, v in enumerate(row):
                    if v:
                        self.cell(x + c, y + r, COLORS[kind])
        px = COLS * CELL + 15
        cv.create_text(px, 30, text='Next:', fill='white', anchor='w')
        for r, row in enumerate(SHAPES[self.next_kind]):
            for c, v in enumerate(row):
                if v:
                    cv.create_rectangle(px + c * 22, 50 + r * 22, px + c * 22 + 20,
                                        50 + r * 22 + 20, fill=COLORS[self.next_kind],
                                        outline='')
        for i, t in enumerate(['Score: %d' % self.score, 'Lines: %d' % self.lines,
                               'Level: %d' % (self.level + 1)]):
            cv.create_text(px, 170 + i * 30, text=t, fill='white', anchor='w')
        for i, t in enumerate(['Arrows: move/rotate', 'Down: soft drop',
                               'Space: hard drop', 'R: restart']):
            cv.create_text(px, 290 + i * 25, text=t, fill='#969696', anchor='w')
        if self.over:
            cx, cy = COLS * CELL // 2, ROWS * CELL // 2
            cv.create_text(cx, cy - 20, text='GAME OVER', fill='#ff5050',
                           font=('Arial', 20, 'bold'))
            cv.create_text(cx, cy + 15, text='Press R to restart', fill='#ffc850')


def main():
    root = tk.Tk()
    Tetris(root)


if __name__ == '__main__':
    main()