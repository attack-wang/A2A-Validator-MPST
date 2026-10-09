'''
scoreboard.py
Keeps track of both players' points, decides when the winning score
threshold is reached and renders the scores on screen.
'''
import pygame
import settings
class Scoreboard:
    """Tracks the score of both players and the win condition."""
    def __init__(self, winning_score=settings.WINNING_SCORE):
        self.winning_score = winning_score
        self.scores = {1: 0, 2: 0}
        self.font = pygame.font.SysFont("consolas", 48, bold=True)
    def score_point(self, player):
        """Award one point to `player` (1 or 2)."""
        if player in self.scores:
            self.scores[player] += 1
    def get_score(self, player):
        return self.scores.get(player, 0)
    def has_winner(self):
        return self.scores[1] >= self.winning_score or self.scores[2] >= self.winning_score
    def get_winner(self):
        """Return the number of the winning player, or None."""
        if self.scores[1] >= self.winning_score:
            return 1
        if self.scores[2] >= self.winning_score:
            return 2
        return None
    def reset(self):
        self.scores = {1: 0, 2: 0}
    def draw(self, screen):
        p1 = self.font.render(str(self.scores[1]), True, settings.WHITE)
        p2 = self.font.render(str(self.scores[2]), True, settings.WHITE)
        screen.blit(p1, (settings.WIDTH // 2 - 60 - p1.get_width() // 2, 20))
        screen.blit(p2, (settings.WIDTH // 2 + 60 - p2.get_width() // 2, 20))