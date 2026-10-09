class Game:
    STATE_IDLE = "idle"
    STATE_SWAPPING = "swapping"
    STATE_CLEARING = "clearing"
    STATE_FALLING = "falling"
    STATE_WON = "won"
    STATE_LOST = "lost"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.Font(None, 44)
        self.font_mid = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.sprites = [self._make_candy_sprite(t) for t in range(config.NUM_CANDY_TYPES)]
        self.reset()