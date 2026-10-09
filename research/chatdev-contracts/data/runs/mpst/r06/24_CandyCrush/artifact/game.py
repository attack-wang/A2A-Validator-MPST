class Game:
    STATE_IDLE = "idle"
    STATE_SWAPPING = "swapping"
    STATE_RESOLVING = "resolving"
    STATE_GAME_OVER = "game_over"
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 20)
        self.font_big = pygame.font.SysFont("arial", 30, bold=True)
        self.font_small = pygame.font.SysFont("arial", 15)
        self.sounds = Sounds()
        self.restart_button = pygame.Rect(
            config.SIDEBAR_X + 16, config.BOARD_Y + 330,
            config.SIDEBAR_WIDTH - 32, 44)
        self.high_score = self._load_high_score()
        self.drag_start = None
        self.hint_cells = None
        self.hint_timer = 0.0
        self.reset()