'''
ui.py
Minimal side-panel UI: HP bar, floor number, adjacent monster stats,
message log and overlay screens (game over).
'''
import pygame
import config
class UIPanel:
    def __init__(self):
        self.font_big = pygame.font.Font(None, 34)
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        self.panel_rect = pygame.Rect(config.MAP_PIXEL_SIZE, 0,
                                      config.UI_PANEL_WIDTH, config.WINDOW_HEIGHT)
    def render(self, window, game):
        pygame.draw.rect(window, config.COLOR_PANEL_BG, self.panel_rect)
        pygame.draw.rect(window, config.COLOR_PANEL_BORDER, self.panel_rect, 2)
        self._draw_title(window)
        self._draw_hp_bar(window, game)
        self._draw_floor(window, game)
        self._draw_monster_stats(window, game)
        self._draw_log(window, game)
        if game.game_over:
            self._draw_game_over(window)
    # helpers below...