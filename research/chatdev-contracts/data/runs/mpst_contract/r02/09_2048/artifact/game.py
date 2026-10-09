import random


class Game:
    """Core 2048 logic on a size x size grid (default 4x4)."""

    def __init__(self, size=4):
        self.size = size
        self.reset()

    def reset(self):
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.best = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        """Spawn a 2 (90%) or 4 (10%) in a random empty cell."""
        empty = [(r, c) for r in range(self.size) for c in range(self.size)
                 if self.grid[r][c] == 0]
        if not empty:
            return False
        r, c = random.choice(empty)
        self.grid[r][c] = 4 if random.random() < 0.1 else 2
        self.best = max(self.best, self.grid[r][c])
        return True

    @staticmethod
    def _slide_left(line):
        """Compress and merge one line toward index 0."""
        tiles = [v for v in line if v]
        result = []
        gained = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged = tiles[i] * 2
                result.append(merged)
                gained += merged
                i += 2
            else:
                result.append(tiles[i])
                i += 1
        result += [0] * (len(line) - len(result))
        return result, gained, result != line

    def move(self, direction):
        """Slide all tiles in 'left'/'right'/'up'/'down'; spawn a tile if moved."""
        if direction not in ('left', 'right', 'up', 'down'):
            return False
        n = self.size
        if direction in ('left', 'right'):
            lines = [self.grid[r][:] for r in range(n)]
        else:
            lines = [[self.grid[r][c] for r in range(n)] for c in range(n)]
        if direction in ('right', 'down'):
            lines = [line[::-1] for line in lines]
        moved = False
        gained = 0
        new_lines = []
        for line in lines:
            new_line, g, m = self._slide_left(line)
            gained += g
            moved = moved or m
            new_lines.append(new_line)
        if not moved:
            return False
        if direction in ('right', 'down'):
            new_lines = [line[::-1] for line in new_lines]
        if direction in ('left', 'right'):
            self.grid = [line[:] for line in new_lines]
        else:
            for c in range(n):
                for r in range(n):
                    self.grid[r][c] = new_lines[c][r]
        self.score += gained
        self.add_random_tile()
        self.best = max(self.best, max(max(row) for row in self.grid))
        return True

    def can_move(self):
        """True if any empty cell or any adjacent equal pair exists."""
        n = self.size
        for r in range(n):
            for c in range(n):
                if self.grid[r][c] == 0:
                    return True
                if c + 1 < n and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r + 1 < n and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False