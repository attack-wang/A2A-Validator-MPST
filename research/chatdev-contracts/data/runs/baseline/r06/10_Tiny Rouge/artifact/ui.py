'''
ui.py
Rendering: draws the 80x80 map, entities, and the side UI panel (HP, monster stats, log).
'''
import pygame
import config
class UI:
    """Responsible for all drawing: map tiles, entities, and the info panel."""
    def __init__(self):
        pygame.font.init()
        self.font_large = pygame.font.SysFont("consolas", 26, bold=True)
        self.font_medium = pygame.font.SysFont("consolas", 18, bold=True)
        self.font_small = pygame.font.SysFont("consolas", 15)
        self.map_offset = (0, 0)
    def draw(self, screen, game):
        screen.fill(config.COLOR_BACKGROUND)
        self._draw_map(screen, game)
        self._draw_panel(screen, game)
        if game.game_over:
            self._draw_game_over(screen)
    def _draw_map(self, screen, game):
        ts = config.TILE_SIZE
        grid = game.map_data.grid
        for y in range(config.GRID_SIZE):
            row = grid[y]
            for x in range(config.GRID_SIZE):
                tile = row[x]
                if tile == config.WALL:
                    color = config.COLOR_WALL
                elif tile == config.DOOR:
                    color = config.COLOR_DOOR
                else:
                    color = config.COLOR_FLOOR
                rect = pygame.Rect(x * ts, y * ts, ts, ts)
                screen.fill(color, rect)
        # chests
        for (x, y) in game.map_data.chests:
            rect = pygame.Rect(x * ts + 1, y * ts + 1, ts - 2, ts - 2)
            screen.fill(config.COLOR_CHEST, rect)
        # monsters
        for monster in game.map_data.monsters.values():
            rect = pygame.Rect(monster.x * ts + 1, monster.y * ts + 1, ts - 2, ts - 2)
            screen.fill(monster.color, rect)
        # player
        p = game.player
        rect = pygame.Rect(p.x * ts, p.y * ts, ts, ts)
        screen.fill(config.COLOR_PLAYER, rect)