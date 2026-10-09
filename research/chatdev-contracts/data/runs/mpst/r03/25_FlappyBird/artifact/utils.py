"""Small helper utilities: text rendering, high-score persistence, math helpers."""
import os
import pygame
from settings import WHITE
_font_cache = {}
def get_font(size, bold=False):
    """Return a cached font keyed by (size, bold) so shared fonts are never mutated."""
    key = (size, bold)
    if key not in _font_cache:
        font = pygame.font.Font(None, size)
        font.set_bold(bold)
        _font_cache[key] = font
    return _font_cache[key]
def draw_text(surface, text, size, x, y, color=WHITE, align="center", bold=False, outline=None):
    """Render text onto surface with optional alignment and outline."""
    font = get_font(size, bold)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if align == "center":
        rect.center = (x, y)
    elif align == "topleft":
        rect.topleft = (x, y)
    elif align == "topright":
        rect.topright = (x, y)
    elif align == "midtop":
        rect.midtop = (x, y)
    elif align == "midbottom":
        rect.midbottom = (x, y)
    if outline:
        o = font.render(text, True, outline)
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            surface.blit(o, rect.move(dx, dy))
    surface.blit(surf, rect)
    return rect
def clamp(value, lo, hi):
    """Clamp value into [lo, hi]."""
    return max(lo, min(hi, value))
def circle_rect_collision(cx, cy, radius, rect):
    """Circle-vs-rect collision via closest-point test."""
    closest_x = clamp(cx, rect.left, rect.right)
    closest_y = clamp(cy, rect.top, rect.bottom)
    dx = cx - closest_x
    dy = cy - closest_y
    return dx * dx + dy * dy <= radius * radius
def load_high_score(path):
    """Read persisted high score; return 0 on any failure."""
    try:
        with open(path, "r") as f:
            return int(f.read().strip() or 0)
    except (OSError, ValueError):
        return 0
def save_high_score(path, score):
    """Persist high score; silently ignore write failures."""
    try:
        with open(path, "w") as f:
            f.write(str(int(score)))
    except OSError:
        pass