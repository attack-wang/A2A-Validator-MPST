import pygame
from constants import ...
class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.fonts = {...}
    def draw(self, game):
        self.screen.fill(BACKGROUND_COLOR)
        self._draw_header(game)
        self._draw_grid(game)
        if game.game_over:
            self._draw_game_over(game)
        pygame.display.flip()