import random

COLS, ROWS = 10, 20

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[1, 1, 1], [0, 1, 0]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
}

COLORS = {
    'I': (0, 190, 200), 'O': (220, 190, 0), 'T': (160, 60, 220),
    'S': (0, 190, 60), 'Z': (220, 60, 60), 'J': (60, 90, 220),
    'L': (230, 140, 20),
}

LINE_SCORES = (0, 100, 300, 500, 800)


def rotate(m):
    return [list(r) for r in zip(*m[::-1])]


class Piece:
    def __init__(self, kind=None):
        self.kind = kind or random.choice(list(SHAPES))
        self.shape = [row[:] for row in SHAPES[self.kind]]
        self.x = (COLS - len(self.shape[0])) // 2
        self.y = 0

    def cells(self):
        return [(self.x + cx, self.y + cy)
                for cy, row in enumerate(self.shape)
                for cx, v in enumerate(row) if v]


class Tetris:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[None] * COLS for _ in range(ROWS)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.paused = False
        self.game_over = False
        self.next_piece = Piece()
        self.spawn()

    def spawn(self):
        self.piece = self.next_piece
        self.next_piece = Piece()
        if self.collides(self.piece, 0, 0):
            self.game_over = True

    def collides(self, piece, dx, dy, shape=None):
        shape = piece.shape if shape is None else shape
        for cy, row in enumerate(shape):
            for cx, v in enumerate(row):
                if v:
                    x, y = piece.x + cx + dx, piece.y + cy + dy
                    if x < 0 or x >= COLS or y >= ROWS:
                        return True
                    if y >= 0 and self.board[y][x]:
                        return True
        return False

    def move(self, dx, dy=0):
        if not self.game_over and not self.collides(self.piece, dx, dy):
            self.piece.x += dx
            self.piece.y += dy
            return True
        return False

    def rotate_piece(self):
        r = rotate(self.piece.shape)
        for kick in (0, -1, 1, -2, 2):
            if not self.collides(self.piece, kick, 0, r):
                self.piece.x += kick
                self.piece.shape = r
                return True
        return False

    def hard_drop(self):
        d = 0
        while self.move(0, 1):
            d += 1
        self.score += 2 * d
        self.lock()

    def step(self):
        if not self.move(0, 1):
            self.lock()

    def lock(self):
        for x, y in self.piece.cells():
            self.board[y][x] = self.piece.kind
        remaining = [row for row in self.board if not all(row)]
        cleared = ROWS - len(remaining)
        self.board = [[None] * COLS for _ in range(cleared)] + remaining
        self.lines += cleared
        self.score += LINE_SCORES[cleared] * self.level
        self.level = self.lines // 10 + 1
        self.spawn()

    def drop_interval(self):
        return max(0.08, 0.6 - 0.05 * (self.level - 1))