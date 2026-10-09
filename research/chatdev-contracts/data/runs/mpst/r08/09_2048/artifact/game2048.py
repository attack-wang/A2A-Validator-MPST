class Game2048:
    def __init__(self):
        self.size = 4
        self.grid = [[None]*4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.spawn_tile()
        self.spawn_tile()
    def move(self, direction):
        # vectors
        vectors = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        dr, dc = vectors[direction]
        # traversal order: if moving right, traverse columns from right to left, etc.
        ...