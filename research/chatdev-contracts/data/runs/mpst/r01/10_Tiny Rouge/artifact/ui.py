'''
ui.py
Rendering layer for the Tower of the Sorcerer roguelike.
Draws the 80x80 tile map (cached to a surface per floor for speed),
the player, monsters and treasure chests, plus the minimal side-panel
UI: current HP with a bar, tower floor number, stats of encountered
(nearby) monsters and a scrolling message log.  Also renders the
game-over overlay.
'''
import pygame
from settings import (
    TILE_SIZE, MAP_PIXEL_WIDTH, PANEL_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT,
    TILE_WALL, TILE_FLOOR, TILE_DOOR,
    COLOR_BACKGROUND, COLOR_WALL, COLOR_WALL_EDGE, COLOR_FLOOR,
    COLOR_FLOOR_ALT, COLOR_DOOR, COLOR_DOOR_EDGE,
    COLOR_PLAYER, COLOR_PLAYER_EDGE, COLOR_MONSTER, COLOR_MONSTER_EDGE,
    COLOR_CHEST, COLOR_CHEST_EDGE, COLOR_PANEL, COLOR_PANEL_EDGE,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_HP_FULL, COLOR_HP_LOW, COLOR_OVERLAY,
    PLAYER_START_HP,
)
class UI:
    """All pygame drawing.  Reads state from the Game object each frame."""
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font_title = pygame.font.Font(None, 30)
        self.font_large = pygame.font.Font(None, 26)
        self.font_medium = pygame.font.Font(None, 22)
        self.font_small = pygame.font.Font(None, 16)
        self._cached_level = None
        self._map_surface = None
    # ------------------------------------------------------------------
    # Frame entry point
    # ------------------------------------------------------------------
    def draw(self, game):
        self.screen.fill(COLOR_BACKGROUND)
        self.draw_map(game)
        self.draw_panel(game)
        if game.game_over:
            self.draw_game_over()
    # ------------------------------------------------------------------
    # Map rendering (static tiles cached per floor)
    # ------------------------------------------------------------------
    def draw_map(self, game):
        level = game.level
        if self._cached_level is not level:
            self._cached_level = level
            self._map_surface = self._render_static_map(level)
        self.screen.blit(self._map_surface, (0, 0))
        # Treasure chests
        for (x, y) in level.chests:
            rect = pygame.Rect(x * TILE_SIZE + 1, y * TILE_SIZE + 1,
                               TILE_SIZE - 2, TILE_SIZE - 2)
            pygame.draw.rect(self.screen, COLOR_CHEST, rect)
            pygame.draw.rect(self.screen, COLOR_CHEST_EDGE, rect, 1)
        # Monsters
        for (x, y) in level.monsters:
            rect = pygame.Rect(x * TILE_SIZE + 1, y * TILE_SIZE + 1,
                               TILE_SIZE - 2, TILE_SIZE - 2)
            pygame.draw.rect(self.screen, COLOR_MONSTER, rect)
            pygame.draw.rect(self.screen, COLOR_MONSTER_EDGE, rect, 1)
        # Player (drawn last so it is always visible)
        player = game.player
        rect = pygame.Rect(player.x * TILE_SIZE + 1, player.y * TILE_SIZE + 1,
                           TILE_SIZE - 2, TILE_SIZE - 2)
        pygame.draw.rect(self.screen, COLOR_PLAYER, rect)
        pygame.draw.rect(self.screen, COLOR_PLAYER_EDGE, rect, 1)
    def _render_static_map(self, level):
        surface = pygame.Surface((MAP_PIXEL_WIDTH, MAP_PIXEL_HEIGHT))
        surface.fill(COLOR_BACKGROUND)
        for y in range(len(level.grid)):
            row = level.grid[y]
            for x in range(len(row)):
                tile = row[x]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE,
                                   TILE_SIZE, TILE_SIZE)
                if tile == TILE_WALL:
                    pygame.draw.rect(surface, COLOR_WALL, rect)
                    pygame.draw.rect(surface, COLOR_WALL_EDGE, rect, 1)
                elif tile == TILE_DOOR:
                    pygame.draw.rect(surface, COLOR_FLOOR, rect)
                    inner = rect.inflate(-4, -4)
                    pygame.draw.rect(surface, COLOR_DOOR, inner)
                    pygame.draw.rect(surface, COLOR_DOOR_EDGE, inner, 1)
                else:  # TILE_FLOOR
                    color = COLOR_FLOOR if (x + y) % 2 == 0 else COLOR_FLOOR_ALT
                    pygame.draw.rect(surface, color, rect)
        return surface