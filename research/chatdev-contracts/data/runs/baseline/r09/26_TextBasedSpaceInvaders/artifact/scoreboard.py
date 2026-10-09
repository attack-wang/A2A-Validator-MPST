'''
scoreboard.py
HUD renderer: shows the current score, high score, level and the
remaining lives as small ship icons, plus overlay messages for the
start, game-over and victory screens.
'''
import pygame
import settings
class Scoreboard:
    def __init__(self, settings, screen, stats):
        self.settings = settings
        self.screen = screen
        self.stats = stats
        self.font = pygame.font.Font(None, settings.FONT_SIZE)
        self.big_font = pygame.font.Font(None, settings.FONT_SIZE_BIG)
        self.small_font = pygame.font.Font(None, settings.FONT_SIZE_SMALL)
    def draw(self, ship_image):
        """Render score, high score and remaining lives onto the HUD."""
        score_img = self.font.render(f"Score: {self.stats.score}", True, settings.COLOR_TEXT)
        self.screen.blit(score_img, (20, 15))
        high_img = self.font.render(f"High Score: {self.stats.high_score}", True, settings.COLOR_ACCENT)
        high_rect = high_img.get_rect()
        high_rect.centerx = self.settings.SCREEN_WIDTH // 2
        high_rect.top = 15
        self.screen.blit(high_img, high_rect)
        # Lives as small ship icons at the right side.
        label = self.small_font.render("Lives:", True, settings.COLOR_TEXT)
        self.screen.blit(label, (self.settings.SCREEN_WIDTH - 190, 18))
        icon = pygame.transform.smoothscale(
            ship_image, (ship_image.get_width() // 2, ship_image.get_height() // 2))
        x = self.settings.SCREEN_WIDTH - 120
        for _ in range(max(0, self.stats.lives_left)):
            self.screen.blit(icon, (x, 15))
            x += icon.get_width() + 8
    def draw_message(self, title, subtitle):
        """Draw a centered overlay with a big title and a subtitle."""
        overlay = pygame.Surface((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        title_img = self.big_font.render(title, True, settings.COLOR_ACCENT)
        title_rect = title_img.get_rect(
            center=(self.settings.SCREEN_WIDTH // 2, self.settings.SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(title_img, title_rect)
        sub_img = self.font.render(subtitle, True, settings.COLOR_TEXT)
        sub_rect = sub_img.get_rect(
            center=(self.settings.SCREEN_WIDTH // 2, self.settings.SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(sub_img, sub_rect)