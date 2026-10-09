import random
class Game2048:
    GRID_SIZE = 4
    def __init__(self):
        self.grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.won = False  # maybe track if reached 2048
        self.spawn_tile()
        self.spawn_tile()
    def reset(self):
        ...
    def spawn_tile(self):
        empty = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
        if not empty:
            return False
        r, c = random.choice(empty)
        self.grid[r][c] = 2 if random.random() < 0.9 else 4
        return True
    def move(self, direction):
        # direction: 'up', 'down', 'left', 'right'
        # returns True if the move changed the board
        moved = False
        ...