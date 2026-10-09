import tkinter as tk
import random

CELL = 26
COLS, ROWS = 10, 20
PANEL = 150

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
}
COLORS = {'I': '#00e5ff', 'O': '#ffd500', 'T': '#a64dff', 'S': '#3ddc55',
          'Z': '#ff3b3b', 'J': '#3b6bff', 'L': '#ff9a3b'}


class Tetris:
    def __init__(self, root):
        self.root = root
        self.job = None
        root.title('Tetris')
        self.canvas = tk.Canvas(root, width=COLS * CELL + PANEL, height=ROWS * CELL,
                                bg='#101018', highlightthickness=0)
        self.canvas.pack()
        root.bind('<Left>', lambda e: self.move(-1))
        root.bind('<Right>', lambda e: self.move(1))
        root.bind('<Down>', lambda e: self.soft_drop())
        root.bind('<Up>', lambda e: self.rotate())
        root.bind('<space>', lambda e: self.hard_drop())
        for k in ('p', 'P'):
            root.bind('<%s>' % k, lambda e: self.toggle_pause())
        for k in ('r', 'R'):
            root.bind('<%s>' % k, lambda e: self.reset())
        self.reset()

    def cancel_job(self):
        if self.job is not None:
            try:
                self.root.after_cancel(self.job)
            except Exception:
                pass
            self.job = None

    def schedule(self):
        self.cancel_job()
        self.job = self.root.after(self.delay, self.loop)

    def reset(self):
        self.cancel_job()
        self.grid = [[None] * COLS for _ in range(ROWS)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.over = False
        self.paused = False
        self.next_key = random.choice(list(SHAPES))
        self.spawn()
        self.delay = self.speed()
        self.draw()
        if not self.over:
            self.schedule()

    def speed(self):
        return max(90, 600 - (self.level - 1) * 55)

    def spawn(self):
        self.key = self.next_key
        self.next_key = random.choice(list(SHAPES))
        self.piece = [row[:] for row in SHAPES[self.key]]
        self.px = (COLS - len(self.piece[0])) // 2
        self.py = 0
        if self.collide(self.piece, self.px, self.py):
            self.over = True
            self.draw()

    def collide(self, m, x, y):
        for cy, row in enumerate(m):
            for cx, v in enumerate(row):
                if v:
                    bx, by = x + cx, y + cy
                    if bx < 0 or bx >= COLS or by >= ROWS:
                        return True
                    if by >= 0 and self.grid[by][bx]:
                        return True
        return False

    def loop(self):
        self.job = None
        if self.over or self.paused:
            return
        self.tick()
        if not self.over and not self.paused:
            self.schedule()

    def tick(self):
        if self.collide(self.piece, self.px, self.py + 1):
            self.lock()
        else:
            self.py += 1
        self.draw()

    def lock(self):
        for cy, row in enumerate(self.piece):
            for cx, v in enumerate(row):
                if v and self.py + cy >= 0:
                    self.grid[self.py + cy][self.px + cx] = self.key
        self.clear_lines()
        self.spawn()

    def clear_lines(self):
        full = [r for r in self.grid if all(r)]
        if full:
            n = len(full)
            for r in full:
                self.grid.remove(r)
            for _ in range(n):
                self.grid.insert(0, [None] * COLS)
            self.lines += n
            self.score += [0, 100, 300, 500, 800][n] * self.level
            new_level = self.lines // 10 + 1
            if new_level > self.level:
                self.level = new_level
                self.delay = self.speed()

    def move(self, dx):
        if self.over or self.paused:
            return
        if not self.collide(self.piece, self.px + dx, self.py):
            self.px += dx
        self.draw()

    def rotate(self):
        if self.over or self.paused:
            return
        r = [list(row) for row in zip(*self.piece[::-1])]
        for off in (0, -1, 1, -2, 2):
            if not self.collide(r, self.px + off, self.py):
                self.piece, self.px = r, self.px + off
                break
        self.draw()

    def soft_drop(self):
        if self.over or self.paused:
            return
        if not self.collide(self.piece, self.px, self.py + 1):
            self.py += 1
            self.score += 1
        else:
            self.lock()
        self.draw()

    def hard_drop(self):
        if self.over or self.paused:
            return
        d = 0
        while not self.collide(self.piece, self.px, self.py + 1):
            self.py += 1
            d += 1
        self.score += d * 2
        self.lock()
        self.draw()

    def toggle_pause(self):
        if self.over:
            return
        if self.paused:
            self.paused = False
            self.schedule()
        else:
            self.paused = True
            self.cancel_job()
        self.draw()

    def cell(self, x, y, color):
        self.canvas.create_rectangle(x * CELL + 1, y * CELL + 1,
                                     (x + 1) * CELL - 1, (y + 1) * CELL - 1,
                                     fill=color, outline='#0a0a12')

    def draw(self):
        c = self.canvas
        c.delete('all')
        for y in range(ROWS):
            for x in range(COLS):
                k = self.grid[y][x]
                self.cell(x, y, COLORS[k] if k else '#1c1c28')
        for cy, row in enumerate(self.piece):
            for cx, v in enumerate(row):
                if v and self.py + cy >= 0:
                    self.cell(self.px + cx, self.py + cy, COLORS[self.key])
        cx0 = COLS * CELL + PANEL // 2
        c.create_text(cx0, 24, text='TETRIS', fill='white', font=('Arial', 14, 'bold'))
        c.create_text(cx0, 58, text='Score: %d' % self.score, fill='white', font=('Arial', 12))
        c.create_text(cx0, 82, text='Lines: %d' % self.lines, fill='white', font=('Arial', 12))
        c.create_text(cx0, 106, text='Level: %d' % self.level, fill='white', font=('Arial', 12))
        c.create_text(cx0, 138, text='Next:', fill='white', font=('Arial', 11))
        nm = SHAPES[self.next_key]
        ox = COLS * CELL + (PANEL - len(nm[0]) * 16) // 2
        oy = 156
        for cy, row in enumerate(nm):
            for cx, v in enumerate(row):
                if v:
                    c.create_rectangle(ox + cx * 16, oy + cy * 16,
                                       ox + cx * 16 + 15, oy + cy * 16 + 15,
                                       fill=COLORS[self.next_key], outline='')
        c.create_text(cx0, ROWS * CELL - 56,
                      text='<- -> move | ^ rotate\nv soft | Space hard\nP pause | R restart',
                      fill='#9a9ab0', font=('Arial', 9), justify='center')
        if self.paused:
            c.create_text(COLS * CELL // 2, ROWS * CELL // 2, text='PAUSED',
                          fill='yellow', font=('Arial', 22, 'bold'))
        if self.over:
            c.create_rectangle(0, ROWS * CELL // 2 - 40, COLS * CELL, ROWS * CELL // 2 + 40,
                               fill='black', stipple='gray50')
            c.create_text(COLS * CELL // 2, ROWS * CELL // 2 - 12, text='GAME OVER',
                          fill='red', font=('Arial', 20, 'bold'))
            c.create_text(COLS * CELL // 2, ROWS * CELL // 2 + 18, text='Press R to restart',
                          fill='white', font=('Arial', 11))


if __name__ == '__main__':
    root = tk.Tk()
    Tetris(root)
    root.mainloop()