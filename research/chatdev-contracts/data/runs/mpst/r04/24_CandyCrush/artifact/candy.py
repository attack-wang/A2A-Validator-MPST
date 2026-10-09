'''Candy piece: rendering, grid/pixel position, animation state.'''
import math
import random
import pygame
import settings as S
_cache = {}
def make_candy_surface(candy_type, size):
    """Pre-render a candy image (shape + shading + shine) for a given type/size."""
    key = (candy_type, size)
    if key in _cache:
        return _cache[key]
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    radius = int(size * 0.40)
    main, dark = S.CANDY_COLORS[candy_type]
    shape = candy_type  # one shape per type
    if shape == 0:  # circle
        pygame.draw.circle(surface, dark, (center, center), radius)
        pygame.draw.circle(surface, main, (center, center - size*0.03), radius - 3)
    elif shape == 1:  # rounded square
        rect = pygame.Rect(0, 0, radius*2, radius*2); rect.center = (center, center)
        pygame.draw.rect(surface, dark, rect, border_radius=size//5)
        inner = rect.inflate(-6, -6); inner.center = (center, center - 2)
        pygame.draw.rect(surface, main, inner, border_radius=size//5)
    elif shape == 2:  # diamond
        pts = [(center, center - radius), (center + radius, center), (center, center + radius), (center - radius, center)]
        pygame.draw.polygon(surface, dark, pts)
        # inner
        ...
    ...