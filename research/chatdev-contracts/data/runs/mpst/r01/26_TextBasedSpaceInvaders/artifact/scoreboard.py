'''scoreboard.py: on-screen HUD showing score, high score, level and lives.'''
import pygame
class Scoreboard:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 64)
    def show_score(self):
        stats = self.game.stats
        s = self.settings
        score_img = self.font.render(f"Score: {stats.score}", True, (230, 235, 255))
        high_img = self.font.render(f"High: {stats.high_score}", True, (230, 235, 255))
        level_img = self.font.render(f"Level: {stats.level}", True, (230, 235, 255))
        self.screen.blit(score_img, (10, 10))
        high_rect = high_img.get_rect(midtop=(s.screen_width // 2, 10))
        self.screen.blit(high_img, high_rect)
        level_rect = level_img.get_rect(topright=(s.screen_width - 10, 10))
        self.screen.blit(level_img, level_rect)
        self.draw_lives()
    def draw_lives(self):
        stats = self.game.stats
        s = self.settings
        for i in range(stats.lives):
            x = 10 + i * 30
            y = s.screen_height - 30
            self._draw_life_icon(x, y)
    def _draw_life_icon(self, x, y):
        color = self.settings.ship_color
        body = pygame.Rect(x, y, 20, 12)
        pygame.draw.rect(self.screen, color, body, border_radius=4)
        pygame.draw.rect(self.screen, color, (x + 8, y - 6, 4, 6))