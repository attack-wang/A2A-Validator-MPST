import pygame
from settings import Settings
from utils import bitmap_to_surface
from ship import SHIP_BITMAP
class Scoreboard:
    """HUD showing score and remaining lives."""
    def __init__(self):
        self.font = pygame.font.Font(None, 30)
        self.icon = bitmap_to_surface(SHIP_BITMAP, Settings.SHIP_COLOR, 1)
    def draw(self, screen, score, lives):
        score_img = self.font.render(f"SCORE: {score}", True, Settings.TEXT_COLOR)
        screen.blit(score_img, (20, 12))
        label = self.font.render("LIVES:", True, Settings.HUD_COLOR)
        icon_w = self.icon.get_width()
        spacing = 6
        total_icons = lives * (icon_w + spacing)
        start_x = Settings.SCREEN_WIDTH - 20 - total_icons
        screen.blit(label, (start_x - label.get_width() - 10, 12))
        for i in range(lives):
            screen.blit(self.icon, (start_x + i * (icon_w + spacing), 14))