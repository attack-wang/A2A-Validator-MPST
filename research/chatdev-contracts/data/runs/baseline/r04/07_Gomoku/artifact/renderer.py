'''
Rendering module for the Gomoku game.
Draws the board grid, stones, hover preview, last-move marker,
winning line and the status panel using pygame.
'''
import pygame
from constants import (
    BOARD_SIZE,
    CELL_SIZE,
    MARGIN,
    INFO_HEIGHT,
    EMPTY,
    BLACK,
    WHITE,
    COLOR_BACKGROUND,
    COLOR_GRID,
    COLOR_BLACK_STONE,
    COLOR_WHITE_STONE,
    COLOR_TEXT,
    COLOR_HIGHLIGHT,
    COLOR_PANEL,
    COLOR_BUTTON,
    COLOR_BUTTON_TEXT,
    STAR_POINTS,
    STONE_RADIUS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)
class Renderer:
    """Responsible for drawing every visual element of the game."""
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont("arial", 32, bold=True)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.font_button = pygame.font.SysFont("arial", 18, bold=True)
        self._status_font_cache = {}
        # Rect of the "New Game" button inside the status panel
        self.restart_button_rect = pygame.Rect(
            WINDOW_WIDTH - 150, WINDOW_HEIGHT - INFO_HEIGHT + 12, 120, 36
        )
    # ... (coordinate helpers, drawing primitives as before)
    def _get_status_font(self, size):
        """Return a cached bold status font of the requested size."""
        if size not in self._status_font_cache:
            self._status_font_cache[size] = pygame.font.SysFont("arial", size, bold=True)
        return self._status_font_cache[size]
    def render_fitted_text(self, text, color, max_width, start_size=32, min_size=14):
        """Render `text` shrinking the font until it fits `max_width` pixels."""
        size = start_size
        surface = self._get_status_font(size).render(text, True, color)
        while size > min_size and surface.get_width() > max_width:
            size -= 2
            surface = self._get_status_font(size).render(text, True, color)
        return surface
    def draw_status_panel(self, message, message_color):
        """Draw the bottom panel with the status message and the restart button."""
        panel_rect = pygame.Rect(0, WINDOW_HEIGHT - INFO_HEIGHT, WINDOW_WIDTH, INFO_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect)
        pygame.draw.line(
            self.screen,
            COLOR_GRID,
            (0, WINDOW_HEIGHT - INFO_HEIGHT),
            (WINDOW_WIDTH, WINDOW_HEIGHT - INFO_HEIGHT),
            2,
        )
        # Shrink the message automatically so it never overlaps the button
        max_text_width = self.restart_button_rect.left - MARGIN - 12
        text = self.render_fitted_text(message, message_color, max_text_width)
        self.screen.blit(text, (MARGIN, WINDOW_HEIGHT - INFO_HEIGHT + 8))
        hint = self.font_small.render(
            "Left click: place stone   |   R: restart   |   ESC: quit", True, COLOR_TEXT
        )
        self.screen.blit(hint, (MARGIN, WINDOW_HEIGHT - INFO_HEIGHT + 52))
        self.draw_button()