'''
ui.py
Rendering helpers for text and the game board grid.
'''
import pygame
from settings import (WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, GRID_COLOR,
                      FONT_NAME)
def draw_text(surface, text, size, color, center=None, topleft=None):
    """Render bold text onto the surface at the requested position."""
    font = pygame.font.SysFont(FONT_NAME, size, bold=True)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center is not None:
        rect.center = center
    if topleft is not None:
        rect.topleft = topleft
    surface.blit(rendered, rect)
    return rect
def draw_grid(surface):
    """Draw faint grid lines over the whole board."""
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))