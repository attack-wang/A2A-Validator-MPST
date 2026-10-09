'''
scoreboard.py
Renders score, high score, lives, and end-game messages.
'''
import pygame
import settings
class Scoreboard:
    """Display game information on screen."""
    def __init__(self, screen, stats):
        self.screen = screen
        self.stats = stats
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 64)
        self.small_font = pygame.font.SysFont(None, 24)
    def show_score(self):
        """Draw score, high score, wave, and remaining lives."""
        score_str = "Score: {:,}".format(self.stats.score)
        self.score_img = self.font.render(score_str, True, settings.WHITE)
        self.screen.blit(self.score_img, (20, 10))
        high_str = "High Score: {:,}".format(self.stats.high_score)
        high_img = self.font.render(high_str, True, settings.WHITE)
        high_rect = high_img.get_rect()
        high_rect.centerx = self.screen.get_rect().centerx
        high_rect.top = 10
        self.screen.blit(high_img, high_rect)
        wave_str = "Wave: {}".format(self.stats.wave)
        wave_img = self.font.render(wave_str, True, settings.WHITE)
        wave_rect = wave_img.get_rect()
        wave_rect.right = self.screen.get_rect().right - 20
        wave_rect.top = 10
        self.screen.blit(wave_img, wave_rect)
        # Lives as small ship icons
        self._draw_lives()
    def _draw_lives(self):
        """Draw the remaining lives as small ship icons at bottom-left."""
        icon_w, icon_h = 24, 16
        for i in range(self.stats.lives):
            x = 20 + i * (icon_w + 8)
            y = self.screen.get_rect().bottom - icon_h - 10
            points = [
                (x + icon_w // 2, y),
                (x + icon_w, y + icon_h),
                (x, y + icon_h),
            ]
            pygame.draw.polygon(self.screen, (60, 200, 255), points)
    def draw_center_message(self, text, sub_text=None):
        """Draw a large centered message with optional sub-text."""
        screen_rect = self.screen.get_rect()
        msg_img = self.big_font.render(text, True, settings.WHITE)
        msg_rect = msg_img.get_rect()
        msg_rect.center = screen_rect.center
        self.screen.blit(msg_img, msg_rect)
        if sub_text:
            sub_img = self.small_font.render(sub_text, True, settings.WHITE)
            sub_rect = sub_img.get_rect()
            sub_rect.midtop = (msg_rect.centerx, msg_rect.bottom + 20)
            self.screen.blit(sub_img, sub_rect)