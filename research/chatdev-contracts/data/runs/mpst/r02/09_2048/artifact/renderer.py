'''
renderer.py
Pygame-based rendering for the 2048 game: window, grid, tiles,
score display, and game-over overlay. All config references are aligned
with config.py, the single source of truth for tunable constants.
'''
import pygame
import config as cfg
class Renderer:
    '''Handles all drawing of the 2048 game to the screen.'''
    def __init__(self, width, height, caption="2048"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self._init_fonts()
    def _init_fonts(self):
        '''Create the font objects used for text rendering.'''
        self.font_tile_small = pygame.font.Font(cfg.FONT_NAME, cfg.FONT_SIZE_TILE_2_DIGITS)
        self.font_tile_medium = pygame.font.Font(cfg.FONT_NAME, cfg.FONT_SIZE_TILE_3_DIGITS)
        self.font_tile_large = pygame.font.Font(cfg.FONT_NAME, cfg.FONT_SIZE_TILE_4_DIGITS)
        self.font_tile_xlarge = pygame.font.Font(cfg.FONT_NAME, cfg.FONT_SIZE_TILE_5_DIGITS)
        self.font_score = pygame.font.Font(cfg.FONT_NAME, cfg.FONT_SIZE_SCORE)
        self.font_title = pygame.font.Font(cfg.FONT_NAME, cfg.FONT_SIZE_TITLE)
        self.font_message = pygame.font.Font(cfg.FONT_NAME, cfg.FONT_SIZE_MESSAGE)
    def draw(self, game):
        '''Render the full game frame: background, header, grid, tiles, overlays.'''
        self.screen.fill(cfg.COLOR_BACKGROUND)
        self._draw_header(game)
        self._draw_grid_background()
        self._draw_tiles(game)
        if game.game_over:
            self._draw_game_over()
        pygame.display.flip()
    def _draw_header(self, game):
        '''Draw the title, current score, and highest tile reached.'''
        title = self.font_title.render("2048", True, cfg.COLOR_TEXT_DARK)
        self.screen.blit(title, (20, 20))
        # Score box
        self._draw_score_box("SCORE", str(game.score), self.width - 220, 20)
        self._draw_score_box("BEST TILE", str(game.highest_tile), self.width - 110, 20)
        hint = self.font_score.render("Arrow keys to move - R to restart", True, cfg.COLOR_TEXT_DARK)
        self.screen.blit(hint, (20, 110))
    def _draw_score_box(self, label, value, x, y):
        '''Draw a small rounded box showing a label and its value.'''
        box_rect = pygame.Rect(x, y, 100, 70)
        pygame.draw.rect(self.screen, cfg.COLOR_GRID_CONTAINER, box_rect, border_radius=6)
        label_surf = self.font_score.render(label, True, cfg.COLOR_TEXT_LIGHT)
        value_surf = self.font_score.render(value, True, cfg.COLOR_TEXT_LIGHT)
        label_rect = label_surf.get_rect(center=(box_rect.centerx, box_rect.y + 20))
        value_rect = value_surf.get_rect(center=(box_rect.centerx, box_rect.y + 48))
        self.screen.blit(label_surf, label_rect)
        self.screen.blit(value_surf, value_rect)
    def _draw_grid_background(self):
        '''Draw the grid container and the empty cells.'''
        grid_origin_x = (self.width - self._grid_pixel_size()) // 2
        grid_rect = pygame.Rect(
            grid_origin_x - cfg.CELL_GAP,
            cfg.GRID_TOP - cfg.CELL_GAP,
            self._grid_pixel_size() + cfg.CELL_GAP * 2,
            self._grid_pixel_size() + cfg.CELL_GAP * 2,
        )
        pygame.draw.rect(self.screen, cfg.COLOR_GRID_CONTAINER, grid_rect, border_radius=8)
        for r in range(cfg.GRID_SIZE):
            for c in range(cfg.GRID_SIZE):
                cell_rect = self._cell_rect(r, c)
                pygame.draw.rect(self.screen, cfg.COLOR_CELL_EMPTY, cell_rect, border_radius=6)
    def _grid_pixel_size(self):
        '''Total pixel size of the grid area.'''
        return cfg.GRID_SIZE * cfg.CELL_SIZE + (cfg.GRID_SIZE + 1) * cfg.CELL_GAP
    def _cell_rect(self, row, col):
        '''Return the pygame Rect for a grid cell.'''
        grid_origin_x = (self.width - self._grid_pixel_size()) // 2
        x = grid_origin_x + cfg.CELL_GAP + col * (cfg.CELL_SIZE + cfg.CELL_GAP)
        y = cfg.GRID_TOP + cfg.CELL_GAP + row * (cfg.CELL_SIZE + cfg.CELL_GAP)
        return pygame.Rect(x, y, cfg.CELL_SIZE, cfg.CELL_SIZE)
    def _draw_tiles(self, game):
        '''Draw each non-empty tile with its value and color.'''
        for r in range(game.size):
            for c in range(game.size):
                value = game.grid[r][c]
                if value == 0:
                    continue
                rect = self._cell_rect(r, c)
                bg_color, text_color = self._get_tile_color(value)
                pygame.draw.rect(self.screen, bg_color, rect, border_radius=6)
                font = self._font_for_value(value)
                text = font.render(str(value), True, text_color)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
    def _font_for_value(self, value):
        '''Choose a font size based on the number of digits in the tile value.'''
        digits = len(str(value))
        if digits <= 2:
            return self.font_tile_small
        if digits == 3:
            return self.font_tile_medium
        if digits == 4:
            return self.font_tile_large
        return self.font_tile_xlarge
    @staticmethod
    def _get_tile_color(value):
        '''Return (background_color, text_color) for a tile value.'''
        return cfg.TILE_COLORS.get(value, cfg.DEFAULT_TILE_COLOR)
    def _draw_game_over(self):
        '''Draw a semi-transparent overlay with the game-over message.'''
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((238, 228, 218, 180))
        self.screen.blit(overlay, (0, 0))
        msg = self.font_message.render("Game Over!", True, cfg.COLOR_TEXT_DARK)
        msg_rect = msg.get_rect(center=(self.width // 2, self.height // 2 - 30))
        self.screen.blit(msg, msg_rect)
        sub = self.font_score.render("Press R to play again", True, cfg.COLOR_TEXT_DARK)
        sub_rect = sub.get_rect(center=(self.width // 2, self.height // 2 + 30))
        self.screen.blit(sub, sub_rect)