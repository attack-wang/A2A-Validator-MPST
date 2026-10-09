class Game:
    def __init__(self):
        self.board = Board(GRID_SIZE)
        self.score = 0
        self.game_over = False
        self.won = False
        self.keep_playing = False  # optional: continue after 2048
    def new_game(self):
        ...
    def handle_move(self, direction):
        """Returns True if the move was valid (board changed)."""
        if self.game_over:
            return False
        moved, gained = self.board.move(direction)
        if not moved:
            return False
        self.score += gained
        self.board.spawn_random_tile()
        if not self.board.can_move():
            self.game_over = True
        # win check
        if not self.won and self.board.get_highest_tile() >= 2048:
            self.won = True
        return True