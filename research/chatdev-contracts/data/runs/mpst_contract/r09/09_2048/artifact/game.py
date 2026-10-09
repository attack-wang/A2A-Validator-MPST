"""Core logic for the 2048 game."""
import random


class Game2048:
    SIZE = 4

    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = [[0] * self.SIZE for _ in range(self.SIZE)]
        self.score = 0
        self.best_tile = 0
        self.add_random_tile()
        self.add_random_tile()

    def empty_cells(self):
        return [(r, c) for r in range(self.SIZE)
                for c in range(self.SIZE) if self.grid[r][c] == 0]

    def add_random_tile(self):
        cells = self.empty_cells()
        if not cells:
            return False
        r, c = random.choice(cells)
        self.grid[r][c] = 2 if random.random() < 0.9 else 4
        self.best_tile = max(self.best_tile, self.grid[r][c])
        return True

    @staticmethod
    def _slide_left(line):
        tiles = [v for v in line if v]
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
        merged.extend([0] * (len(line) - len(merged)))
        return merged, gained, merged != list(line)

    def move(self, direction):
        """Slide all tiles in direction ('left'|'right'|'up'|'down').

        Equal neighbours merge once per move, the merge values are added to
        the score, a new tile spawns afterwards, and True is returned when
        the board changed.
        """
        if direction not in ("left", "right", "up", "down"):
            return False
        moved = False
        gained_total = 0
        for i in range(self.SIZE):
            if direction in ("left", "right"):
                line = list(self.grid[i])
            else:
                line = [self.grid[r][i] for r in range(self.SIZE)]
            reverse = direction in ("right", "down")
            if reverse:
                line.reverse()
            new_line, gained, line_moved = self._slide_left(line)
            gained_total += gained
            if reverse:
                new_line.reverse()
            if line_moved:
                moved = True
                if direction in ("left", "right"):
                    self.grid[i] = new_line
                else:
                    for r in range(self.SIZE):
                        self.grid[r][i] = new_line[r]
        if moved:
            self.score += gained_total
            self.best_tile = max(self.best_tile,
                                 max(v for row in self.grid for v in row))
            self.add_random_tile()
        return moved

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

    def game_over(self):
        return not self.can_move()