'''
renderer.py
Draws the 80x80 grid world, entities and delegates the side panel to the UI.
'''
import pygame
import config
from ui import UIPanel
class Renderer:
    def __init__(self, window):
        self.window = window
        self.ui = UIPanel()
        self.map_surface = pygame.Surface((config.MAP_PIXEL_SIZE, config.MAP_PIXEL_SIZE))
        self._cached_grid = None
    def render(self, game):
        self.window.fill(config.COLOR_BACKGROUND)
        self._draw_map(game)
        self._draw_entities(game)
        self._draw_player(game)
        self.ui.render(self.window, game)
        pygame.display.flip()
    # ------------------------------------------------------------------ #
    # Map
    # ------------------------------------------------------------------ #
    def _draw_map(self, game):
        if self._cached_grid is not game.grid:
            self._rebuild_map_surface(game.grid)
            self._cached_grid = game.grid
        self.window.blit(self.map_surface, (0, 0))
    def _rebuild_map_surface(self, grid):
        for y in range(config.GRID_SIZE):
            for x in range(config.GRID_SIZE):
                color = (config.COLOR_FLOOR if grid[y][x] == config.TILE_FLOOR
                         else config.COLOR_WALL)
                rect = pygame.Rect(x * config.TILE_SIZE, y * config.TILE_SIZE,
                                   config.TILE_SIZE, config.TILE_SIZE)
                pygame.draw.rect(self.map_surface, color, rect)
        # subtle checkerboard on floors for readability
        for y in range(config.GRID_SIZE):
            for x in range(config.GRID_SIZE):
                if grid[y][x] == config.TILE_FLOOR and (x + y) % 2 == 0:
                    rect = pygame.Rect(x * config.TILE_SIZE, y * config.TILE_SIZE,
                                       config.TILE_SIZE, config.TILE_SIZE)
                    pygame.draw.rect(self.map_surface, config.COLOR_FLOOR_ALT, rect)
    # ------------------------------------------------------------------ #
    # Entities
    # ------------------------------------------------------------------ #
    def _entity_rect(self, x, y):
        return pygame.Rect(x * config.TILE_SIZE, y * config.TILE_SIZE,
                           config.TILE_SIZE, config.TILE_SIZE)
    def _draw_entities(self, game):
        for door in [game.door]:
            pygame.draw.rect(self.window, config.COLOR_DOOR,
                             self._entity_rect(door.x, door.y))
        for chest in game.chests.values():
            rect = self._entity_rect(chest.x, chest.y)
            pygame.draw.rect(self.window, config.COLOR_CHEST, rect)
            pygame.draw.rect(self.window, config.COLOR_TEXT_DIM, rect, 1)
        for monster in game.monsters.values():
            rect = self._entity_rect(monster.x, monster.y)
            pygame.draw.rect(self.window, monster.color, rect)
            pygame.draw.rect(self.window, config.COLOR_TEXT_DIM, rect, 1)
    def _draw_player(self, game):
        rect = self._entity_rect(game.player.x, game.player.y)
        pygame.draw.rect(self.window, config.COLOR_PLAYER, rect)
        pygame.draw.rect(self.window, config.COLOR_TEXT, rect, 1)