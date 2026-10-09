'''
Shared helpers: math clamp, font caching, text drawing, gradient making.
'''
import pygame
_font_cache = {}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
def clamp(v, lo, hi):
    return max(lo, min(hi, v))
def get_font(size, bold=True):
    key = (size, bold)
    if key not in _font_cache:
        try:
            _font_cache[key] = pygame.font.SysFont("arial", size, bold=bold)
        except Exception:
            _font_cache[key] = pygame.font.Font(None, size)
    return _font_cache[key]
def draw_text(surface, text, size, center_x, center_y, color=WHITE, outline_color=None, outline_width=2, bold=True):
    font = get_font(size, bold)
    img = font.render(text, True, color)
    rect = img.get_rect(center=(center_x, center_y))
    if outline_color:
        shadow = font.render(text, True, outline_color)
        w = outline_width
        for dx, dy in ((-w, 0), (w, 0), (0, -w), (0, w), (-w, -w), (w, -w), (-w, w), (w, w)):
            surface.blit(shadow, rect.move(dx, dy))
    surface.blit(img, rect)
def make_gradient(width, height, top, bottom):
    surf = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(1, height - 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        pygame.draw.line(surf, color, (0, y), (width, y))
    return surf