'''
Scoreboard module: tracks both players' scores, detects a winner,
and renders the score digits and the winner banner.
'''
import pygame
import settings
class Scoreboard:
    '''Tracks and displays the score for both players.'''
    def __init__(self):
        '''Start both scores at zero and prepare the fonts.'''
        self.score_left = 0   # Player 1 (left paddle)
        self.score_right = 0  # Player 2 (right paddle)
        self.font = pygame.font.Font(settings.FONT_NAME, settings.SCORE_FONT_SIZE)
        self.message_font = pygame.font.Font(settings.FONT_NAME, settings.MESSAGE_FONT_SIZE)
    def score_point(self, player):
        '''Add one point to `player` ('left' or 'right').'''
        if player == 'left':
            self.score_left += 1
        else:
            self.score_right += 1
    def has_winner(self):
        '''Return True once either player reaches the winning score.'''
        return self.score_left >= settings.WINNING_SCORE or self.score_right >= settings.WINNING_SCORE
    def get_winner(self):
        '''Return the winning side ('left' or 'right'), or None if no winner yet.'''
        if self.score_left >= settings.WINNING_SCORE:
            return 'left'
        if self.score_right >= settings.WINNING_SCORE:
            return 'right'
        return None
    def reset_scores(self):
        '''Set both scores back to zero for a new match.'''
        self.score_left = 0
        self.score_right = 0
    def draw(self, screen):
        '''Render both scores at the top of the screen.'''
        left_text = self.font.render(str(self.score_left), True, settings.WHITE)
        right_text = self.font.render(str(self.score_right), True, settings.WHITE)
        screen.blit(left_text, (settings.SCREEN_WIDTH // 2 - 80, 20))
        screen.blit(right_text, (settings.SCREEN_WIDTH // 2 + 40, 20))
        # NOTE: the dashed center line is drawn by Game.draw_center_line();
        # it is intentionally NOT duplicated here.
    def draw_winner(self, screen):
        '''Display the winner banner and restart hint (called only when game_over).'''
        if self.get_winner() == 'left':
            text = "Player 1 (Left) wins!"
        else:
            text = "Player 2 (Right) wins!"
        msg = self.message_font.render(text, True, settings.GREEN)
        screen.blit(msg, msg.get_rect(center=(settings.SCREEN_WIDTH // 2,
                                              settings.SCREEN_HEIGHT // 2 - 30)))
        hint = self.message_font.render("Press R to play again", True, settings.WHITE)
        screen.blit(hint, hint.get_rect(center=(settings.SCREEN_WIDTH // 2,
                                                settings.SCREEN_HEIGHT // 2 + 30)))