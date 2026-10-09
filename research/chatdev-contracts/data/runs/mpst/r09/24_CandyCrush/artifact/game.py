class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("Candy Match — Match-3 Puzzle")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("arial", 30, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.reset_game()
    def reset_game(self):
        self.board = Board()
        self.score = 0
        self.moves = 0
        self.cascade_level = 0
        self.time_left = config.TIME_LIMIT
        self.state = STATE_IDLE
        self.selected = None  # (row, col)
        self.swap_pair = None  # (candy_a, candy_b)
        self.clearing = []  # candies being cleared
        self.pending_groups = []
        self.message = ""
        self.message_timer = 0.0
        self.hint = None
        self.hint_timer = 0.0
        self.best_score = loaded from file? maybe skip persistence... 