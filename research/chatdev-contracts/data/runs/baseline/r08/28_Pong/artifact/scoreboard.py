'''Scoreboard: tracks both players' points and the win condition.'''
import pygame
import settings
class Scoreboard:
    '''Stores scores, detects a winner, and renders the HUD.'''
    def __init__(self):
        self.scores = [0, 0]  # index 0 -> player 1 (left), 1 -> player 2 (right)
        self.winning_score = settings.WINNING_SCORE
        self.score_font = pygame.font.Font(settings.FONT_NAME, settings.SCORE_FONT_SIZE)
        self.message_font = pygame.font.Font(settings.FONT_NAME, settings.MESSAGE_FONT_SIZE)
        self.small_font = pygame.font.Font(settings.FONT_NAME, settings.SMALL_FONT_SIZE)
    def score_point(self, player_index):
        '''Add one point to the given player (0 or 1).'''
        self.scores[player_index] += 1
    def get_winner(self):
        '''Return the index of the winning player, or None if no one has won yet.'''
        for index, score in enumerate(self.scores):
            if score >= self.winning_score:
                return index
        return None
    def reset(self):
        self.scores = [0, 0]
    def draw(self, surface):
        # Big score numbers near the top on each half
        ...