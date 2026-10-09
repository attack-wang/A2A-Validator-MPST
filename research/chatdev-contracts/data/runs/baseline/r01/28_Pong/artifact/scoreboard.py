'''
scoreboard.py
Defines the Scoreboard class: tracks both players' scores, checks the
winning threshold, and renders the scores on screen.
'''
import pygame
import constants as c
class Scoreboard:
    '''Tracks and displays the score of both players.'''
    def __init__(self):
        '''Start both scores at zero.'''
        self.left_score = 0
        self.right_score = 0
        self.font = pygame.font.Font(None, c.FONT_SIZE_SCORE)
    def increment_left(self):
        '''Add one point to the left player.'''
        self.left_score += 1
    def increment_right(self):
        '''Add one point to the right player.'''
        self.right_score += 1
    def has_winner(self):
        '''True when either player reached the winning score.'''
        return self.left_score >= c.WINNING_SCORE or self.right_score >= c.WINNING_SCORE
    def get_winner(self):
        '''Return "left" or "right" depending on who won (None if no winner).'''
        if self.left_score >= c.WINNING_SCORE:
            return "left"
        if self.right_score >= c.WINNING_SCORE:
            return "right"
        return None
    def reset(self):
        '''Set both scores back to zero for a new match.'''
        self.left_score = 0
        self.right_score = 0
    def draw(self, surface):
        '''Render both scores near the top of the window.'''
        left_text = self.font.render(str(self.left_score), True, c.COLOR_PADDLE_LEFT)
        right_text = self.font.render(str(self.right_score), True, c.COLOR_PADDLE_RIGHT)
        surface.blit(left_text, (c.WINDOW_WIDTH // 4 - left_text.get_width() // 2, 20))
        surface.blit(right_text, (3 * c.WINDOW_WIDTH // 4 - right_text.get_width() // 2, 20))