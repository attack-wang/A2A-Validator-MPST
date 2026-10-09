import tkinter as tk
import random

W, H, CELL = 10, 20, 28
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


def rotate(m):
    return [list(r) for r in zip(*m[::-1])]


class Tetris:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=W * CELL, height=H * CELL, bg='black')
        self.canvas.pack()
        self.info = tk.Label(root, text='')
        self.info.pack()
        root.bind('<Left>', lambda e: self.move(-1))
        root.bind('<Right>', lambda e: self.move(1))
        root.bind('<Down>', lambda e: self.step(True))
        root.bind('<Up>', lambda e: self.rotate_piece())
        root.bind('<space>', lambda e: self.hard_drop())
        root.bind('<p>', lambda e: self.toggle_pause())
        self.new_game()
        self.tick()

    def new_game(self):
        self.board = [[None] * W for _ in range(H)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.paused = False
        self.game_over = False
        self.spawn()
        self.draw()

    def spawn(self):
        self.name = random.choice(list(SHAPES))
        self.piece = [row[:] for row in SHAPES[self.name]]
        self.x = (W - len(self.piece[0])) // 2
        self.y = 0
        if self.collides(self.piece, self.x, self.y):
            self.game_over = True

    def collides(self, piece, px, py):
        for r, row in enumerate(piece):
            for c, v in enumerate(row):
                if v:
                    nx, ny = px + c, py + r
                    if nx < 0 or nx >= W or ny >= H:
                        return True
                    if ny >= 0 and self.board[ny][nx]:
                        return True
        return False

    def move(self, dx):
        if self.game_over or self.paused:
            return
        if not self.collides(self.piece, self.x + dx, self.y):
            self.x += dx
        self.draw()

    def rotate_piece(self):
        if self.game_over or self.paused:
            return
        rp = rotate(self.piece)
        for dx in (0, -1, 1, -2, 2):
            if not self.collides(rp, self.x + dx, self.y):
                self.piece, self.x = rp, self.x + dx
                break
        self.draw()

    def step(self, manual=False):
        if self.game_over or self.paused:
            return
        if not self.collides(self.piece, self.x, self.y + 1):
            self.y += 1
            if manual:
                self.score += 1
        else:
            self.lock()
        self.draw()

    def hard_drop(self):
        if self.game_over or self.paused:
            return
        while not self.collides(self.piece, self.x, self.y + 1):
            self.y += 1
            self.score += 2
        self.lock()
        self.draw()

    def lock(self):
        for r, row in enumerate(self.piece):
            for c, v in enumerate(row):
                if v and 0 <= self.y + r < H:
                    self.board[self.y + r][self.x + c] = self.name
        self.clear_lines()
        self.spawn()

    def clear_lines(self):
        full = [r for r in range(H) if all(self.board[r])]
        for r in full:
            del self.board[r]
            self.board.insert(0, [None] * W)
        if full:
            self.lines += len(full)
            self.score += [0, 100, 300, 500, 800][len(full)] * self.level
            self.level = 1 + self.lines // 10

    def speed(self):
        return max(120, 800 - (self.level - 1) * 70)

    def tick(self):
        self.step()
        self.root.after(self.speed(), self.tick)

    def toggle_pause(self):
        self.paused = not self.paused
        self.draw()

    def draw(self):
        self.canvas.delete('all')
        for r in range(H):
            for c in range(W):
                if self.board[r][c]:
                    self.cell(c, r, COLORS[self.board[r][c]])
        if not self.game_over:
            for r, row in enumerate(self.piece):
                for c, v in enumerate(row):
                    if v:
                        self.cell(self.x + c, self.y + r, COLORS[self.name])
        if self.game_over:
            self.canvas.create_text(W * CELL // 2, H * CELL // 2, text='GAME OVER',
                                    fill='white', font=('Arial', 24, 'bold'))
        elif self.paused:
            self.canvas.create_text(W * CELL // 2, H * CELL // 2, text='PAUSED',
                                    fill='white', font=('Arial', 24, 'bold'))
        self.info.config(text='Score: %d  Lines: %d  Level: %d' %
                                (self.score, self.lines, self.level))

    def cell(self, c, r, color):
        x1, y1 = c * CELL, r * CELL
        self.canvas.create_rectangle(x1, y1, x1 + CELL, y1 + CELL,
                                     fill=color, outline='gray')


def main():
    root = tk.Tk()
    root.title('Tetris')
    Tetris(root)
    root.mainloop()


if __name__ == '__main__':
    main()