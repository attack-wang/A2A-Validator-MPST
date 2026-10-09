import random

SIZE = 4


class Game2048:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.highest = 0
        self.over = False
        self.won = False
        self.spawn()
        self.spawn()
        self.highest = max(max(row) for row in self.board)

    def empty_cells(self):
        return [(r, c) for r in range(SIZE) for c in range(SIZE)
                if self.board[r][c] == 0]

    def spawn(self):
        cells = self.empty_cells()
        if not cells:
            return False
        r, c = random.choice(cells)
        self.board[r][c] = 2 if random.random() < 0.9 else 4
        return True

    @staticmethod
    def _slide(row):
        tiles = [v for v in row if v != 0]
        new = []
        gained = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged = tiles[i] * 2
                new.append(merged)
                gained += merged
                i += 2
            else:
                new.append(tiles[i])
                i += 1
        new += [0] * (SIZE - len(new))
        return new, gained, new != row

    def can_move(self):
        if any(v == 0 for row in self.board for v in row):
            return True
        for r in range(SIZE):
            for c in range(SIZE):
                v = self.board[r][c]
                if c + 1 < SIZE and self.board[r][c + 1] == v:
                    return True
                if r + 1 < SIZE and self.board[r + 1][c] == v:
                    return True
        return False

    def move(self, direction):
        if self.over:
            return False
        board = self.board
        if direction in ("up", "down"):
            board = [list(col) for col in zip(*board)]
        if direction in ("right", "down"):
            board = [row[::-1] for row in board]
        gained = 0
        moved = False
        rows = []
        for row in board:
            new_row, g, m = self._slide(row)
            rows.append(new_row)
            gained += g
            moved = moved or m
        if not moved:
            return False
        if direction in ("right", "down"):
            rows = [row[::-1] for row in rows]
        if direction in ("up", "down"):
            rows = [list(col) for col in zip(*rows)]
        self.board = rows
        self.score += gained
        self.spawn()
        self.highest = max(self.highest, max(max(row) for row in self.board))
        if self.highest >= 2048:
            self.won = True
        if not self.can_move():
            self.over = True
        return True