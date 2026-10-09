"""Shared helper utilities."""
import pygame
def draw_text(surface, text, font, color, center, shadow_color=None, shadow_offset=2):
    """Render text centered at a position with optional drop shadow."""
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    if shadow_color is not None:
        shadow = font.render(text, True, shadow_color)
        surface.blit(shadow, rect.move(shadow_offset, shadow_offset))
    surface.blit(rendered, rect)
    return rect
def clamp(value, minimum, maximum):
    """Constrain value to the inclusive range [minimum, maximum]."""
    return max(minimum, min(maximum, value))
def draw_cloud(surface, x, y, scale, color):
    """Draw a simple puffy cloud made of overlapping circles."""
    r = int(14 * scale)
    pygame.draw.circle(surface, color, (x, y), r)
    pygame.draw.circle(surface, color, (x + r, y + int(r * 0.2)), int(r * 0.8))
    pygame.draw.circle(surface, color, (x - r, y + int(r * 0.25)), int(r * 0.7))
    pygame.draw.circle(surface, color, (x + int(r * 0.3), y - int(r * 0.5)), int(r * 0.7))