import random

SIZE = 4


class Game2048:
    def __init__(self):
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.highest = 0
        self.spawn()
        self.spawn()

    def empty_cells(self):
        return [(r, c) for r in range(SIZE) for c in range(SIZE) if self.board[r][c] == 0]

    def spawn(self):
        cells = self.empty_cells()
        if not cells:
            return False
        r, c = random.choice(cells)
        self.board[r][c] = 4 if random.random() < 0.1 else 2
        self.highest = max(self.highest, self.board[r][c])
        return True

    @staticmethod
    def _slide_left(row):
        tiles = [v for v in row if v]
        merged = []
        gained = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                value = tiles[i] * 2
                merged.append(value)
                gained += value
                i += 2
            else:
                merged.append(tiles[i])
                i += 1
        merged += [0] * (SIZE - len(merged))
        return merged, gained

    def _move(self, board, direction):
        # direction: 0=left, 1=up, 2=right, 3=down
        if direction in (1, 3):
            board = [list(col) for col in zip(*board)]
            if direction == 3:
                board = [row[::-1] for row in board]
        elif direction == 2:
            board = [row[::-1] for row in board]
        moved = False
        gained_total = 0
        new_board = []
        for row in board:
            merged, gained = self._slide_left(row)
            gained_total += gained
            if merged != row:
                moved = True
            new_board.append(merged)
        if direction == 2:
            new_board = [row[::-1] for row in new_board]
        if direction in (1, 3):
            if direction == 3:
                new_board = [row[::-1] for row in new_board]
            new_board = [list(col) for col in zip(*new_board)]
        return new_board, moved, gained_total

    def move(self, direction):
        new_board, moved, gained = self._move(self.board, direction)
        if moved:
            self.board = new_board
            self.score += gained
            self.highest = max(self.highest, max(v for row in self.board for v in row))
            self.spawn()
        return moved

    def can_move(self):
        for r in range(SIZE):
            for c in range(SIZE):
                v = self.board[r][c]
                if v == 0:
                    return True
                if c + 1 < SIZE and self.board[r][c + 1] == v:
                    return True
                if r + 1 < SIZE and self.board[r + 1][c] == v:
                    return True
        return False

    def game_over(self):
        return not self.can_move()