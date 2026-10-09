class Renderer:
    def __init__(self, game):
        pygame.init()
        self.screen = pygame.display.set_mode(...)
        pygame.display.set_caption("2048")
        self.clock = pygame.time.Clock()
        self.fonts = {...}
        self.game = game
        self.move_start_time = None  # animation start
    def start_move_animation(self):
        self.move_start_time = pygame.time.get_ticks()
    def draw(self):
        self.screen.fill(BACKGROUND)
        self._draw_header()  # title, score, highest tile
        self._draw_board()
        self._draw_messages()  # game over overlay, win banner, help text
        pygame.display.flip()
    def _draw_header(self):
        # "2048" title, score box, highest tile box
    def _draw_board(self):
        # board background rounded rect
        # empty cells
        # tiles with animation
    def _draw_tile(self, tile, x, y, size, alpha=255):
        # rounded rect with color by value, centered text
    def _animation_progress(self):
        # returns (slide_t, pop_t) or (1.0, 1.0) if no animation