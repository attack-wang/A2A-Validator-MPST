class Renderer:
    """Draws the board, pieces, sidebar, and overlays."""
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont / Font(None, sizes)
    def draw(self, game):
        self.draw_board(game)
        self.draw_ghost(game)
        self.draw_current_piece(game)
        self.draw_sidebar(game)
        self.draw_overlays(game)