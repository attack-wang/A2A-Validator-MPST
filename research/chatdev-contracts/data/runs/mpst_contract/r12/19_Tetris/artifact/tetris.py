import random
import tkinter as tk

WIDTH, HEIGHT, CELL = 10, 20, 28

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'Z': [[1, 1, 0], [0, 1, 1]],
}
COLORS = {'I': 'cyan', 'J': 'blue', 'L': 'orange',
          'O': 'yellow', 'S': 'green', 'T': 'purple', 'Z': 'red'}
LINE_SCORES = (0, 100, 300, 500, 800)


class Tetris:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH * CELL, height=HEIGHT * CELL,
                                bg='black', highlightthickness=0)
        self.canvas.pack()
        self.status = tk.StringVar()
        tk.Label(root, textvariable=self.status, font=('Arial', 12)).pack()
        tk.Label(root, text='Left/Right: move  Up: rotate  Down: soft drop\n'
                            'Space: hard drop  P: pause  R: restart',
                 font=('Arial', 10), fg='gray').pack()
        root.bind('<Left>', lambda e: self.move(-1))
        root.bind('<Right>', lambda e: self.move(1))
        root.bind('<Up>', lambda e: self.rotate())
        root.bind('<Down>', lambda e: self.soft_drop())
        root.bind('<space>', lambda e: self.hard_drop())
        root.bind('<p>', lambda e: self.toggle_pause())
        root.bind('<r>', lambda e: self.restart())
        self.restart()
        self.root.after(self.speed(), self.tick)

    def restart(self):
        self.board = [[None] * WIDTH for _ in range(HEIGHT)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.spawn()
        self.draw()

    def spawn(self):
        self.name = random.choice(list(SHAPES))
        self.matrix = [row[:] for row in SHAPES[self.name]]
        self.row = 0
        self.col = (WIDTH - len(self.matrix[0])) // 2
        if self.collides(self.row, self.col, self.matrix):
            self.game_over = True

    def collides(self, r, c, m):
        for i, row in enumerate(m):
            for j, v in enumerate(row):
                if v:
                    rr, cc = r + i, c + j
                    if cc < 0 or cc >= WIDTH or rr >= HEIGHT:
                        return True
                    if rr >= 0 and self.board[rr][cc]:
                        return True
        return False

    def move(self, dc):
        if not self.game_over and not self.paused and \
                not self.collides(self.row, self.col + dc, self.matrix):
            self.col += dc
            self.draw()

    def rotate(self):
        if self.game_over or self.paused:
            return
        m = [list(r) for r in zip(*self.matrix[::-1])]
        for off in (0, -1, 1, -2, 2):
            if not self.collides(self.row, self.col + off, m):
                self.matrix, self.col = m, self.col + off
                self.draw()
                return

    def soft_drop(self):
        if self.game_over or self.paused:
            return
        if not self.collides(self.row + 1, self.col, self.matrix):
            self.row += 1
        else:
            self.lock()
        self.draw()

    def hard_drop(self):
        if self.game_over or self.paused:
            return
        while not self.collides(self.row + 1, self.col, self.matrix):
            self.row += 1
        self.lock()
        self.draw()

    def lock(self):
        for i, row in enumerate(self.matrix):
            for j, v in enumerate(row):
                if v and self.row + i >= 0:
                    self.board[self.row + i][self.col + j] = self.name
        full = [r for r in range(HEIGHT) if all(self.board[r])]
        for r in full:
            del self.board[r]
            self.board.insert(0, [None] * WIDTH)
        if full:
            self.lines += len(full)
            self.score += LINE_SCORES[len(full)] * self.level
            self.level = self.lines // 10 + 1
        self.spawn()

    def speed(self):
        return max(100, 800 - (self.level - 1) * 70)

    def tick(self):
        if not self.game_over and not self.paused:
            self.soft_drop()
        self.root.after(self.speed(), self.tick)

    def toggle_pause(self):
        self.paused = not self.paused
        self.draw()

    def draw(self):
        self.canvas.delete('all')
        for r in range(HEIGHT):
            for c in range(WIDTH):
                if self.board[r][c]:
                    self.cell(r, c, COLORS[self.board[r][c]])
        if not self.game_over:
            for i, row in enumerate(self.matrix):
                for j, v in enumerate(row):
                    if v and self.row + i >= 0:
                        self.cell(self.row + i, self.col + j, COLORS[self.name])
        self.status.set('Score: %d   Lines: %d   Level: %d' %
                        (self.score, self.lines, self.level))
        if self.game_over:
            self.canvas.create_text(WIDTH * CELL // 2, HEIGHT * CELL // 2,
                                    text='GAME OVER', fill='white',
                                    font=('Arial', 24, 'bold'))
        elif self.paused:
            self.canvas.create_text(WIDTH * CELL // 2, HEIGHT * CELL // 2,
                                    text='PAUSED', fill='white',
                                    font=('Arial', 24, 'bold'))

    def cell(self, r, c, color):
        x, y = c * CELL, r * CELL
        self.canvas.create_rectangle(x + 1, y + 1, x + CELL - 1, y + CELL - 1,
                                     fill=color, outline='')