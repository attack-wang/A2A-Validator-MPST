import random
class Board:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[None] * size for _ in range(size)]
        self.spawn_random_tile()
        self.spawn_random_tile()
    def get_empty_cells(self):
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] is None]
    def spawn_random_tile(self):
        empty = self.get_empty_cells()
        if not empty:
            return None
        r, c = random.choice(empty)
        value = 2 if random.random() < 0.9 else 4
        tile = Tile(value, r, c)
        tile.is_new = True
        tile.prev_row, tile.prev_col = r, c
        self.grid[r][c] = tile
        return tile
    def move(self, direction):
        # record previous positions, reset flags
        for r in range(self.size):
            for c in range(self.size):
                tile = self.grid[r][c]
                if tile:
                    tile.prev_row, tile.prev_col = tile.row, tile.col
                    tile.is_new = False
                    tile.is_merged = False
                    tile.merged_from = []
        moved = False
        gained = 0
        for index in range(self.size):
            line = self._get_line(index, direction)
            new_line, line_score, line_moved = self._slide_line(line)
            self._set_line(index, direction, new_line)
            gained += line_score
            moved = moved or line_moved
        return moved, gained