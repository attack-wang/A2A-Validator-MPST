'''
scoreboard.py
Score tracking and HUD rendering for the Pong match.
Keeps both players' scores, decides when the winning threshold is
reached, and draws the in-game HUD (scores, center line, labels) as
well as the game-over banner.
'''
import pygame
from settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINNING_SCORE,
    COLOR_CENTER_LINE,
    COLOR_TEXT,
    COLOR_WIN_TEXT,
    COLOR_OVERLAY,
    COLOR_PADDLE_LEFT,
    COLOR_PADDLE_RIGHT,
)
class Scoreboard:
    """Tracks the match score and renders all score-related UI."""
    def __init__(self):
        self.left_score = 0
        self.right_score = 0
        self.font_score = pygame.font.SysFont("consolas", 64, bold=True)
        self.font_label = pygame.font.SysFont("consolas", 22, bold=True)
        self.font_banner = pygame.font.SysFont("consolas", 58, bold=True)
        self.font_hint = pygame.font.SysFont("consolas", 26)
    def reset(self):
        """Zero both scores for a fresh match."""
        self.left_score = 0
        self.right_score = 0
    def award_left(self):
        """Give one point to the left player."""
        self.left_score += 1
    def award_right(self):
        """Give one point to the right player."""
        self.right_score += 1
    def has_winner(self):
        """True when either player reached the winning score threshold."""
        return self.left_score >= WINNING_SCORE or self.right_score >= WINNING_SCORE
    def winner_side(self):
        """Return 'LEFT' or 'RIGHT' for the winner, or None if the match is ongoing."""
        if self.left_score >= WINNING_SCORE:
            return "LEFT"
        if self.right_score >= WINNING_SCORE:
            return "RIGHT"
        return None
    def draw_center_line(self, surface):
        """Draw the dashed vertical line separating the two field halves."""
        dash_height = 18
        gap = 14
        x = WINDOW_WIDTH // 2 - 2
        y = 0
        while y < WINDOW_HEIGHT:
            pygame.draw.rect(surface, COLOR_CENTER_LINE, (x, y, 4, dash_height))
            y += dash_height + gap
    def draw(self, surface):
        """Render the center line, both scores and the player labels."""
        self.draw_center_line(surface)
        left_text = self.font_score.render(str(self.left_score), True, COLOR_PADDLE_LEFT)
        right_text = self.font_score.render(str(self.right_score), True, COLOR_PADDLE_RIGHT)
        surface.blit(left_text, left_text.get_rect(center=(WINDOW_WIDTH * 0.25, 60)))
        surface.blit(right_text, right_text.get_rect(center=(WINDOW_WIDTH * 0.75, 60)))
        left_label = self.font_label.render("PLAYER 1  (W/S)", True, COLOR_TEXT)
        right_label = self.font_label.render("PLAYER 2  (UP/DOWN)", True, COLOR_TEXT)
        surface.blit(left_label, left_label.get_rect(midbottom=(WINDOW_WIDTH * 0.25, WINDOW_HEIGHT - 12)))
        surface.blit(right_label, right_label.get_rect(midbottom=(WINDOW_WIDTH * 0.75, WINDOW_HEIGHT - 12)))
    def draw_winner_overlay(self, surface):
        """Dim the field and announce the winner with a restart hint."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*COLOR_OVERLAY, 200))
        surface.blit(overlay, (0, 0))
        winner = self.winner_side()
        if winner == "LEFT":
            banner_text = "PLAYER 1 WINS!"
            banner_color = COLOR_PADDLE_LEFT
        else:
            banner_text = "PLAYER 2 WINS!"
            banner_color = COLOR_PADDLE_RIGHT
        banner = self.font_banner.render(banner_text, True, banner_color)
        surface.blit(banner, banner.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)))
        final = self.font_hint.render(
            "Final score  {} - {}".format(self.left_score, self.right_score), True, COLOR_TEXT)
        surface.blit(final, final.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)))
        hint = self.font_hint.render("Press SPACE to play again  |  ESC to quit", True, COLOR_WIN_TEXT)
        surface.blit(hint, hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80)))