import tkinter as tk
import random

COLS, ROWS, CELL = 10, 20, 30

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[1, 1, 1], [0, 1, 0]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
}
COLORS = {'I': 'cyan', 'O': 'yellow', 'T': 'purple', 'S': 'green',
          'Z': 'red', 'J': 'blue', 'L': 'orange'}


def rotate(shape):
    return [list(r) for r in zip(*shape[::-1])]


class Tetris:
    def __init__(self, root):
        self.root = root
        root.title('Tetris')
        self.canvas = tk.Canvas(root, width=COLS * CELL, height=ROWS * CELL,
                                bg='black', highlightthickness=0)
        self.canvas.pack(side=tk.LEFT)
        side = tk.Frame(root)
        side.pack(side=tk.RIGHT, fill=tk.Y, padx=8, pady=8)
        self.score_v = tk.StringVar(value='Score: 0')
        self.level_v = tk.StringVar(value='Level: 1')
        self.lines_v = tk.StringVar(value='Lines: 0')
        for v in (self.score_v, self.level_v, self.lines_v):
            tk.Label(side, textvariable=v, font=('Arial', 13)).pack(anchor='w', pady=3)
        tk.Label(side, text='Left/Right: move\nUp: rotate\nDown: soft drop\n'
                            'Space: hard drop\nP: pause\nN: new game',
                 justify=tk.LEFT).pack(pady=10)
        for key, fn in (('<Left>', lambda e: self.move(-1, 0)),
                        ('<Right>', lambda e: self.move(1, 0)),
                        ('<Down>', lambda e: self.move(0, 1)),
                        ('<Up>', lambda e: self.rotate_piece()),
                        ('<space>', lambda e: self.hard_drop()),
                        ('<p>', lambda e: self.toggle_pause()),
                        ('<n>', lambda e: self.new_game())):
            root.bind(key, fn)
        self.new_game()
        self.tick()

    def new_game(self):
        self.board = [[None] * COLS for _ in range(ROWS)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.paused = False
        self.over = False
        self.spawn()
        self.update_stats()
        self.draw()

    def spawn(self):
        kind = random.choice(list(SHAPES))
        shape = [row[:] for row in SHAPES[kind]]
        self.piece = {'kind': kind, 'shape': shape,
                      'x': (COLS - len(shape[0])) // 2, 'y': 0}
        if not self.valid(shape, self.piece['x'], self.piece['y']):
            self.over = True

    def valid(self, shape, px, py):
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    x, y = px + c, py + r
                    if x < 0 or x >= COLS or y >= ROWS:
                        return False
                    if y >= 0 and self.board[y][x]:
                        return False
        return True

    def move(self, dx, dy):
        if self.over or self.paused:
            return
        p = self.piece
        if self.valid(p['shape'], p['x'] + dx, p['y'] + dy):
            p['x'] += dx
            p['y'] += dy
        elif dy:
            self.lock()
        self.draw()

    def rotate_piece(self):
        if self.over or self.paused:
            return
        p = self.piece
        rot = rotate(p['shape'])
        for dx, dy in ((0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0), (0, -1)):
            if self.valid(rot, p['x'] + dx, p['y'] + dy):
                p['shape'], p['x'], p['y'] = rot, p['x'] + dx, p['y'] + dy
                break
        self.draw()

    def hard_drop(self):
        if self.over or self.paused:
            return
        p = self.piece
        while self.valid(p['shape'], p['x'], p['y'] + 1):
            p['y'] += 1
        self.lock()
        self.draw()

    def lock(self):
        p = self.piece
        for r, row in enumerate(p['shape']):
            for c, cell in enumerate(row):
                if cell and p['y'] + r >= 0:
                    self.board[p['y'] + r][p['x'] + c] = COLORS[p['kind']]
        full = [i for i, row in enumerate(self.board) if all(row)]
        for i in full:
            del self.board[i]
            self.board.insert(0, [None] * COLS)
        if full:
            self.lines += len(full)
            self.score += (100, 300, 500, 800)[len(full) - 1] * self.level
            self.level = self.lines // 10 + 1
            self.update_stats()
        self.spawn()

    def update_stats(self):
        self.score_v.set('Score: %d' % self.score)
        self.level_v.set('Level: %d' % self.level)
        self.lines_v.set('Lines: %d' % self.lines)

    def delay(self):
        return max(100, 800 - (self.level - 1) * 60)

    def tick(self):
        if not self.paused and not self.over:
            self.move(0, 1)
        self.root.after(self.delay(), self.tick)

    def toggle_pause(self):
        if not self.over:
            self.paused = not self.paused
            self.draw()

    def draw(self):
        self.canvas.delete('all')
        for y in range(ROWS):
            for x in range(COLS):
                color = self.board[y][x]
                if color:
                    self.cell(x, y, color)
                else:
                    self.canvas.create_rectangle(x * CELL, y * CELL,
                                                 (x + 1) * CELL, (y + 1) * CELL,
                                                 outline='#222')
        if not self.over:
            p = self.piece
            for r, row in enumerate(p['shape']):
                for c, cell in enumerate(row):
                    if cell and p['y'] + r >= 0:
                        self.cell(p['x'] + c, p['y'] + r, COLORS[p['kind']])
        if self.over:
            self.canvas.create_rectangle(0, ROWS * CELL // 2 - 40, COLS * CELL,
                                         ROWS * CELL // 2 + 40, fill='black',
                                         stipple='gray50')
            self.canvas.create_text(COLS * CELL // 2, ROWS * CELL // 2,
                                    text='GAME OVER\nPress N', fill='white',
                                    font=('Arial', 18), justify=tk.CENTER)
        elif self.paused:
            self.canvas.create_text(COLS * CELL // 2, ROWS * CELL // 2,
                                    text='PAUSED', fill='white', font=('Arial', 20))

    def cell(self, x, y, color):
        self.canvas.create_rectangle(x * CELL + 1, y * CELL + 1,
                                     (x + 1) * CELL - 1, (y + 1) * CELL - 1,
                                     fill=color, outline='')


def main():
    root = tk.Tk()
    Tetris(root)
    root.mainloop()


if __name__ == '__main__':
    main()