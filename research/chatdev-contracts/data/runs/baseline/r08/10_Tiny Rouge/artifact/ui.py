'''Rendering: draws the grid, entities and the minimal side-panel UI.'''
import pygame
import settings
class UI:
    '''Responsible for all drawing: map, entities, HUD panel and overlays.'''
    def __init__(self, screen):
        self.screen = screen
        self.font_small = self._load_font(settings.FONT_SIZE_SMALL)
        self.font_medium = self._load_font(settings.FONT_SIZE_MEDIUM)
        self.font_large = self._load_font(settings.FONT_SIZE_LARGE)
    @staticmethod
    def _load_font(size):
        '''Load the configured font with a safe fallback to pygame's default.'''
        try:
            return pygame.font.SysFont(settings.FONT_NAME, size)
        except Exception:
            return pygame.font.Font(None, size)
    def draw(self, game):
        '''Draw one full frame: background, map, entities, panel, overlays.'''
        self.screen.fill(settings.COLOR_BACKGROUND)
        self._draw_map(game)
        self._draw_entities(game)
        self._draw_panel(game)
        if game.state != "playing":
            self._draw_overlay(game)
    def _draw_map(self, game):
        '''Draw wall/floor/door tiles of the current level.'''
        ts = settings.TILE_SIZE
        for y in range(settings.GRID_SIZE):
            for x in range(settings.GRID_SIZE):
                tile = game.grid[y][x]
                if tile == settings.WALL:
                    color = settings.COLOR_WALL
                elif tile == settings.DOOR:
                    color = settings.COLOR_DOOR
                else:
                    color = settings.COLOR_FLOOR
                pygame.draw.rect(self.screen, color,
                                 (x * ts, y * ts, ts, ts))
    def _draw_entities(self, game):
        '''Draw chests, monsters and the player on top of the tiles.'''
        ts = settings.TILE_SIZE
        for (x, y) in game.chests:
            pygame.draw.rect(self.screen, settings.COLOR_CHEST,
                             (x * ts + 1, y * ts + 1, ts - 2, ts - 2))
        for (x, y), monster in game.monsters.items():
            pygame.draw.rect(self.screen, monster.color,
                             (x * ts + 1, y * ts + 1, ts - 2, ts - 2))
        px, py = game.player.pos
        pygame.draw.rect(self.screen, settings.COLOR_PLAYER,
                         (px * ts + 1, py * ts + 1, ts - 2, ts - 2))
    def _draw_panel(self, game):
        '''Draw the minimal UI: HP bar, floor number and monster stats.'''
        ts = settings.GRID_SIZE * settings.TILE_SIZE
        pygame.draw.rect(self.screen, settings.COLOR_PANEL_BG,
                         (ts, 0, settings.PANEL_WIDTH, settings.WINDOW_HEIGHT))
        ox = ts + 12
        title = self.font_large.render("TOWER", True, settings.COLOR_TITLE)
        self.screen.blit(title, (ox, 10))
        floor_txt = self.font_medium.render(
            f"Floor {game.level}/{settings.MAX_LEVELS}",
            True, settings.COLOR_PANEL_TEXT)
        self.screen.blit(floor_txt, (ox, 48))
        hp_txt = self.font_medium.render(
            f"HP: {game.player.hp}", True, settings.COLOR_PANEL_TEXT)
        self.screen.blit(hp_txt, (ox, 78))
        # HP bar (clamped so overhealing never overflows the bar)
        bar_width = settings.PANEL_WIDTH - 24
        pygame.draw.rect(self.screen, settings.COLOR_HP_BAR_BG,
                         (ox, 104, bar_width, 14))
        ratio = max(0.0, min(1.0, game.player.hp / settings.PLAYER_START_HP))
        pygame.draw.rect(self.screen, settings.COLOR_HP_BAR_FILL,
                         (ox, 104, int(bar_width * ratio), 14))
        # Last encountered monster stats
        label = self.font_medium.render("Last monster:",
                                        True, settings.COLOR_PANEL_TEXT)
        self.screen.blit(label, (ox, 134))
        y = 158
        if game.last_monster:
            m = game.last_monster
            lines = [m.name, f"HP {m.hp}", f"ATK {m.atk}"]
        else:
            lines = ["(none yet)"]
        for line in lines:
            surf = self.font_small.render(line, True, settings.COLOR_PANEL_TEXT)
            self.screen.blit(surf, (ox, y))
            y += 18
        # Message log (most recent messages last)
        y += 10
        for msg in game.messages[-6:]:
            surf = self.font_small.render(msg, True, settings.COLOR_MESSAGE)
            self.screen.blit(surf, (ox, y))
            y += 18
    def _draw_overlay(self, game):
        '''Dim the screen and show the death / victory banner.'''
        overlay = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT),
                                 pygame.SRCALPHA)
        overlay.fill((*settings.COLOR_OVERLAY, 160))
        self.screen.blit(overlay, (0, 0))
        text = "YOU DIED" if game.state == "dead" else "VICTORY!"
        big = self.font_large.render(text, True, settings.COLOR_TITLE)
        small = self.font_medium.render("Press R to restart",
                                        True, settings.COLOR_PANEL_TEXT)
        center = (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)
        self.screen.blit(big, big.get_rect(center=(center[0], center[1] - 20)))
        self.screen.blit(small, small.get_rect(center=(center[0], center[1] + 20)))