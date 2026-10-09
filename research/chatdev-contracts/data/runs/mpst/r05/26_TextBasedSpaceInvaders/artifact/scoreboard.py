def __init__(self, settings, screen):
    self.settings = settings
    self.screen = screen
    self.font = pygame.font.SysFont("consolas", 22, bold=True)
    self.small_font = pygame.font.Font(None, 20)
    self.high_score = 0
    self.reset()
def reset(self):
    """Reset the score for a new game (high score persists in memory)."""
    self.score = 0