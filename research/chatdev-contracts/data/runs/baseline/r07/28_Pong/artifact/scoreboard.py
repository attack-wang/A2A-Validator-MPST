'''
scoreboard.py
Defines the Scoreboard class: tracks both players' scores and renders them.
'''
import pygame
from constants import (WINDOW_WIDTH, FONT_SCORE_SIZE, COLOR_TEXT,
                       COLOR_PADDLE_LEFT, COLOR_PADDLE_RIGHT, WINNING_SCORE)
class Scoreboard:
    '''Keeps the score for both players and draws it at the top of the window.'''
    def __init__(self):
        '''Start a fresh match with both scores at zero.'''
        self.left_score = 0
        self.right_score = 0
        self.font = pygame.font.SysFont("consolas", FONT_SCORE_SIZE, bold=True)
    def reset(self):
        '''Reset both scores to zero for a new match.'''
        self.left_score = 0
        self.right_score = 0
    def score_left(self):
        '''Award one point to the left player.'''
        self.left_score += 1
    def score_right(self):
        '''Award one point to the right player.'''
        self.right_score += 1
    def has_winner(self):
        '''Return True once either player reaches the winning score threshold.'''
        return self.left_score >= WINNING_SCORE or self.right_score >= WINNING_SCORE
    def get_winner(self):
        '''Return "LEFT PLAYER" or "RIGHT PLAYER" for whoever reached the threshold.'''
        if self.left_score >= WINNING_SCORE:
            return "LEFT PLAYER"
        return "RIGHT PLAYER"
    def draw(self, surface):
        '''Render both scores near the top of the window.'''
        left_text = self.font.render(str(self.left_score), True, COLOR_PADDLE_LEFT)
        right_text = self.font.render(str(self.right_score), True, COLOR_PADDLE_RIGHT)
        left_rect = left_text.get_rect(center=(WINDOW_WIDTH // 4, FONT_SCORE_SIZE // 2 + 10))
        right_rect = right_text.get_rect(center=(3 * WINDOW_WIDTH // 4, FONT_SCORE_SIZE // 2 + 10))
        surface.blit(left_text, left_rect)
        surface.blit(right_text, right_rect)