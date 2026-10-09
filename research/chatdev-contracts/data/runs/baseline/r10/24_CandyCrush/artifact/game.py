class Game:
    STATE_IDLE, STATE_SWAPPING, STATE_CLEARING, STATE_FALLING, STATE_GAME_OVER = ...
    def __init__(self):
        self.board = Board(GRID_SIZE, GRID_SIZE)
        self.score = 0
        self.moves_left = INITIAL_MOVES
        self.state = IDLE
        self.selected = None  # (r,c)
        self.cascade = 0
        self.pending_swap = None  # (r1,c1,r2,c2, revert)
        self.hint = None
        self.floaters = []
        self.message = None  # transient message
    def handle_click(self, pos): ...
    def handle_drag(...)?  # maybe just clicks
    def try_swap(self, r1,c1,r2,c2): ...
    def update(self, dt): ...  # state machine progression
    def add_score(...)