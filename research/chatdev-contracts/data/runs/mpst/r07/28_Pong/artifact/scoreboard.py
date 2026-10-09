'''
scoreboard.py
Defines the Scoreboard class: keeps both players' scores, detects the
winning score threshold and renders the score, centre messages and the
game-over text on screen.
'''
import pygame
import settings
class Scoreboard:
    """Tracks the score of both players and the win condition."""
    def __init__(self):
        self.scores = [0, 0]
        self.score_font = pygame.font.Font(settings.FONT_NAME, settings.SCORE_FONT_SIZE)
        self.message_font = pygame.font.Font(settings.FONT_NAME, settings.MESSAGE_FONT_SIZE)
        self.small_font = pygame.font.Font(settings.FONT_NAME, settings.SMALL_FONT_SIZE)
    def reset(self):
        """Set both scores back to zero for a fresh match."""
        self.scores = [0, 0]
    def score_point(self, player_index):
        """Add one point to `player_index` (0 = left player, 1 = right player)."""
        self.scores[player_index] += 1
    def get_winner(self):
        """Return the index of the winning player, or None if nobody won yet."""
        for index, score in enumerate(self.scores):
            if score >= settings.WINNING_SCORE:
                return index
        return None
    def draw(self, screen):
        """Render both scores near the top of the screen."""
        left_text = self.score_font.render(str(self.scores[0]), True, settings.FOREGROUND_COLOR)
        right_text = self.score_font.render(str(self.scores[1]), True, settings.FOREGROUND_COLOR)
        centre_y = 20
        screen.blit(left_text, (settings.SCREEN_WIDTH // 4 - left_text.get_width() // 2, centre_y))
        screen.blit(right_text, (3 * settings.SCREEN_WIDTH // 4 - right_text.get_width() // 2, centre_y))
    def draw_centered_message(self, screen, message, y, color=settings.FOREGROUND_COLOR, font=None):
        """
        Render `message` horizontally centred on the screen at height `y`.
        `font` defaults to the message font and `color` defaults to the
        foreground colour. Used for the serve countdown, the target-score
        hint and the game-over screen.
        """
        font = font or self.message_font
        text = font.render(message, True, color)
        screen.blit(text, (settings.SCREEN_WIDTH // 2 - text.get_width() // 2, y))