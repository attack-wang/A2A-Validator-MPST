'''
renderer.py
All pygame drawing routines for the 2048 game: score bar, grid panel,
tiles, help text, and the game-over overlay.
'''
import pygame
from constants import (
    GRID_SIZE, CELL_SIZE, CELL_MARGIN,
    GRID_ORIGIN_X, GRID_ORIGIN_Y,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    BACKGROUND_COLOR, GRID_PANEL_COLOR, EMPTY_CELL_COLOR,
    TEXT_COLOR, LIGHT_TEXT_COLOR, TITLE_COLOR,
    TILE_COLORS, DEFAULT_TILE_COLOR,
)
class Renderer:
    """Draws the complete 2048 game frame for a given game state."""
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont("arial", 40, bold=True)
        self.label_font = pygame.font.SysFont("arial", 16, bold=True)
        self.value_font = pygame.font.SysFont("arial", 24, bold=True)
        self.tile_fonts = {
            "large": pygame.font.SysFont("arial", 44, bold=True),   # 1-2 digit tiles
            "medium": pygame.font.SysFont("arial", 34, bold=True),  # 3 digit tiles
            "small": pygame.font.SysFont("arial", 26, bold=True),   # 4+ digit tiles
        }
        self.overlay_font = pygame.font.SysFont("arial", 44, bold=True)
        self.sub_overlay_font = pygame.font.SysFont("arial", 20, bold=True)
        self.help_font = pygame.font.SysFont("arial", 16)
    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def draw(self, game):
        """Render one full frame: background, score bar, grid, tiles, overlays."""
        self.screen.fill(BACKGROUND_COLOR)
        self._draw_score_bar(game)
        self._draw_grid_panel()
        self._draw_tiles(game.grid)
        self._draw_help_text()
        if game.game_over:
            self._draw_game_over_overlay(game)
        pygame.display.flip()
    # ------------------------------------------------------------------
    # Private drawing helpers
    # ------------------------------------------------------------------
    def _draw_score_bar(self, game):
        """Draw the game title plus boxes for score and highest tile."""
        # Title
        title = self.title_font.render("2048", True, TITLE_COLOR)
        self.screen.blit(title, (GRID_ORIGIN_X, 20))
        # Score box
        self._draw_stat_box("SCORE", str(game.score),
                            WINDOW_WIDTH - 2 * (CELL_SIZE + CELL_MARGIN) - CELL_MARGIN,
                            20)
        # Highest tile box
        self._draw_stat_box("BEST TILE", str(game.highest_tile),
                            WINDOW_WIDTH - (CELL_SIZE + CELL_MARGIN) - CELL_MARGIN,
                            20)
    def _draw_stat_box(self, label, value, x, y):
        """Draw a small rounded box showing a label and its numeric value."""
        box_rect = pygame.Rect(x, y, CELL_SIZE + CELL_MARGIN, 70)
        pygame.draw.rect(self.screen, EMPTY_CELL_COLOR, box_rect, border_radius=6)
        label_surf = self.label_font.render(label, True, LIGHT_TEXT_COLOR)
        value_surf = self.value_font.render(value, True, LIGHT_TEXT_COLOR)
        label_rect = label_surf.get_rect(center=(box_rect.centerx, y + 22))
        value_rect = value_surf.get_rect(center=(box_rect.centerx, y + 48))
        self.screen.blit(label_surf, label_rect)
        self.screen.blit(value_surf, value_rect)
    def _draw_grid_panel(self):
        """Draw the grid background panel and the empty cell slots."""
        panel_rect = pygame.Rect(
            GRID_ORIGIN_X, GRID_ORIGIN_Y,
            CELL_SIZE * GRID_SIZE + CELL_MARGIN * (GRID_SIZE + 1),
            CELL_SIZE * GRID_SIZE + CELL_MARGIN * (GRID_SIZE + 1),
        )
        pygame.draw.rect(self.screen, GRID_PANEL_COLOR, panel_rect, border_radius=8)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell_rect = self._cell_rect(r, c)
                pygame.draw.rect(self.screen, EMPTY_CELL_COLOR, cell_rect, border_radius=6)
    def _cell_rect(self, row, col):
        """Return the pygame Rect for the cell at (row, col)."""
        x = GRID_ORIGIN_X + CELL_MARGIN + col * (CELL_SIZE + CELL_MARGIN)
        y = GRID_ORIGIN_Y + CELL_MARGIN + row * (CELL_SIZE + CELL_MARGIN)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    def _draw_tiles(self, grid):
        """Draw every non-empty tile with the proper color and font size."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = grid[r][c]
                if value == 0:
                    continue
                rect = self._cell_rect(r, c)
                tile_color, text_color = TILE_COLORS.get(value, DEFAULT_TILE_COLOR)
                pygame.draw.rect(self.screen, tile_color, rect, border_radius=6)
                self._draw_tile_value(value, rect, text_color)
    def _draw_tile_value(self, value, rect, text_color):
        """Render a tile's number centered in its cell, shrinking font for long numbers."""
        if value < 100:
            font = self.tile_fonts["large"]
        elif value < 1000:
            font = self.tile_fonts["medium"]
        else:
            font = self.tile_fonts["small"]
        text = font.render(str(value), True, text_color)
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)
    def _draw_help_text(self):
        """Draw the controls hint line under the grid."""
        help_text = "Arrow keys / WASD: move   |   R: restart   |   ESC: quit"
        surf = self.help_font.render(help_text, True, TEXT_COLOR)
        rect = surf.get_rect(center=(WINDOW_WIDTH // 2,
                                     WINDOW_HEIGHT - HELP_BAR_HEIGHT // 2))
        self.screen.blit(surf, rect)
    def _draw_game_over_overlay(self, game):
        """Draw a semi-transparent overlay announcing the game-over state."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((187, 173, 160, 180))
        self.screen.blit(overlay, (0, 0))
        title = self.overlay_font.render("GAME OVER!", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        self.screen.blit(title, title_rect)
        final_score = self.sub_overlay_font.render(
            f"Final score: {game.score}   |   Best tile: {game.highest_tile}",
            True, TEXT_COLOR)
        score_rect = final_score.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(final_score, score_rect)
        restart = self.sub_overlay_font.render("Press R to play again", True, TEXT_COLOR)
        restart_rect = restart.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(restart, restart_rect)