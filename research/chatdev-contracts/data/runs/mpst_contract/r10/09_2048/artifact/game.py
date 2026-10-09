"""Core 2048 game logic: 4x4 grid, sliding, merging, scoring, game-over detection."""
import random


class Game2048:
    SIZE = 4

    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = [[0] * self.SIZE for _ in range(self.SIZE)]
        self.score = 0
        self.highest = 0
        self.over = False
        self.add_random_tile()
        self.add_random_tile()
        self.highest = max(max(row) for row in self.grid)

    def empty_cells(self):
        return [(r, c) for r in range(self.SIZE) for c in range(self.SIZE)
                if self.grid[r][c] == 0]

    def add_random_tile(self):
        cells = self.empty_cells()
        if not cells:
            return False
        r, c = random.choice(cells)
        self.grid[r][c] = 2 if random.random() < 0.9 else 4
        return True

    @staticmethod
    def _slide_row(row):
        """Slide and merge one row toward index 0. Returns (new_row, gained)."""
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
        merged += [0] * (len(row) - len(merged))
        return merged, gained

    def _move(self, direction):
        """Apply one slide in 'left'/'right'/'up'/'down'. Returns True if changed."""
        moved = False
        gained_total = 0
        for i in range(self.SIZE):
            if direction in ("left", "right"):
                original = self.grid[i][:]
            else:
                original = [self.grid[r][i] for r in range(self.SIZE)]
            row = original[:]
            if direction in ("right", "down"):
                row.reverse()
            new_row, gained = self._slide_row(row)
            if direction in ("right", "down"):
                new_row.reverse()
            if new_row != original:
                moved = True
                if direction in ("left", "right"):
                    self.grid[i] = new_row
                else:
                    for r in range(self.SIZE):
                        self.grid[r][i] = new_row[r]
            gained_total += gained
        if moved:
            self.score += gained_total
            self.highest = max(self.highest, max(max(row) for row in self.grid))
        return moved

    def move(self, direction):
        """Attempt a move; spawn a tile if the board changed. Returns True if moved."""
        if self.over:
            return False
        if not self._move(direction):
            return False
        self.add_random_tile()
        if not self.can_move():
            self.over = True
        return True

    def can_move(self):
        if self.empty_cells():
            return True
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                v = self.grid[r][c]
                if c + 1 < self.SIZE and self.grid[r][c + 1] == v:
                    return True
                if r + 1 < self.SIZE and self.grid[r + 1][c] == v:
                    return True
        return False