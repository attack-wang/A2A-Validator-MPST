"""Core 2048 game logic: grid, moves, merges, score and game-over detection."""
import random


class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.reset()

    def reset(self):
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.highest = 0
        self.over = False
        self.add_random_tile()
        self.add_random_tile()
        self.highest = self._max_tile()

    def _max_tile(self):
        return max(max(row) for row in self.grid)

    def empty_cells(self):
        return [(r, c) for r in range(self.size) for c in range(self.size)
                if self.grid[r][c] == 0]

    def add_random_tile(self):
        empty = self.empty_cells()
        if not empty:
            return False
        r, c = random.choice(empty)
        self.grid[r][c] = 2 if random.random() < 0.9 else 4
        return True

    @staticmethod
    def _slide(row):
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
        merged.extend([0] * (len(row) - len(merged)))
        return merged, gained

    def move(self, direction):
        """Slide all tiles in direction ('left', 'right', 'up', 'down')."""
        if self.over:
            return False
        moved = False
        gained_total = 0
        n = self.size
        for i in range(n):
            if direction in ("left", "right"):
                original = self.grid[i][:]
            else:
                original = [self.grid[j][i] for j in range(n)]
            work = original[::-1] if direction in ("right", "down") else original
            new_line, gained = self._slide(work)
            if direction in ("right", "down"):
                new_line = new_line[::-1]
            if new_line != original:
                moved = True
                if direction in ("left", "right"):
                    self.grid[i] = new_line
                else:
                    for j in range(n):
                        self.grid[j][i] = new_line[j]
            gained_total += gained
        if moved:
            self.score += gained_total
            self.add_random_tile()
            self.highest = max(self.highest, self._max_tile())
            if not self.moves_available():
                self.over = True
        return moved

    def moves_available(self):
        n = self.size
        for r in range(n):
            for c in range(n):
                v = self.grid[r][c]
                if v == 0:
                    return True
                if c + 1 < n and self.grid[r][c + 1] == v:
                    return True
                if r + 1 < n and self.grid[r + 1][c] == v:
                    return True
        return False