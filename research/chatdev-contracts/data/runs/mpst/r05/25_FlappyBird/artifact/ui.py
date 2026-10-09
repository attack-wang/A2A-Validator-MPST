'''Font caching and outlined text rendering helpers.'''
import pygame
_font_cache = {}
def get_font(size):
    """Return a cached default font of the requested size."""
    if size not in _font_cache:
        _font_cache[size] = pygame.font.Font(None, size)
    return _font_cache[size]
def draw_text(surface, text, size, color, center, outline_color=None, outline_width=2):
    """Draw text centered at `center`, optionally with a solid outline."""
    font = get_font(size)
    text_surf = font.render(text, True, color)
    cx, cy = center
    if outline_color:
        outline_surf = font.render(text, True, outline_color)
        offsets = []
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx == 0 and dy == 0:
                    continue
                offsets.append((dx, dy))
        for dx, dy in offsets:
            surface.blit(outline_surf, outline_surf.get_rect(center=(cx + dx, cy + dy)))
    surface.blit(text_surf, text_surf.get_rect(center=(cx, cy)))