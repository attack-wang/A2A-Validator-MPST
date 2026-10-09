'''
Renderer module for the 2048 game.
Defines the Renderer class, which initializes the Pygame window and draws
the 4x4 grid, numbered tiles, the score panel (current score and highest
tile reached), and the game-over overlay. This module fully implements the
presentation layer referenced by main.py.
'''
import pygame
# ---- Layout constants ----
MARGIN = 20
CELL_SIZE = 100
CELL_GAP = 10
BOX_WIDTH = 120
BOX_HEIGHT = 60
PANEL_HEIGHT = 80   # vertical space reserved for title + score boxes
# ---- Colors (R, G, B) ----
BACKGROUND_COLOR = (250, 248, 239)
GRID_BACKGROUND_COLOR = (187, 173, 160)
EMPTY_CELL_COLOR = (205, 193, 180)
TEXT_COLOR = (119, 110, 101)
TILE_TEXT_DARK = (119, 110, 101)
TILE_TEXT_LIGHT = (249, 246, 242)
TILE_COLORS = {
    2: (238, 228, 218), 4: (237, 194, 174), 8: (242, 177, 121),
    16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59),
    128: (237, 207, 114), 256: (237, 204, 97), 512: (237, 200, 80),
    1024: (237, 197, 63), 2048: (237, 194, 46),
}
FALLBACK_TILE_COLOR = (60, 58, 56)  # for values beyond 2048
class Renderer:
    '''Renders the 2048 window: grid, tiles, score panel, and overlays.'''
    def __init__(self, size=4):
        '''Initialize Pygame, create the window, fonts, and cell geometry.'''
        self.size = size
        self.MARGIN = MARGIN
        self.BOX_WIDTH = BOX_WIDTH
        self.BOX_HEIGHT = BOX_HEIGHT
        self.width = MARGIN * 2 + size * CELL_SIZE + (size - 1) * CELL_GAP
        self.height = self.width + PANEL_HEIGHT
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('2048')
        self.font_title = pygame.font.Font(None, 48)
        self.font_label = pygame.font.Font(None, 22)
        self.font_value = pygame.font.Font(None, 32)
        self.font_tile = pygame.font.Font(None, 40)
        self.font_tile_small = pygame.font.Font(None, 30)
        self.font_overlay = pygame.font.Font(None, 40)
        # Pre-compute the top-left pixel of every grid cell
        self.cell_positions = {
            (r, c): (MARGIN + c * (CELL_SIZE + CELL_GAP),
                     PANEL_HEIGHT + MARGIN + r * (CELL_SIZE + CELL_GAP))
            for r in range(size) for c in range(size)
        }
    def draw(self, game):
        '''Render one full frame: panel, grid, tiles, and game-over overlay.'''
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_score_panel(game)
        self._draw_grid_background()
        self._draw_tiles(game)
        if game.game_over:
            self._draw_game_over()
        pygame.display.flip()
    def draw_score_panel(self, game):
        '''Show the game title, current score, and highest tile reached.'''
        title = self.font_title.render('2048', True, TEXT_COLOR)
        self.screen.blit(title, (self.MARGIN, self.MARGIN - 4))
        self._draw_stat_box('SCORE', str(game.score),
                            right=self.width - self.MARGIN, top=self.MARGIN)
        self._draw_stat_box('HIGHEST TILE', str(game.highest_tile),
                            right=self.width - self.MARGIN - 130, top=self.MARGIN)
    def _draw_stat_box(self, label, value, right, top):
        '''Draw one labelled statistic box (SCORE / HIGHEST TILE).'''
        rect = pygame.Rect(right - self.BOX_WIDTH, top,
                           self.BOX_WIDTH, self.BOX_HEIGHT)
        pygame.draw.rect(self.screen, EMPTY_CELL_COLOR, rect, border_radius=6)
        label_surf = self.font_label.render(label, True, TEXT_COLOR)
        self.screen.blit(label_surf,
                         label_surf.get_rect(midtop=(rect.centerx, rect.top + 8)))
        value_surf = self.font_value.render(value, True, TEXT_COLOR)
        self.screen.blit(value_surf,
                         value_surf.get_rect(midtop=(rect.centerx, rect.top + 32)))
    def _draw_grid_background(self):
        '''Draw the grid container and the empty cell slots beneath the tiles.'''
        grid_dim = self.size * CELL_SIZE + (self.size - 1) * CELL_GAP
        grid_rect = pygame.Rect(self.MARGIN, PANEL_HEIGHT + self.MARGIN,
                                grid_dim, grid_dim)
        pygame.draw.rect(self.screen, GRID_BACKGROUND_COLOR, grid_rect,
                         border_radius=8)
        for x, y in self.cell_positions.values():
            cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, EMPTY_CELL_COLOR, cell_rect,
                             border_radius=6)
    def _draw_tiles(self, game):
        '''Draw every non-zero tile with a color and font sized to its value.'''
        for r in range(game.size):
            for c in range(game.size):
                value = game.grid[r][c]
                if value == 0:
                    continue
                x, y = self.cell_positions[(r, c)]
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen,
                                 TILE_COLORS.get(value, FALLBACK_TILE_COLOR),
                                 rect, border_radius=6)
                font = self.font_tile if value < 1024 else self.font_tile_small
                text_color = TILE_TEXT_DARK if value <= 4 else TILE_TEXT_LIGHT
                surf = font.render(str(value), True, text_color)
                self.screen.blit(surf, surf.get_rect(center=rect.center))
    def _draw_game_over(self):
        '''Overlay a translucent banner announcing the game has ended.'''
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((250, 248, 239, 160))
        self.screen.blit(overlay, (0, 0))
        text = self.font_overlay.render('Game Over!  Press R to restart',
                                        True, TEXT_COLOR)
        self.screen.blit(text, text.get_rect(center=(self.width // 2,
                                                     self.height // 2)))