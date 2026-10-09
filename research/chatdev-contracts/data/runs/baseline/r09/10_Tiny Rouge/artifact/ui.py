'''
ui.py
Rendering: grid viewport and sidebar UI (HP, level, monster stats, log).
'''
import pygame
from settings import (
    GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, SIDEBAR_WIDTH, SCREEN_HEIGHT,
    WALL, FLOOR, DOOR,
    COLOR_BG, COLOR_WALL, COLOR_FLOOR, COLOR_DOOR,
    COLOR_CHEST, COLOR_MONSTER, COLOR_PLAYER,
    COLOR_SIDEBAR, COLOR_TEXT, COLOR_TEXT_DIM,
    COLOR_HP_BG, COLOR_HP_FILL, COLOR_TITLE,
    COLOR_PANEL, COLOR_PANEL_EDGE,
    COLOR_MSG_DANGER, COLOR_MSG_GOOD, COLOR_MSG_INFO,
    COLOR_OVERLAY,
    PLAYER_START_HP, LOG_LINES,
)
MSG_COLORS = {"danger": COLOR_MSG_DANGER, "good": COLOR_MSG_GOOD, "info": COLOR_MSG_INFO}
class Renderer:
    '''Draws the whole frame: map viewport, sidebar and end-of-run overlay.'''
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 20)
        self.font_small = pygame.font.SysFont(None, 16)
        self.font_big = pygame.font.SysFont(None, 36, bold=True)
        self._base = None       # cached static tile surface
        self._base_key = None   # floor_version the cache was built for
    # ------------------------------------------------------------------ public
    def draw(self, game):
        self._draw_map(game)
        self._draw_sidebar(game)
        if game.game_over:
            self._draw_overlay(game)
    # --------------------------------------------------------------------- map
    def _floor_surface(self, game):
        '''Build (or reuse) the static tile layer for the current floor.'''
        if self._base is not None and self._base_key == game.floor_version:
            return self._base
        surface = pygame.Surface((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE))
        surface.fill(COLOR_BG)
        for y in range(GRID_HEIGHT):
            row = game.grid[y]
            for x in range(GRID_WIDTH):
                tile = row[x]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == WALL:
                    surface.fill(COLOR_WALL, rect)
                elif tile == DOOR:
                    surface.fill(COLOR_DOOR, rect)
                elif tile == FLOOR:
                    surface.fill(COLOR_FLOOR, rect)
        self._base = surface
        self._base_key = game.floor_version
        return surface
    def _draw_map(self, game):
        self.screen.blit(self._floor_surface(game), (0, 0))
        for x, y in game.chests:
            self._blit_entity(COLOR_CHEST, x, y)
        for x, y in game.monsters:
            self._blit_entity(COLOR_MONSTER, x, y)
        self._blit_entity(COLOR_PLAYER, game.player.x, game.player.y)
    def _blit_entity(self, color, x, y):
        rect = pygame.Rect(x * TILE_SIZE + 1, y * TILE_SIZE + 1, TILE_SIZE - 2, TILE_SIZE - 2)
        pygame.draw.rect(self.screen, color, rect)
    # ----------------------------------------------------------------- sidebar
    def _draw_sidebar(self, game):
        left = GRID_WIDTH * TILE_SIZE
        pygame.draw.rect(self.screen, COLOR_SIDEBAR,
                         (left, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
        x = left + 16
        y = 14
        title = self.font_big.render("TOWER", True, COLOR_TITLE)
        self.screen.blit(title, (x, y))
        y += title.get_height() + 2
        sub = self.font_small.render("of the Sorcerer", True, COLOR_TEXT_DIM)
        self.screen.blit(sub, (x, y))
        y += sub.get_height() + 16
        floor_label = self.font.render(f"Floor: {game.level}", True, COLOR_TEXT)
        self.screen.blit(floor_label, (x, y))
        y += floor_label.get_height() + 10
        y = self._draw_hp_bar(game, x, y) + 14
        y = self._draw_monster_panel(game, x, y) + 14
        self._draw_log(game, x, y, SCREEN_HEIGHT - 14)
    def _draw_hp_bar(self, game, x, y):
        label = self.font.render("HP", True, COLOR_TEXT)
        self.screen.blit(label, (x, y))
        y += label.get_height() + 4
        bar_w = SIDEBAR_WIDTH - 32
        bar_h = 18
        bar = pygame.Rect(x, y, bar_w, bar_h)
        pygame.draw.rect(self.screen, COLOR_HP_BG, bar)
        ratio = max(0.0, min(1.0, game.player.hp / PLAYER_START_HP))
        if ratio > 0.0:
            pygame.draw.rect(self.screen, COLOR_HP_FILL,
                             (x, y, max(1, int(bar_w * ratio)), bar_h))
        pygame.draw.rect(self.screen, COLOR_PANEL_EDGE, bar, 1)
        text = self.font.render(f"{game.player.hp} / {PLAYER_START_HP}", True, COLOR_TEXT)
        self.screen.blit(text, (x + bar_w - text.get_width() - 6, y + 2))
        return y + bar_h
    def _draw_monster_panel(self, game, x, y):
        panel_w = SIDEBAR_WIDTH - 32
        panel_h = 104
        pygame.draw.rect(self.screen, COLOR_PANEL, (x, y, panel_w, panel_h))
        pygame.draw.rect(self.screen, COLOR_PANEL_EDGE, (x, y, panel_w, panel_h), 1)
        ty = y + 8
        head = self.font.render("Monsters", True, COLOR_TEXT_DIM)
        self.screen.blit(head, (x + 10, ty))
        ty += head.get_height() + 6
        rows = []
        if game.nearby_monster is not None:
            rows.append(("Adjacent", game.nearby_monster, COLOR_MSG_INFO))
        if game.last_monster is not None:
            rows.append(("Defeated", game.last_monster, COLOR_MSG_GOOD))
        if not rows:
            hint = self.font_small.render("None encountered yet.", True, COLOR_TEXT_DIM)
            self.screen.blit(hint, (x + 10, ty))
        else:
            for tag, monster, color in rows:
                line = self.font.render(f"{tag}: {monster.name}", True, color)
                self.screen.blit(line, (x + 10, ty))
                ty += line.get_height() + 2
                stat = self.font_small.render(f"   HP {monster.hp}", True, COLOR_TEXT)
                self.screen.blit(stat, (x + 10, ty))
                ty += stat.get_height() + 4
        return y + panel_h
    def _draw_log(self, game, x, y, bottom):
        head = self.font.render("Log", True, COLOR_TEXT_DIM)
        self.screen.blit(head, (x, y))
        y += head.get_height() + 4
        for text, kind in game.messages[-LOG_LINES:]:
            if y > bottom:
                break
            line = self.font_small.render(text, True, MSG_COLORS.get(kind, COLOR_TEXT))
            self.screen.blit(line, (x, y))
            y += line.get_height() + 2
    # ----------------------------------------------------------------- overlay
    def _draw_overlay(self, game):
        veil = pygame.Surface((GRID_WIDTH * TILE_SIZE, SCREEN_HEIGHT), pygame.SRCALPHA)
        veil.fill((*COLOR_OVERLAY, 200))
        self.screen.blit(veil, (0, 0))
        big = self.font_big.render("YOU DIED", True, COLOR_MSG_DANGER)
        self.screen.blit(big, ((GRID_WIDTH * TILE_SIZE - big.get_width()) // 2,
                               SCREEN_HEIGHT // 2 - 40))
        hint = self.font.render(
            f"You reached floor {game.level}. Press R to restart.", True, COLOR_TEXT)
        self.screen.blit(hint, ((GRID_WIDTH * TILE_SIZE - hint.get_width()) // 2,
                                SCREEN_HEIGHT // 2 + 10))