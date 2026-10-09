'''
ui.py
Rendering: map view, side panel (HP / monster stats / messages) and overlays.
'''
import pygame
import settings
class UI:
    """Draws the game world and the minimal side-panel UI."""
    def __init__(self):
        if not pygame.font.get_init():
            pygame.font.init()
        self.font_title = pygame.font.Font(None, 30)
        self.font_big = pygame.font.Font(None, 26)
        self.font_small = pygame.font.Font(None, 20)
        self.font_glyph = pygame.font.Font(None, 18)
    # --- public API -------------------------------------------------------
    def draw_game(self, surface, level, player, nearby_monsters, messages, game_over):
        """Render one full frame: map, panel and (optionally) the game-over overlay."""
        self._draw_map(surface, level, player)
        self._draw_panel(surface, player, level, nearby_monsters, messages)
        if game_over:
            self._draw_game_over(surface)
    def _draw_map(self, surface, level, player):
        """Draw every tile of the 80x80 grid plus entities and the player."""
        area = pygame.Rect(0, 0, settings.MAP_PIXEL_WIDTH, settings.MAP_PIXEL_HEIGHT)
        pygame.draw.rect(surface, settings.COLOR_BACKGROUND, area)
        for y in range(settings.GRID_HEIGHT):
            for x in range(settings.GRID_WIDTH):
                rect = pygame.Rect(x * settings.TILE_SIZE, y * settings.TILE_SIZE,
                                   settings.TILE_SIZE, settings.TILE_SIZE)
                if level.is_door(x, y):
                    color = settings.COLOR_DOOR
                elif level.is_wall(x, y):
                    color = settings.COLOR_WALL
                else:
                    color = settings.COLOR_FLOOR if (x + y) % 2 == 0 else settings.COLOR_FLOOR_ALT
                pygame.draw.rect(surface, color, rect)
        # chests
        for chest in level.chests:
            rect = pygame.Rect(chest.x * settings.TILE_SIZE, chest.y * settings.TILE_SIZE,
                               settings.TILE_SIZE, settings.TILE_SIZE)
            pygame.draw.rect(surface, settings.COLOR_CHEST, rect)
        # monsters
        for monster in level.monsters:
            rect = pygame.Rect(monster.x * settings.TILE_SIZE, monster.y * settings.TILE_SIZE,
                               settings.TILE_SIZE, settings.TILE_SIZE)
            pygame.draw.rect(surface, monster.color, rect)
        # player
        rect = pygame.Rect(player.x * settings.TILE_SIZE, player.y * settings.TILE_SIZE,
                           settings.TILE_SIZE, settings.TILE_SIZE)
        pygame.draw.rect(surface, settings.COLOR_PLAYER, rect)