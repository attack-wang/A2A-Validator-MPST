'''UI module: text rendering helpers with font caching and HUD panels.'''
import pygame
import config
_font_cache = {}
def get_font(size, bold=False):
    key = (size, bold)
    if key not in _font_cache:
        _font_cache[key] = pygame.font.SysFont("arial", size, bold=bold)
    return _font_cache[key]
def draw_text(surface, text, size, color, x, y, anchor="topleft", bold=False):
    font = get_font(size, bold)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if anchor == "topleft":
        rect.topleft = (x, y)
    elif anchor == "topright":
        rect.topright = (x, y)
    elif anchor == "midtop":
        rect.midtop = (x, y)
    elif anchor == "center":
        rect.center = (x, y)
    elif anchor == "midbottom":
        rect.midbottom = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rendered, rect)
    return rect
def draw_panel(surface, rect, color=(30, 34, 56), border=(90, 100, 140)):
    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, border, rect, 2, border_radius=10)