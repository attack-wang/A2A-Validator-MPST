'''
scoreboard.py
Scoreboard class: tracks and displays player scores.
Keeps both players' points, detects the winner against the
winning-score threshold, and renders the scores on screen.
'''
import pygame
import settings
class Scoreboard:
    '''Tracks both players' scores and renders them on screen.'''
    def __init__(self):
        '''Initialize scores to zero and prepare fonts.'''
        self.score_left = 0   # Player 1 (left paddle)
        self.score_right = 0  # Player 2 (right paddle)
        self.font = pygame.font.Font(settings.FONT_NAME, settings.SCORE_FONT_SIZE)
    def score_point(self, player):
        '''Add one point to the given player (1 = left, 2 = right).'''
        if player == 1:
            self.score_left += 1
        elif player == 2:
            self.score_right += 1
    def has_winner(self):
        '''Return True if either player reached the winning score.'''
        return (self.score_left >= settings.WINNING_SCORE
                or self.score_right >= settings.WINNING_SCORE)
    def get_winner(self):
        '''Return the winning player number (1 or 2), or None if no winner yet.'''
        if self.score_left >= settings.WINNING_SCORE:
            return 1
        if self.score_right >= settings.WINNING_SCORE:
            return 2
        return None
    def reset(self):
        '''Reset both scores to zero.'''
        self.score_left = 0
        self.score_right = 0
    def draw(self, surface):
        '''Render both scores near the top of the screen.'''
        text_left = self.font.render(str(self.score_left), True, settings.WHITE)
        text_right = self.font.render(str(self.score_right), True, settings.WHITE)
        left_pos = (settings.SCREEN_WIDTH * 0.25 - text_left.get_width() / 2, 20)
        right_pos = (settings.SCREEN_WIDTH * 0.75 - text_right.get_width() / 2, 20)
        surface.blit(text_left, left_pos)
        surface.blit(text_right, right_pos)