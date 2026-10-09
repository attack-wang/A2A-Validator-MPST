'''
scoreboard.py
Tracks both players' scores, renders them on screen and decides when
the winning score threshold has been reached.
'''
import pygame
import settings
class Scoreboard:
    """Keeps the score for both players and detects a winner."""
    def __init__(self, font):
        """Create a scoreboard using `font` to render the score digits."""
        self.font = font
        self.winning_score = settings.WINNING_SCORE
        self.left_score = 0
        self.right_score = 0
    def award_point(self, side):
        """Give one point to `side` ("left" or "right")."""
        if side == "left":
            self.left_score += 1
        elif side == "right":
            self.right_score += 1
    def has_winner(self):
        """Return True once either player reaches the winning score."""
        return self.winner_side() is not None
    def winner_side(self):
        """Return "left"/"right" for the winner, or None if nobody won yet."""
        if self.left_score >= self.winning_score:
            return "left"
        if self.right_score >= self.winning_score:
            return "right"
        return None
    def reset(self):
        """Set both scores back to zero for a new match."""
        self.left_score = 0
        self.right_score = 0
    def draw(self, surface):
        """Render both scores near the top of the screen."""
        left_text = self.font.render(str(self.left_score), True, settings.COLOR_PADDLE_LEFT)
        right_text = self.font.render(str(self.right_score), True, settings.COLOR_PADDLE_RIGHT)
        left_pos = (settings.SCREEN_WIDTH // 4 - left_text.get_width() // 2, 16)
        right_pos = (3 * settings.SCREEN_WIDTH // 4 - right_text.get_width() // 2, 16)
        surface.blit(left_text, left_pos)
        surface.blit(right_text, right_pos)