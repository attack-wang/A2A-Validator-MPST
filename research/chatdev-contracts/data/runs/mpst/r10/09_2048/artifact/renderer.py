'''
renderer.py
Pygame-based rendering for the 2048 game: window layout, grid, tiles, score panel and game-over overlay.
'''
import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, CELL_SIZE, CELL_MARGIN,
    GRID_PADDING, GRID_TOP,
    COLOR_BACKGROUND, COLOR_GRID_BACKGROUND, COLOR_EMPTY_CELL,
    COLOR_TEXT_DARK, COLOR_TEXT_LIGHT,
    TILE_COLORS, TILE_COLOR_DEFAULT, DARK_TEXT_TILES,
    FONT_SIZE_TITLE, FONT_SIZE_LABEL, FONT_SIZE_SCORE,
    FONT_SIZE_TILE_LARGE, FONT_SIZE_TILE_MEDIUM, FONT_SIZE_TILE_SMALL,
    FONT_SIZE_TILE_TINY, FONT_SIZE_MESSAGE, FONT_SIZE_HINT,
)
class Renderer:
    """Draws the complete 2048 game window for a given Game instance."""
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, FONT_SIZE_TITLE)
        self.font_label = pygame.font.Font(None, FONT_SIZE_LABEL)
        self.font_score = pygame.font.Font(None, FONT_SIZE_SCORE)
        self.font_tile_large = pygame.font.Font(None, FONT_SIZE_TILE_LARGE)
        self.font_tile_medium = pygame.font.Font(None, FONT_SIZE_TILE_MEDIUM)
        self.font_tile_small = pygame.font.Font(None, FONT_SIZE_TILE_SMALL)
        self.font_tile_tiny = pygame.font.Font(None, FONT_SIZE_TILE_TINY)
        self.font_message = pygame.font.Font(None, FONT_SIZE_MESSAGE)
        self.font_hint = pygame.font.Font(None, FONT_SIZE_HINT)
        # Precompute grid geometry
        self.grid_pixel_size = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_MARGIN
        self.grid_left = (WINDOW_WIDTH - self.grid_pixel_size) // 2
    def draw(self, game):
        """Render one full frame: background, header, grid, tiles and overlays."""
        self.screen.fill(COLOR_BACKGROUND)
        self._draw_header(game)
        self._draw_grid_background()
        self._draw_tiles(game)
        self._draw_footer()
        if game.is_game_over():
            self._draw_game_over_overlay()
    def _draw_header(self, game):
        """Draw the game title plus the current score and highest tile panels."""
        # Title
        title = self.font_title.render("2048", True, COLOR_TEXT_DARK)
        self.screen.blit(title, (self.grid_left, 20))
        # Score panel
        self._draw_score_panel("SCORE", str(game.score),
                               self.grid_left + self.grid_pixel_size - 200, 20)
        self._draw_score_panel("HIGHEST", str(game.highest_tile),
                               self.grid_left + self.grid_pixel_size - 95, 20)
    def _draw_score_panel(self, label, value, x, y):
        """Draw a single rounded score box with a label and a value."""
        panel_rect = pygame.Rect(x, y, 90, 60)
        pygame.draw.rect(self.screen, COLOR_GRID_BACKGROUND, panel_rect, border_radius=6)
        label_surface = self.font_label.render(label, True, COLOR_TEXT_LIGHT)
        value_surface = self.font_score.render(value, True, COLOR_TEXT_LIGHT)
        label_rect = label_surface.get_rect(center=(panel_rect.centerx, y + 18))
        value_rect = value_surface.get_rect(center=(panel_rect.centerx, y + 42))
        self.screen.blit(label_surface, label_rect)
        self.screen.blit(value_surface, value_rect)
    def _draw_grid_background(self):
        """Draw the grid container and the empty cell slots."""
        grid_rect = pygame.Rect(self.grid_left, GRID_TOP,
                                self.grid_pixel_size, self.grid_pixel_size)
        pygame.draw.rect(self.screen, COLOR_GRID_BACKGROUND, grid_rect, border_radius=8)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell_rect = self._cell_rect(r, c)
                pygame.draw.rect(self.screen, COLOR_EMPTY_CELL, cell_rect, border_radius=6)
    def _cell_rect(self, row, col):
        """Return the pygame.Rect of the cell at (row, col)."""
        x = self.grid_left + CELL_MARGIN + col * (CELL_SIZE + CELL_MARGIN)
        y = GRID_TOP + CELL_MARGIN + row * (CELL_SIZE + CELL_MARGIN)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    def _draw_tiles(self, game):
        """Draw every non-empty tile with its value centred in its cell."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = game.grid[r][c]
                if value == 0:
                    continue
                cell_rect = self._cell_rect(r, c)
                color = TILE_COLORS.get(value, TILE_COLOR_DEFAULT)
                pygame.draw.rect(self.screen, color, cell_rect, border_radius=6)
                text_color = COLOR_TEXT_DARK if value in DARK_TEXT_TILES else COLOR_TEXT_LIGHT
                font = self._font_for_value(value)
                surface = font.render(str(value), True, text_color)
                surface_rect = surface.get_rect(center=cell_rect.center)
                self.screen.blit(surface, surface_rect)
    @staticmethod
    def _font_for_value(value):
        """Choose a font size that fits the number of digits in the tile value."""
        digits = len(str(value))
        if digits <= 2:
            return ... 