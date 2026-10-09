'''
ui.py
Heads-up display: score, high score, lives (as ship icons), and centered
messages for pause / game over / victory states.
'''
import pygame
class HUD:
    """Draws score, high score, remaining lives, and center messages."""
    def __init__(self, settings):
        self.settings = settings
        self.font = pygame.font.SysFont(None, settings.font_size)
        self.big_font = pygame.font.SysFont(None, settings.big_font_size)
    def draw(self, screen, score, high_score, lives):
        """Render the top HUD bar: score, high score, and life icons."""
        score_text = self.font.render(f"Score: {score}", True, self.settings.hud_color)
        screen.blit(score_text, (10, 10))
        hs_text = self.font.render(f"High Score: {high_score}", True, self.settings.hud_color)
        screen.blit(hs_text, (self.settings.screen_width // 2 - hs_text.get_width() // 2, 10))
        # lives as small ship icons on the right
        icon_w, icon_h = 24, 14
        for i in range(lives):
            x = self.settings.screen_width - 10 - (i + 1) * (icon_w + 8)
            y = 12
            points = [
                (x + icon_w // 2, y),
                (x + icon_w, y + icon_h),
                (x, y + icon_h),
            ]
            pygame.draw.polygon(screen, (0, 200, 255), points)
    def draw_center_message(self, screen, title, subtitle):
        """Draw a large centered title with a smaller subtitle beneath it."""
        title_surf = self.big_font.render(title, True, self.settings.hud_color)
        sub_surf = self.font.render(subtitle, True, self.settings.hud_color)
        cx = self.settings.screen_width // 2
        cy = self.settings.screen_height // 2
        screen.blit(title_surf, (cx - title_surf.get_width() // 2, cy - 60))
        screen.blit(sub_surf, (cx - sub_surf.get_width() // 2, cy + 10))