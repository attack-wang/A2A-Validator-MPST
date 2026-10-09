"""Pre-rendered candy sprites (one image per candy type), built once."""
import pygame
from config import CELL_SIZE, CANDY_TYPES
_IMAGE_CACHE = {}
def _make_candy_image(type_id):
    """Render a candy sprite for the given type (distinct shape per type)."""
    size = CELL_SIZE
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = cy = size // 2
    radius = int(size * 0.38)
    name, color, dark, light = CANDY_TYPES[type_id]
    if type_id == 0:      # red jelly — circle
        pygame.draw.circle(s, color, (cx, cy), radius)
        pygame.draw.circle(s, dark, (cx, cy), radius, 3)
        pygame.draw.circle(s, light, (cx - radius // 3, cy - radius // 3), radius // 4)
    elif type_id == 1:    # orange drop — rounded square
        rect = pygame.Rect(0, 0, radius * 2, radius * 2)
        rect.center = (cx, cy)
        pygame.draw.rect(s, color, rect, border_radius=10)
        pygame.draw.rect(s, dark, rect, 3, border_radius=10)
        ...
    ...
    return s
def get_candy_image(type_id):
    if type_id not in _IMAGE_CACHE:
        _IMAGE_CACHE[type_id] = _make_candy_image(type_id)
    return _IMAGE_CACHE[type_id]