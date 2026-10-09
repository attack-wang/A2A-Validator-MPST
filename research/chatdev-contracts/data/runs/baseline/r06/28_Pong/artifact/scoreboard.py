'''
scoreboard.py
Defines the Scoreboard class: tracks both players' scores, the winning
score threshold, and renders the scores on screen.
'''
import pygame
from constants import (
    SCREEN_WIDTH, SCORE_FONT_SIZE, SMALL_FONT_SIZE,
    P1_COLOR, P2_COLOR, GRAY, WINNING_SCORE,
)
class Scoreboard:
    """Tracks and displays the score for both players."""
    def __init__(self, winning_score=WINNING_SCORE):
        self.winning_score = winning_score
        self.scores = [0, 0]
        self._score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
        self._label_font = pygame.font.Font(None, SMALL_FONT_SIZE)
    def score_point(self, player_index):
        """Award one point to the given player (0 or 1)."""
        if player_index in (0, 1):
            self.scores[player_index] += 1
    def get_winner(self):
        """Return the index of the winning player, or None if no one has won yet."""
        for idx, score in enumerate(self.scores):
            if score >= self.winning_score:
                return idx
        return None
    def reset(self):
        """Set both players' scores back to zero."""
        self.scores = [0, 0]
    def draw(self, surface):
        """Render both color-coded scores and the winning-score label."""
        p1 = self._score_font.render(str(self.scores[0]), True, P1_COLOR)
        p2 = self._score_font.render(str(self.scores[1]), True, P2_COLOR)
        surface.blit(p1, p1.get_rect(midright=(SCREEN_WIDTH // 2 - 30, 50)))
        surface.blit(p2, p2.get_rect(midleft=(SCREEN_WIDTH // 2 + 30, 50)))
        label = self._label_font.render(
            f"First to {self.winning_score}", True, GRAY)
        surface.blit(label, label.get_rect(midtop=(SCREEN_WIDTH // 2, 20)))