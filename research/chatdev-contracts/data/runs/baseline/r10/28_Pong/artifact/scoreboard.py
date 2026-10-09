'''
scoreboard.py
Defines the Scoreboard class: tracks both players' scores, determines
the winner, and renders the scores on screen.
'''
import pygame
import settings
class Scoreboard:
    """Tracks and displays the scores of the two players."""
    def __init__(self):
        """Initialize both scores to zero and prepare fonts."""
        self.score_left = 0
        self.score_right = 0
        self.score_font = pygame.font.Font(settings.FONT_NAME, settings.SCORE_FONT_SIZE)
        self.message_font = pygame.font.Font(settings.FONT_NAME, settings.MESSAGE_FONT_SIZE)
        self.small_font = pygame.font.Font(settings.FONT_NAME, settings.SMALL_FONT_SIZE)
    def increase_score(self, player):
        """Add one point to the given player ('left' or 'right')."""
        if player == 'left':
            self.score_left += 1
        elif player == 'right':
            self.score_right += 1
    def has_winner(self):
        """Return True if either player reached the winning score."""
        return self.score_left >= settings.WINNING_SCORE or \
               self.score_right >= settings.WINNING_SCORE
    def get_winner(self):
        """Return 'left' or 'right' for the winning player, or None."""
        if self.score_left >= settings.WINNING_SCORE:
            return 'left'
        if self.score_right >= settings.WINNING_SCORE:
            return 'right'
        return None
    def reset(self):
        """Reset both scores to zero for a new match."""
        self.score_left = 0
        self.score_right = 0
    def draw(self, screen):
        """Render both scores near the top of the screen."""
        score_text = f"{self.score_left}   {self.score_right}"
        surface = self.score_font.render(score_text, True, settings.WHITE)
        rect = surface.get_rect(center=(settings.SCREEN_WIDTH // 2, 50))
        screen.blit(surface, rect)