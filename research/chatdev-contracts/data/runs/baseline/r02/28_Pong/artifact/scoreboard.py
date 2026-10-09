'''
scoreboard.py
Tracks both players' scores, decides when the winning threshold is
reached and renders the score on screen.
'''
import pygame
import settings
class Scoreboard:
    """Keeps the score of the two players and renders it."""
    def __init__(self):
        """Create the fonts and start both scores at zero."""
        self.left_score = 0
        self.right_score = 0
        self.font = pygame.font.SysFont("consolas", 56, bold=True)
        self.small_font = pygame.font.SysFont("consolas", 24)
    def increment(self, side):
        """Add one point to the given side ('left' or 'right')."""
        if side == "left":
            self.left_score += 1
        elif side == "right":
            self.right_score += 1
    def get_winner(self):
        """Return 'left'/'right' if someone reached the winning score, else None."""
        if self.left_score >= settings.WINNING_SCORE:
            return "left"
        if self.right_score >= settings.WINNING_SCORE:
            return "right"
        return None
    def reset(self):
        """Set both scores back to zero (new match)."""
        self.left_score = 0
        self.right_score = 0
    def draw(self, surface):
        """Render the big scores near the top, each on its own half."""
        left_text = self.font.render(str(self.left_score), True, settings.COLOR_PADDLE_LEFT)
        right_text = self.font.render(str(self.right_score), True, settings.COLOR_PADDLE_RIGHT)
        surface.blit(left_text, (settings.SCREEN_WIDTH // 4 - left_text.get_width() // 2, 20))
        surface.blit(right_text, (3 * settings.SCREEN_WIDTH // 4 - right_text.get_width() // 2, 20))