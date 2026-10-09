class Game2048:
    def __init__(self, grid_size=4, starting_tiles=2, two_probability=0.9):
        '''Create a fresh board and place the initial random tiles.'''
        self.grid_size = grid_size
        self.two_probability = two_probability
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        self.board = [[0] * grid_size for _ in range(grid_size)]
        for _ in range(starting_tiles):
            self.spawn_tile()
    def reset(self):
        '''Restore the game to its initial state (empty board, zero score).'''
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        for _ in range(2):
            self.spawn_tile()