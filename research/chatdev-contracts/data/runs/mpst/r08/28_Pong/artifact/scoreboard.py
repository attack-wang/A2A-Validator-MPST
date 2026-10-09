'''
scoreboard.py
Defines the Scoreboard class: score tracking, winner determination,
and on-screen rendering of scores and centered text messages.
'''
import pygame
from constants import (SCREEN_WIDTH, WINNING_SCORE, WHITE, GRAY)
class Scoreboard:
    """Tracks both players' scores and renders them on screen."""
    def __init__(self):
        self.scores = [0, 0]
        self.font_large = None
        self.font_small = None
        self._load_fonts()
    def _load_fonts(self):
        """Create the fonts used for scores and messages."""
        try:
            self.font_large = pygame.font.Font(None, 72)
            self.font_small = pygame.font.Font(None, 32)
        except Exception:
            self.font_large = pygame.font.SysFont(None, 72)
            self.font_small = pygame.font.SysFont(None, 32)
    def reset(self):
        """Set both scores back to zero."""
        self.scores = [0, 0]
    def award_point(self, player_index):
        """Add one point to the given player (0 = player 1, 1 = player 2)."""
        if 0 <= player_index < len(self.scores):
            self.scores[player_index] += 1
    def get_winner(self):
        """Return the index of the winning player, or None if no one has won."""
        for i, score in enumerate(self.scores):
            if score >= WINNING_SCORE:
                return i
        return None
    def draw(self, screen):
        """Render both scores near the top of the court."""
        if self.font_large is None:
            self._load_fonts()
        score1_text = self.font_large.render(str(self.scores[0]), True, WHITE)
        score2_text = self.font_large.render(str(self.scores[1]), True, WHITE)
        screen.blit(score1_text, (SCREEN_WIDTH // 4 - score1_text.get_width() // 2, 20))
        screen.blit(score2_text, (3 * SCREEN_WIDTH // 4 - score2_text.get_width() // 2, 20))
    def draw_center_text(self, screen, text, color=WHITE, y_offset=0, small=False):
        """Render a text message centered horizontally, offset vertically."""
        if self.font_small is None:
            self._load_fonts()
        font = self.font_small if small else self.font_large
        surface = font.render(text, True, color)
        x = (SCREEN_WIDTH - surface.get_width()) // 2
        y = (SCREEN_HEIGHT - surface.get_height()) // 2 + y_offset
        screen.blit(surface, (x, y))