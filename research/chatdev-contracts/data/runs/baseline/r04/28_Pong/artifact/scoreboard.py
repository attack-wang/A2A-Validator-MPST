'''
scoreboard.py
Keeps track of both players' points, detects the winner, and renders scores.
'''
import pygame
from settings import (
    FONT_NAME,
    FONT_SIZE_SCORE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINNING_SCORE,
    COLOR_SCORE,
)
class Scoreboard:
    """Stores scores for [left, right] and renders them on screen."""
    def __init__(self):
        self.scores = [0, 0]
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SCORE, bold=True)
    def reset(self):
        self.scores = [0, 0]
    def score_point(self, player_index):
        """Add one point to player 0 (left) or 1 (right)."""
        self.scores[player_index] += 1
    def get_winner(self):
        """Return index of the player who reached WINNING_SCORE, else None."""
        for index, score in enumerate(self.scores):
            if score >= WINNING_SCORE:
                return index
        return None
    def draw(self, surface):
        for index, score in enumerate(self.scores):
            text = self.font.render(str(score), True, COLOR_SCORE)
            center_x = WINDOW_WIDTH * (0.25 if index == 0 else 0.75)
            rect = text.get_rect(center=(center_x, WINDOW_HEIGHT * 0.12))
            surface.blit(text, rect)